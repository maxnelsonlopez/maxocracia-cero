const base = `${location.protocol}//${location.host}`

const el = id => document.getElementById(id)

// Token helpers: persist token in localStorage so UI actions reuse it
function saveToken(t){
  if (!t) { localStorage.removeItem('mc_token'); el('token').textContent = '(no token)'; return }
  localStorage.setItem('mc_token', t)
  el('token').textContent = t
}

function loadToken(){
  const t = localStorage.getItem('mc_token')
  if (t) el('token').textContent = t
  return t
}

function getAuthHeaders(headers={}){
  const t = loadToken()
  if (t && t !== '(no token)') headers['Authorization'] = `Bearer ${t}`
  return headers
}

// keep decode helper for edge-cases, but prefer /auth/me
function decodeJwtPayload(token){
  try{
    const parts = token.split('.')
    if (parts.length !== 3) return null
    const payload = parts[1]
    const json = atob(payload.replace(/-/g,'+').replace(/_/g,'/'))
    return JSON.parse(decodeURIComponent(escape(json)))
  }catch(e){ return null }
}

function showProfileFromToken(){
  const token = loadToken()
  if (!token) { el('profile').textContent = '(not logged in)'; return }
  // prefer to fetch /auth/me for authoritative profile
  // prefer authoritative profile via /auth/me
  fetch(`${base}/auth/me`, {headers: getAuthHeaders({})}).then(async res => {
    if (!res.ok) {
      el('profile').textContent = '(unauthenticated)'
      return
    }
    const j = await res.json()
    const parts = []
    if (j.name) parts.push(`Name: ${j.name}`)
    if (j.id) parts.push(`ID: ${j.id}`)
    if (j.email) parts.push(`Email: ${j.email}`)
    el('profile').textContent = parts.join(' | ')
  }).catch(e => {
    el('profile').textContent = '(error fetching profile)'
  })
}

el('btnLogout').onclick = () => { saveToken(null); showProfileFromToken() }

el('btnRegister').onclick = async () => {
  const email = el('email').value
  const name = el('name').value
  const password = el('password').value
  if (!email || !password || !name) { alert('email, name and password required'); return }
  const res = await fetch(`${base}/auth/register`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email,password,name})})
  const text = await res.text()
  if (!res.ok) alert('Register failed: '+text)
  el('interchange_res').textContent = text
}

el('btnLogin').onclick = async () => {
  const email = el('email').value
  const password = el('password').value
  const res = await fetch(`${base}/auth/login`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email,password})})
  const data = await res.json()
  const token = data.token || null
  saveToken(token)
  showProfileFromToken()
}

el('btnInterchange').onclick = async () => {
  const interchange_id = el('int_id').value
  const giver_id = parseInt(el('giver_id').value||0)
  const receiver_id = parseInt(el('receiver_id').value||0)
  const uth = parseFloat(el('uth').value||0)
  const impact = parseInt(el('impact').value||0)
  const description = el('description').value
  const res = await fetch(`${base}/interchanges`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({interchange_id,giver_id,receiver_id,uth_hours:uth,impact_resolution_score:impact,description})})
  el('interchange_res').textContent = JSON.stringify(await res.json(), null, 2)
  await refreshInterchanges()
}

el('btnBalance').onclick = async () => {
  let uid = el('balance_user').value
  const token = loadToken()
  if (!uid) {
    // if logged in, prefer authenticated user id
    const dec = token ? decodeJwtPayload(token) : null
    if (dec && dec.user_id) uid = dec.user_id
  }
  if (!uid) { alert('user id required'); return }
  const headers = getAuthHeaders({})
  const res = await fetch(`${base}/maxo/${uid}/balance`, {headers})
  el('balance_res').textContent = JSON.stringify(await res.json(), null, 2)
}

