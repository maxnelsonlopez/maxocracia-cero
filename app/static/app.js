const el = id => document.getElementById(id)

let currentUser = null

async function showProfileFromToken() {
  const profile = await api.getProfile();
  if (!profile) {
    currentUser = null;
    el('profile').textContent = '(not logged in)';
    el('token').textContent = '(no token)';
    return;
  }

  currentUser = profile;
  el('token').textContent = api.getToken();

  const parts = []
  if (profile.name) parts.push(`Name: ${profile.name}`)
  if (profile.id) parts.push(`ID: ${profile.id}`)
  if (profile.email) parts.push(`Email: ${profile.email}`)
  el('profile').textContent = parts.join(' | ')
}

el('btnLogout').onclick = () => {
  api.logout();
  showProfileFromToken();
}

el('btnRegister').onclick = async () => {
  const email = el('email').value
  const name = el('name').value
  const password = el('password').value
  if (!email || !password || !name) { alert('email, name and password required'); return }

  const { ok, data } = await api.register(name, email, password);
  if (!ok) {
    alert('Register failed: ' + (data.error || 'Unknown error'));
    el('interchange_res').textContent = JSON.stringify(data);
  } else {
    showProfileFromToken();
    el('interchange_res').textContent = 'Registered successfully';
  }
}

el('btnLogin').onclick = async () => {
  const email = el('email').value
  const password = el('password').value

  const { ok, data } = await api.login(email, password);
  if (!ok) {
    alert('Login failed: ' + (data.error || 'Unknown error'));
  } else {
    showProfileFromToken();
  }
}

el('btnInterchange').onclick = async () => {
  const interchange_id = el('int_id').value
  const giver_id = parseInt(el('giver_id').value || 0)
  const receiver_id = parseInt(el('receiver_id').value || 0)
  const uth = parseFloat(el('uth').value || 0)
  const impact = parseInt(el('impact').value || 0)
  const description = el('description').value

  const res = await api.request('/interchanges', {
    method: 'POST',
    body: JSON.stringify({ interchange_id, giver_id, receiver_id, uth_hours: uth, impact_resolution_score: impact, description })
  });

  el('interchange_res').textContent = JSON.stringify(await res.json(), null, 2)
  await refreshInterchanges()
}

el('btnBalance').onclick = async () => {
  let uid = el('balance_user').value
  if (!uid) {
    if (currentUser && currentUser.id) uid = currentUser.id
  }
  if (!uid) { alert('user id required'); return }

  const res = await api.request(`/maxo/${uid}/balance`);
  el('balance_res').textContent = JSON.stringify(await res.json(), null, 2)
}

el('btnTransfer').onclick = async () => {
  const from_user = currentUser && currentUser.id ? parseInt(currentUser.id) : parseInt(el('from_user').value || 0)
  const to_user = parseInt(el('to_user').value || 0)
  const amount = parseFloat(el('amount').value || 0)

  try {
    const res = await api.request('/maxo/transfer', {
      method: 'POST',
      body: JSON.stringify({ from_user_id: from_user, to_user_id: to_user, amount, reason: 'from UI' })
    });

    let json
    try { json = await res.json() } catch (e) {
      el('transfer_res').textContent = `Invalid response (status ${res.status})`
      return
    }
    el('transfer_res').textContent = JSON.stringify(json, null, 2)
  } catch (e) {
    el('transfer_res').textContent = `Network error: ${e.message}`
  }
}

el('btnCreateRes').onclick = async () => {
  const title = el('res_title').value
  const category = el('res_cat').value
  const description = el('res_desc').value
  const user_id = currentUser && currentUser.id ? currentUser.id : 1

  const res = await api.request('/resources', {
    method: 'POST',
    body: JSON.stringify({ user_id, title, category, description })
  });

  el('res_list').textContent = JSON.stringify(await res.json(), null, 2)
  await refreshResources()
}

el('btnListRes').onclick = async () => {
  const res = await api.request('/resources');
  const data = await res.json()
  el('res_list').textContent = JSON.stringify(data, null, 2)
  renderResourcesTable(data);
}

async function refreshInterchanges() {
  const res = await api.request('/interchanges');
  const data = await res.json()
  const tbody = document.querySelector('#interchanges_table tbody')
  if (!tbody) return
  tbody.innerHTML = ''
  data.slice(0, 20).forEach(it => {
    const tr = document.createElement('tr')
    tr.innerHTML = `<td>${it.interchange_id || it.id}</td><td>${it.giver_id}</td><td>${it.receiver_id}</td><td>${it.uth_hours || ''}</td><td>${it.impact_resolution_score || ''}</td><td>${it.created_at || ''}</td>`
    tbody.appendChild(tr)
  })
}

async function refreshResources() {
  const res = await api.request('/resources');
  const data = await res.json()
  renderResourcesTable(data);
}

function renderResourcesTable(data) {
  const tbody = document.querySelector('#resources_table tbody')
  if (!tbody) return
  tbody.innerHTML = ''
  data.forEach(it => {
    const tr = document.createElement('tr')
    tr.innerHTML = `<td>${it.id}</td><td>${it.title}</td><td>${it.category || ''}</td><td>${it.user_id || ''}</td><td>${it.created_at || ''}</td><td><button data-id='${it.id}' class='claim-btn'>Claim</button></td>`
    tbody.appendChild(tr)
  })

  Array.from(document.querySelectorAll('.claim-btn')).forEach(b => b.onclick = async (e) => {
    const id = e.target.dataset.id
    const user_id = currentUser && currentUser.id ? currentUser.id : 1

    const resp = await api.request(`/resources/${id}/claim`, {
      method: 'POST',
      body: JSON.stringify({ user_id })
    });

    const json = await resp.json()
    alert(json.message || JSON.stringify(json))
    await refreshResources()
  })
}

// initial load
refreshInterchanges()
refreshResources()
showProfileFromToken()
