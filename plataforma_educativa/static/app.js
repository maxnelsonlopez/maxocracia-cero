/* Plataforma Educativa — frontend vanilla JS (sin framework).
 * Usa fetch() contra la API REST y guarda el token en localStorage.
 */
"use strict";

var TOKEN_KEY = "plataforma_educativa_token";

// ------------------------------------------------------------------
// Utilidades
// ------------------------------------------------------------------
function $(id) { return document.getElementById(id); }

function api(path, opts) {
  opts = opts || {};
  var headers = Object.assign({ "Content-Type": "application/json" }, opts.headers || {});
  if (getToken()) headers["X-Auth-Token"] = getToken();
  var init = { method: opts.method || "GET", headers: headers };
  if (opts.body !== undefined) init.body = JSON.stringify(opts.body);
  return fetch(path, init).then(function (res) {
    if (res.status === 401) { showAuth(); throw new Error("Sesión expirada"); }
    return res.json().then(function (data) {
      data.__status = res.status;
      return data;
    });
  });
}

function getToken() { return localStorage.getItem(TOKEN_KEY) || ""; }
function setToken(t) { localStorage.setItem(TOKEN_KEY, t); }
function clearToken() { localStorage.removeItem(TOKEN_KEY); }

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}

function isoWeek(d) {
  var date = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  var day = date.getUTCDay() || 7;
  date.setUTCDate(date.getUTCDate() + 4 - day);
  var yearStart = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
  var week = Math.ceil((((date - yearStart) / 86400000) + 1) / 7);
  return date.getUTCFullYear() + "-W" + String(week).padStart(2, "0");
}

var estadoLabel = {
  not_seen: "Sin ver", learning: "En curso", test_passed: "Aprobado", mastered: "Dominado"
};

// ------------------------------------------------------------------
// La ciudad del saber (M14): el conocimiento como mapa que se ilumina.
// Niebla: los barrios lejanos se insinúan; cada lote construido alumbre.
// Lore: la historia del barrio se revela al entrar (motor de curiosidad).
// ------------------------------------------------------------------
var CITY_LORE = {
  matematicas: "Los números fueron la primera lengua de la ciudad: medir, repartir, contar lo que importa. Cada fórmula es un puente entre dos veredas.",
  naturaleza: "El barrio verde: la ciudad no está SOBRE la tierra, está EN ella. Aquí se estudia el agua, el suelo y los ciclos que nos sostienen.",
  higiene: "Las murallas de la salud: pequeñas decisiones diarias que protegen al barrio entero. Limpiar, dormir, moverte: eso también es arquitectura.",
  relaciones: "Las plazas y los salones: la ciudad se hace entre personas. Empatía, escucha y palabra: el cemento invisible de todo lo demás.",
  computadores: "El barrio de los inventos: máquinas que aprenden a trabajar con nosotros. La llave es el criterio, no el aparato.",
  escritura: "Los escribanos de la ciudad: el pensamiento se vuelve cosa cuando se escribe. Quien escribe, deja mapa.",
  lectura: "La biblioteca central: leer es caminar por la cabeza de otros sin salir de la plaza. Se aprende a preguntar, no a repetir.",
  lenguaje: "El mercado de las palabras: hablar, escuchar, persuadir. La oratoria es la plaza hablada; el idioma, la moneda compartida."
};

var cityView = "tree";
var cityBranches = null;

function toggleCity() {
  cityView = cityView === "tree" ? "city" : "tree";
  $("btn-city-toggle").textContent = cityView === "tree" ? "🗺 La ciudad" : "🌳 El árbol";
  renderView();
}

function renderView() {
  if (!cityBranches) return;
  if (cityView === "city") renderCity(cityBranches);
  else renderTree(cityBranches);
}

function renderCity(branches) {
  var search = ($("tree-search").value || "").toLowerCase();
  var html = "";
  branches.forEach(function (br) {
    var iluminado = br.topics.some(function (t) { return t.estado !== "not_seen" || t.unlocked; });
    var visibles = br.topics.filter(function (t) {
      return !search || t.titulo.toLowerCase().indexOf(search) !== -1;
    });
    html += '<div class="city-district' + (iluminado ? " lit" : " fog") + '">' +
      '<h3>' + esc(br.nombre) + (iluminado ? "" : " <span class='muted'>· barrio por descubrir</span>") + "</h3>" +
      (iluminado ? "<p class='muted'>" + esc(br.descripcion) + "</p>" +
        "<p class='city-lore'>" + esc(CITY_LORE[br.slug] || "") + "</p>" : "");
    html += '<div class="city-lots">';
    visibles.forEach(function (t) {
      var icon = t.estado === "mastered" ? "🏛" : (t.ready_to_teach ? "✨" : t.estado === "test_passed" ? "✅" : t.estado === "learning" ? "🔨" : t.unlocked ? "◽" : "🔒");
      html += '<button class="city-lot" data-action="lot" data-topic="' + t.id + '" title="' + esc(t.titulo) + '">' +
        icon + '<span>' + esc(t.titulo) + "</span>" +
        (t.dificultad ? '<small>' + "★".repeat(t.dificultad) + "</small>" : "") + "</button>";
    });
    html += "</div></div>";
  });
  $("tree").innerHTML = html || '<p class="muted">Sin barrios.</p>';
  bindTopicButtons();
}

