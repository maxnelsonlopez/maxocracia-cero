const base = `${location.protocol}//${location.host}`

const el = id => document.getElementById(id)

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
  el('token').textContent = data.token || '(no token)'
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
}

el('btnBalance').onclick = async () => {
  const uid = el('balance_user').value
  const token = el('token').textContent
  if (!uid) { alert('user id required'); return }
  const headers = token && token !== '(no token)' ? {'Authorization': `Bearer ${token}`} : {}
  const res = await fetch(`${base}/maxo/${uid}/balance`, {headers})
  el('balance_res').textContent = JSON.stringify(await res.json(), null, 2)
}

el('btnTransfer').onclick = async () => {
  const from_user = parseInt(el('from_user').value||0)
  const to_user = parseInt(el('to_user').value||0)
  const amount = parseFloat(el('amount').value||0)
  const token = el('token').textContent
  const headers = {'Content-Type':'application/json'}
  if (token && token !== '(no token)') headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${base}/maxo/transfer`, {method:'POST', headers, body: JSON.stringify({from_user_id:from_user,to_user_id:to_user,amount,reason:'from UI'})})
  el('transfer_res').textContent = JSON.stringify(await res.json(), null, 2)
}

el('btnCreateRes').onclick = async () => {
  const title = el('res_title').value
  const category = el('res_cat').value
  const description = el('res_desc').value
  const token = el('token').textContent
  const headers = {'Content-Type':'application/json'}
  if (token && token !== '(no token)') headers['Authorization'] = `Bearer ${token}`
  const body = JSON.stringify({user_id:1,title,category,description})
  const res = await fetch(`${base}/resources`, {method:'POST', headers, body})
  el('res_list').textContent = JSON.stringify(await res.json(), null, 2)
}

el('btnListRes').onclick = async () => {
  const res = await fetch(`${base}/resources`)
  el('res_list').textContent = JSON.stringify(await res.json(), null, 2)
}
