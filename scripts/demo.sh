#!/usr/bin/env bash
set -euo pipefail

PORT=${PORT:-5001}
BASE="http://127.0.0.1:${PORT}"

echo "Using base: $BASE"

# helper to pretty print json when jq available
jj(){ if command -v jq >/dev/null 2>&1; then jq -C .; else python3 -m json.tool || cat; fi }

# 1) Register two users: alice and bob
curl -s -X POST "$BASE/auth/register" -H 'Content-Type: application/json' -d '{"email":"alice@example.test","password":"password1","name":"Alice"}' | jj
curl -s -X POST "$BASE/auth/register" -H 'Content-Type: application/json' -d '{"email":"bob@example.test","password":"password2","name":"Bob"}' | jj

# 2) Login as Alice and capture token
ALICE_TOKEN=$(curl -s -X POST "$BASE/auth/login" -H 'Content-Type: application/json' -d '{"email":"alice@example.test","password":"password1"}' | jq -r '.token')
echo "Alice token: ${ALICE_TOKEN}" | sed 's/.*/[REDACTED TOKEN]/'

# 3) Login as Bob (for later)
BOB_TOKEN=$(curl -s -X POST "$BASE/auth/login" -H 'Content-Type: application/json' -d '{"email":"bob@example.test","password":"password2"}' | jq -r '.token')

# 4) Create an interchange where Alice is the giver (this will credit Alice automatically)
curl -s -X POST "$BASE/interchanges" -H 'Content-Type: application/json' -d '{"interchange_id":"DEMO-INT-001","giver_id":1,"receiver_id":2,"description":"Helping set up a vegetable garden","uth_hours":3.0,"impact_resolution_score":4}' | jj

# 5) Check interchanges
curl -s "$BASE/interchanges" | jj

# 6) Check Alice's balance
curl -s "$BASE/maxo/1/balance" -H "Authorization: Bearer ${ALICE_TOKEN}" | jj

# 7) Transfer from Alice to Bob (Alice must have enough balance from the interchange credit)
curl -s -X POST "$BASE/maxo/transfer" -H 'Content-Type: application/json' -H "Authorization: Bearer ${ALICE_TOKEN}" -d '{"from_user_id":1,"to_user_id":2,"amount":2.0,"reason":"Thanks for help"}' | jj

# 8) Check both balances
echo "Alice balance:"; curl -s "$BASE/maxo/1/balance" -H "Authorization: Bearer ${ALICE_TOKEN}" | jj
echo "Bob balance:"; curl -s "$BASE/maxo/2/balance" -H "Authorization: Bearer ${BOB_TOKEN}" | jj

# 9) Create a resource as Alice
curl -s -X POST "$BASE/resources" -H 'Content-Type: application/json' -H "Authorization: Bearer ${ALICE_TOKEN}" -d '{"user_id":1,"title":"Ladder","description":"A 3m ladder","category":"tools"}' | jj

# 10) List resources
curl -s "$BASE/resources" | jj

# 11) Claim the resource as Bob
# get resource id
RID=$(curl -s "$BASE/resources" | jq '.[0].id')
echo "Claiming resource id: $RID"
curl -s -X POST "$BASE/resources/${RID}/claim" -H 'Content-Type: application/json' -d '{"user_id":2}' | jj

# 12) Add a reputation review for Bob
curl -s -X POST "$BASE/reputation/review" -H 'Content-Type: application/json' -d '{"user_id":2,"score":4.5}' | jj

# 13) Check Bob reputation
curl -s "$BASE/reputation/2" | jj

echo "Demo complete."