function loadSuggestion() {
  api("/api/suggest").then(function (data) {
    var el = $("city-guide");
    if (!data.suggestion) {
      el.hidden = true;
      return;
    }
    var s = data.suggestion;
    el.innerHTML =
      '<b class="city-guide-label">🧭 El compañero de la ciudad sugiere:</b> ' +
      esc(s.titulo) + ' <span class="muted">· barrio de ' + esc(s.branch_nombre) +
      (s.dificultad ? ' · ' + "★".repeat(s.dificultad) : "") + "</span> " +
      '<button class="small primary" data-action="start" data-topic="' + s.topic_id + '">Empezar a construir</button>';
    el.hidden = false;
    bindTopicButtons();
  }).catch(function () { $("city-guide").hidden = true; });
}

function showTopicHint(topicId) {
  var topic = null;
  (cityBranches || []).some(function (b) {
    return b.topics.some(function (t) {
      if (t.id === topicId) { topic = t; return true; }
      return false;
    });
  });
  if (!topic) return;
  if (topic.estado === "not_seen" && topic.unlocked) startTopic(topicId);
  else if (topic.estado === "learning") openTest(topicId);
  else toggleCity(); // construir detalles, obras y triada en la vista árbol
}

var AVAILABLE_SLOTS = ["LUN 19:00", "MIE 19:00", "VIE 18:00", "SÁB 10:00"];
var selectedSlots = {};

// ------------------------------------------------------------------
// Vistas
// ------------------------------------------------------------------
function showAuth() {
  $("auth-view").hidden = false;
  $("app-view").hidden = true;
  $("welcome").textContent = "";
  $("auth-error").hidden = true;
}

function showApp() {
  $("auth-view").hidden = true;
  $("app-view").hidden = false;
}

// ------------------------------------------------------------------
// Carga general
// ------------------------------------------------------------------
function loadAll() {
  return Promise.all([
    api("/api/me"),
    api("/api/tree"),
    api("/api/availability"),
    api("/api/meetings")
  ]).then(function (res) {
    renderUser(res[0].user);
    renderProgress(res[0].branches);
    cityBranches = res[1].branches;
    renderView();
    loadSuggestion();
    renderAvailability(res[2].availability || []);
    renderMeetings(res[3].meetings || []);
    toggleCoordinator(res[0].user.is_coordinator);
  }).catch(console.error);
}

function renderUser(user) {
  $("welcome").textContent = "Hola, " + user.username + (user.is_coordinator ? " · coordinador" : "");
}

function renderProgress(branches) {
  var html = "";
  branches.forEach(function (b) {
    html += '<div class="progress-row">' +
      '<span class="progress-name">' + esc(b.nombre) + "</span>" +
      '<span class="progress-bar"><span class="progress-fill" style="width:' + b.progress_pct + '%"></span></span>' +
      '<span class="progress-num">' + b.progress_pct + "% (" + b.topics_passed + "/" + b.topics_total + ")</span>" +
      "</div>";
  });
  $("progress").innerHTML = html || '<p class="muted">Sin datos.</p>';
}

function renderTree(branches) {
  var search = ($("tree-search").value || "").toLowerCase();
  var html = "";
  branches.forEach(function (br, bi) {
    var open = bi === 0;
    html += '<div class="branch">' +
      '<button class="branch-header" data-toggle="branches-' + br.id + '">' +
      '<span>' + esc(br.nombre) + "</span><small>" + esc(br.descripcion) + "</small></button>" +
      '<div id="branches-' + br.id + '" class="branch-body"' + (open ? "" : " hidden") + ">";
    br.topics.forEach(function (t) {
      if (search && t.titulo.toLowerCase().indexOf(search) === -1) return;
      html += renderTopic(t);
    });
    html += "</div></div>";
  });
  $("tree").innerHTML = html;

  document.querySelectorAll("[data-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var el = $(btn.getAttribute("data-toggle"));
      if (el) el.hidden = !el.hidden;
    });
  });

  bindTopicButtons();
}