el('btnTransfer').onclick = async () => {
  // If a token is present, prefer using the authenticated user as the sender
  const token = loadToken()
  const decoded = token ? decodeJwtPayload(token) : null
  const from_user = decoded && decoded.user_id ? parseInt(decoded.user_id) : parseInt(el('from_user').value||0)
  const to_user = parseInt(el('to_user').value||0)
  const amount = parseFloat(el('amount').value||0)
  const headers = getAuthHeaders({'Content-Type':'application/json'})
  try{
    const res = await fetch(`${base}/maxo/transfer`, {method:'POST', headers, body: JSON.stringify({from_user_id:from_user,to_user_id:to_user,amount,reason:'from UI'})})
    let json
    try{ json = await res.json() } catch(e){
      el('transfer_res').textContent = `Invalid response (status ${res.status})`
      return
    }
    el('transfer_res').textContent = JSON.stringify(json, null, 2)
  }catch(e){
    el('transfer_res').textContent = `Network error: ${e.message}`
  }
}

el('btnCreateRes').onclick = async () => {
  const title = el('res_title').value
  const category = el('res_cat').value
  const description = el('res_desc').value
  const token = loadToken()
  const decoded = token ? decodeJwtPayload(token) : null
  const user_id = decoded && decoded.user_id ? decoded.user_id : 1
  const headers = getAuthHeaders({'Content-Type':'application/json'})
  const body = JSON.stringify({user_id,title,category,description})
  const res = await fetch(`${base}/resources`, {method:'POST', headers, body})
  el('res_list').textContent = JSON.stringify(await res.json(), null, 2)
  await refreshResources()
}

el('btnListRes').onclick = async () => {
  const res = await fetch(`${base}/resources`)
  const data = await res.json()
  el('res_list').textContent = JSON.stringify(data, null, 2)
  const tbody = document.querySelector('#resources_table tbody')
  if (!tbody) return
  tbody.innerHTML = ''
  data.forEach(it => {
    const tr = document.createElement('tr')
    tr.innerHTML = `<td>${it.id}</td><td>${it.title}</td><td>${it.category||''}</td><td>${it.user_id||''}</td><td>${it.created_at||''}</td><td><button data-id='${it.id}' class='claim-btn'>Claim</button></td>`
    tbody.appendChild(tr)
  })
  Array.from(document.querySelectorAll('.claim-btn')).forEach(b => b.onclick = async (e)=>{
    const id = e.target.dataset.id
    const token = loadToken()
    const decoded = token ? decodeJwtPayload(token) : null
    const user_id = decoded && decoded.user_id ? decoded.user_id : 1
    const resp = await fetch(`${base}/resources/${id}/claim`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({user_id})})
    const json = await resp.json()
    alert(json.message || JSON.stringify(json))
    await refreshResources()
  })
}

async function refreshInterchanges() {
  const res = await fetch(`${base}/interchanges`)
  const data = await res.json()
  const tbody = document.querySelector('#interchanges_table tbody')
  if (!tbody) return
  tbody.innerHTML = ''
  data.slice(0,20).forEach(it => {
    const tr = document.createElement('tr')
    tr.innerHTML = `<td>${it.interchange_id||it.id}</td><td>${it.giver_id}</td><td>${it.receiver_id}</td><td>${it.uth_hours||''}</td><td>${it.impact_resolution_score||''}</td><td>${it.created_at||''}</td>`
    tbody.appendChild(tr)
  })
}

async function refreshResources(){
  const res = await fetch(`${base}/resources`)
  const data = await res.json()
  const tbody = document.querySelector('#resources_table tbody')
  if (!tbody) return
  tbody.innerHTML = ''
  data.forEach(it => {
    const tr = document.createElement('tr')
    tr.innerHTML = `<td>${it.id}</td><td>${it.title}</td><td>${it.category||''}</td><td>${it.user_id||''}</td><td>${it.created_at||''}</td><td><button data-id='${it.id}' class='claim-btn'>Claim</button></td>`
    tbody.appendChild(tr)
  })
  Array.from(document.querySelectorAll('.claim-btn')).forEach(b => b.onclick = async (e)=>{
    const id = e.target.dataset.id
    const token = loadToken()
    const decoded = token ? decodeJwtPayload(token) : null
    const user_id = decoded && decoded.user_id ? decoded.user_id : 1
    const resp = await fetch(`${base}/resources/${id}/claim`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({user_id})})
    const json = await resp.json()
    alert(json.message || JSON.stringify(json))
    await refreshResources()
  })
}

// initial load
refreshInterchanges()
refreshResources()
showProfileFromToken()