function renderTopic(t) {
  var locked = !t.unlocked;
  var st = t.estado;
  var actions = "";
  var showTeach = st === "test_passed" || st === "mastered";
  if (st === "not_seen" || st === "learning") {
    if (!locked) {
      actions += '<button class="small" data-action="start" data-topic="' + t.id + '">Empezar</button>';
      actions += '<button class="small primary" data-action="test" data-topic="' + t.id + '">Hacer test</button>';
    } else {
      actions += '<span class="hint">🔒 primero aprueba el prerrequisito</span>';
    }
  } else {
    if (!locked) actions += '<button class="small primary" data-action="test" data-topic="' + t.id + '">Rehacer test</button>';
    if (showTeach) {
      if (t.evidence) {
        actions += '<span class="badge mastered" title="' + esc(t.evidence.titulo) + '">Material ' + esc(t.evidence.tipo) + " ✓</span>";
      } else {
        actions += '<button class="small" data-action="evidence" data-topic="' + t.id + '">Aportar material</button>';
      }
    }
  }
  var label = t.ready_to_teach ? "Listo para enseñar" : (estadoLabel[st] || st);
  var badge = st === "mastered" ? "badge mastered" : (t.ready_to_teach ? "badge ready" : (st === "test_passed" ? "badge passed" : "badge"));
  return '<div class="topic">' +
    '<div class="topic-main">' +
    '<div class="topic-title">' + esc(t.titulo) + (t.dificultad ? ' <span class="diff">' + "★".repeat(t.dificultad) + "</span>" : "") + "</div>" +
    '<div class="topic-sub">' + esc(t.descripcion) + " · " + t.questions + " preguntas" + (locked ? " · 🔒 prerrequisito" : "") + "</div>" +
    "</div>" +
    '<span class="' + badge + '">' + esc(label) + "</span>" +
    (st !== "not_seen" ? '<span class="score">' + (t.score == null ? "" : t.score + "%") + "</span>" : "") +
    '<div class="topic-actions">' + actions + "</div>" +
    "</div>";
}

function bindTopicButtons() {
  document.querySelectorAll("[data-action]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var action = btn.getAttribute("data-action");
      var topicId = Number(btn.getAttribute("data-topic"));
      if (action === "start") startTopic(topicId);
      else if (action === "test") openTest(topicId);
      else if (action === "mentor") requestMentorship(topicId);
      else if (action === "evidence") openEvidence(topicId);
      else if (action === "lot") showTopicHint(topicId);
    });
  });
}

function toggleCoordinator(isCoordinator) {
  $("coordinator-zone").hidden = !isCoordinator;
}

// ------------------------------------------------------------------
// Acciones de tema
// ------------------------------------------------------------------
function startTopic(topicId) {
  api("/api/topics/" + topicId + "/start", { method: "POST", body: {} })
    .then(function (data) {
      if (data.__status === 403) { alert(data.error); return; }
      loadAll();
    })
    .catch(console.error);
}

function requestMentorship(topicId) {
  api("/api/topics/" + topicId + "/request-mentorship", { method: "POST", body: {} })
    .then(function (data) {
      alert(data.message || "Solicitud enviada.");
      loadAll();
    })
    .catch(console.error);
}

// ------------------------------------------------------------------
// Test
// ------------------------------------------------------------------
var testTopic = null;

function openTest(topicId) {
  api("/api/topics/" + topicId).then(function (data) {
    if (data.__status === 404) { alert(data.error); return; }
    testTopic = topicId;
    $("test-title").textContent = "Test: " + data.titulo;
    var html = "";
    data.preguntas.forEach(function (q, i) {
      html += '<div class="question"><p>' + (i + 1) + ". " + esc(q.pregunta) + "</p>";
      q.opciones.forEach(function (opt, j) {
        html += '<label class="option"><input type="radio" name="q-' + i + '" value="' + j + '"> ' + esc(opt) + "</label>";
      });
      // La explicación NO se muestra antes de responder (se revelaría la
      // respuesta); aparece como corrección tras enviar.
      html += "</div>";
    });
    $("test-body").innerHTML = html || '<p class="muted">Sin preguntas.</p>';
    $("test-modal").hidden = false;
  });
}

function closeTest() { $("test-modal").hidden = true; testTopic = null; }

// ------------------------------------------------------------------
// Material de enseñanza (M13): la vacuación sin muros
// ------------------------------------------------------------------
var evidenceTopic = null;

function openEvidence(topicId) {
  evidenceTopic = topicId;
  $("evidence-tipo").value = "texto";
  $("evidence-titulo").value = "";
  $("evidence-url").value = "";
  $("evidence-texto").value = "";
  $("evidence-error").hidden = true;
  $("evidence-modal").hidden = false;
}

function closeEvidence() { $("evidence-modal").hidden = true; evidenceTopic = null; }

function submitEvidence() {
  if (!evidenceTopic) return;
  var payload = {
    tipo: $("evidence-tipo").value,
    titulo: $("evidence-titulo").value.trim(),
    url: $("evidence-url").value.trim(),
    texto: $("evidence-texto").value.trim()
  };
  if (!payload.titulo) { $("evidence-error").textContent = "Dales un título a tu material."; $("evidence-error").hidden = false; return; }
  if (payload.tipo === "texto" && !payload.texto) { $("evidence-error").textContent = "Para texto, escribe el contenido."; $("evidence-error").hidden = false; return; }
  if (payload.tipo !== "texto" && !payload.url) { $("evidence-error").textContent = "Pega la dirección (URL) del archivo."; $("evidence-error").hidden = false; return; }

  $("btn-evidence-submit").disabled = true;
  api("/api/topics/" + evidenceTopic + "/evidence", { method: "POST", body: payload })
    .then(function (data) {
      $("btn-evidence-submit").disabled = false;
      if (data.__status === 201) { closeEvidence(); loadAll(); }
      else {
        $("evidence-error").textContent = data.error || "No se pudo guardar.";
        $("evidence-error").hidden = false;
      }
    })
    .catch(function () {
      $("btn-evidence-submit").disabled = false;
      $("evidence-error").textContent = "Error de conexión.";
      $("evidence-error").hidden = false;
    });
}

function submitTest() {
  var testBody = $("test-body");
  var radios = testBody.querySelectorAll('input[type="radio"]:checked');
  var byName = {};
  radios.forEach(function (r) { byName[r.name] = Number(r.value); });
  var count = testBody.querySelectorAll(".question").length;
  var answers = [];
  for (var i = 0; i < count; i++) answers.push(byName["q-" + i] != null ? byName["q-" + i] : -1);

  api("/api/topics/" + testTopic + "/test", { method: "POST", body: { answers: answers } })
    .then(function (data) {
      closeTest();
      alert("Resultado: " + data.correct + "/" + data.total + " (" + data.score + "%). " +
        (data.passed ? "¡Aprobado!" : "Aún no alcanzas el 70%."));
      loadAll();
    })
    .catch(console.error);
}

// ------------------------------------------------------------------
// Disponibilidad
// ------------------------------------------------------------------
function renderAvailability(list) {
  var week = $("av-week").value || isoWeek(new Date());
  $("av-week").value = week;
  var current = {};
  var found = list.find(function (a) { return a.week === week; });
  if (found) found.slots.forEach(function (s) { current[s] = true; });
  selectedSlots = current;
  var html = "";
  AVAILABLE_SLOTS.forEach(function (slot) {
    var on = selectedSlots[slot];
    html += '<button class="chip' + (on ? " on" : "") + '" data-slot="' + esc(slot) + '">' + esc(slot) + "</button>";
  });
  $("slot-chips").innerHTML = html;
  document.querySelectorAll("[data-slot]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var s = btn.getAttribute("data-slot");
      selectedSlots[s] = !selectedSlots[s];
      btn.classList.toggle("on", !!selectedSlots[s]);
    });
  });
}

// ------------------------------------------------------------------
// Reuniones
// ------------------------------------------------------------------
function renderMeetings(meetings) {
  var html = meetings.map(function (m) {
    var parts = '<div class="meeting">' +
      '<div class="meeting-title">' + esc(m.topic_titulo) + " · " + esc(m.branch_nombre) + "</div>" +
      "<div>" + esc(m.fecha) + " " + esc(m.hora_inicio) + " · " + m.participants_count + "/8" +
      " · monitor: " + (m.monitor_username ? esc(m.monitor_username) : "—") + " · " + esc(m.estado) + "</div>" +
      '<div class="topic-actions"><button class="small" data-join="' + m.id + '">Unirme</button></div>' +
      (m.monitor_username ? '<div class="topic-actions"><button class="small" data-attend="' + m.id + '">Marcar asistencia</button></div>' : "") +
      "</div>";
    return parts;
  }).join("");
  $("my-meetings").innerHTML = html || '<p class="muted">No hay reuniones esta semana.</p>';

  document.querySelectorAll("[data-join]").forEach(function (btn) {
    btn.addEventListener("click", function () { joinMeeting(Number(btn.getAttribute("data-join"))); });
  });
  document.querySelectorAll("[data-attend]").forEach(function (btn) {
    btn.addEventListener("click", function () { attendMeeting(Number(btn.getAttribute("data-attend"))); });
  });
}

function loadMeetings() {
  api("/api/meetings").then(function (data) { renderMeetings(data.meetings || []); });
}

function joinMeeting(id) {
  api("/api/meetings/" + id + "/join", { method: "POST", body: {} }).then(function (data) {
    if (data.__status === 409) { alert(data.error); return; }
    loadMeetings();
  });
}

function attendMeeting(id) {
  if (!confirm("Marcar asistencia de todos los participantes?")) return;
  api("/api/meetings/" + id + "/attend", { method: "POST", body: { asistio: true } })
    .then(function () { loadMeetings(); });
}

// ------------------------------------------------------------------
// Coordinador
// ------------------------------------------------------------------
function generateWeek() {
  var week = isoWeek(new Date());
  api("/api/meetings/generate?week=" + week, { method: "POST", body: {} }).then(function (data) {
    if (data.__status === 403) { alert(data.error); return; }
    $("coordinator-output").innerHTML =
      '<p>' + (data.meetings || []).length + " reuniones generadas en " + esc(data.week) + ".</p>";
    loadMeetings();
  });
}

// ------------------------------------------------------------------
// Boot
// ------------------------------------------------------------------
function init() {
  $("login-form").addEventListener("submit", function (e) {
    e.preventDefault();
    api("/api/auth/login", {
      method: "POST",
      body: { username: $("login-username").value, password: $("login-password").value }
    }).then(function (data) {
      if (data.__status === 401) { showError(data.error); return; }
      setToken(data.token);
      showApp();
      loadAll();
    });
  });

  $("register-form").addEventListener("submit", function (e) {
    e.preventDefault();
    api("/api/auth/register", {
      method: "POST",
      body: {
        username: $("reg-username").value,
        password: $("reg-password").value,
        email: $("reg-email").value || undefined
      }
    }).then(function (data) {
      if (data.__status === 409) { showError(data.error); return; }
      if (data.__status === 400) { showError(data.error); return; }
      setToken(data.token);
      showApp();
      loadAll();
    });
  });

  $("btn-logout").addEventListener("click", function () { clearToken(); showAuth(); });

  $("btn-save-availability").addEventListener("click", function () {
    var slots = Object.keys(selectedSlots).filter(function (s) { return selectedSlots[s]; });
    api("/api/availability", {
      method: "POST",
      body: { week: $("av-week").value, slots: slots }
    }).then(function () { alert("Disponibilidad guardada."); });
  });

  $("btn-refresh-meetings").addEventListener("click", loadMeetings);
  $("btn-generate-week").addEventListener("click", generateWeek);
  $("btn-test-cancel").addEventListener("click", closeTest);
  $("btn-test-submit").addEventListener("click", submitTest);
  $("btn-evidence-cancel").addEventListener("click", closeEvidence);
  $("btn-evidence-submit").addEventListener("click", submitEvidence);
  $("tree-search").addEventListener("input", function () { loadAll(); });

  // Puerta del OEV (M12): la identidad llega por el FRAGMENTO de la URL
  // (#jwt=...), que nunca viajó al servidor (no quedó en logs). Se captura una
  // sola vez, se guarda como token federado y se limpia la URL.
  captureFederatedJwt();

  if (getToken()) { showApp(); loadAll(); }
  else { showAuth(); }
}

// ------------------------------------------------------------------
// Identidad federada desde la Maxocracia (:5001) — Una sola puerta
// ------------------------------------------------------------------
function captureFederatedJwt() {
  var m = location.hash.match(/^#jwt=([^&]+)/);
  if (!m) return;
  try {
    var jwt = decodeURIComponent(m[1]);
    if (jwt && jwt.split(".").length === 3) {
      setToken(jwt);
      history.replaceState(null, "", location.pathname + location.search);
      console.info("Identidad federada del OEV capturada (JWT de Maxocracia).");
    }
  } catch (e) {
    console.warn("Fragmento federado inválido, se ignora.", e);
  }
}

function showError(msg) {
  $("auth-error").textContent = msg || "Error";
  $("auth-error").hidden = false;
}

init();
