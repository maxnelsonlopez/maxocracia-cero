# Despliegue por comunidad — una casa por tejido

**Idea:** sistema común, gobierno independiente. Cada comunidad corre su
propia instancia con su propia base de datos (`comun.db`) y su propia
`SECRET_KEY`: mismo plano, distinta llave y distinto libro. No hay
federación entre instancias (pendiente de diseño): la plaza de cada casa
es soberana.

## 1. Requisitos

- Python 3.11+, Node 22, un servidor o PC siempre encendido.
- Un dominio o IP pública + proxy TLS (Caddy o nginx): el TLS lo termina
  el proxy, nunca waitress.

## 2. Backend (una instancia por comunidad)

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
copy config.example.env .env
```

En `.env` (obligatorio en producción, `run.py` y `create_app()` abortan
sin esto):

```ini
SECRET_KEY=<openssl rand -hex 32>
FLASK_ENV=production
PORT=5001
FORCE_HTTPS=1
```

Sin `DEEPSEEK_API_KEY` el oráculo degrada elegante (la negociación sigue
con plantillas; `analyze` responde 503 informativo). El Concilio solo
despierta si se instala su tarea (`scripts/instalar_arranque_concilio.py`):
para el piloto, **no instalarla**.

Arranque:

```powershell
.venv\Scripts\python.exe run.py   # waitress en 0.0.0.0:5001
```

## 3. Frontend (apunta a la casa y congela)

```powershell
cd frontend
$env:NEXT_PUBLIC_API_URL="https://tu-servidor"
npm ci; npm run build
cd ..
.venv\Scripts\python.exe scripts/build_front.py  # out/ -> app/static/dist/
```

La URL queda embebida en el JS: cambiar de servidor exige rebuild.
Flask sirve `app/static/dist/` y resuelve las rutas dinámicas
(`/contracts/<id>` vía alias a placeholder, RSC y shells de página).

## 4. Primeros pasos del tejido (facilitador)

1. Registra al facilitador y hazlo admin:
   `.venv\Scripts\python.exe scripts/migrate_add_admin_role.py`.
2. Crea el primer hogar en `/micromax` y reparte su `invite_code` (6 letras,
   a mano o dictado: es corto a propósito).
3. Cada vecino: `/register` → `/forms/cero` (basta **una** vía de contacto:
   llamada, WhatsApp o Telegram) → publica necesidad y oferta en `/matching`.
   **Modo facilitador**: acompaña desde tu celular con el link
   `/register?referred_by=<tu-alias>` — el referido viaja solo al Form Cero
   ("¿Quién te invitó?") y el tejido queda trazado desde la primera llegada.
4. Del match al acuerdo: botón "Contrato Ético" → el borrador vive en
   `/contracts/<id>` → aceptar → activar → check-ins semanales.
5. Lee `docs/guides/GUIA_FACILITADOR.md` y `docs/guides/semana_de_la_verdad.md`
   (n=1 de 7 días habitando el sistema antes de reclutar).

## 5. Cuidado de la casa

- **Copia de seguridad:** `comun.db` es un archivo. Cópialo cada noche a
  otro disco; para restaurarlo basta reemplazarlo con el servidor apagado.
- **Secretos:** `.env` jamás va a git (ya está ignorado). Si una
  `SECRET_KEY` se filtra, rota y todos vuelven a entrar.
- **Límites honestos:** SQLite sostiene una comunidad (decenas de personas)
  en un solo nodo. PostgreSQL/Redis están en el roadmap a 30-90 días
  (`docs/architecture/PLAN_ENDURECIMIENTO_SEGURIDAD.md`).
- **Votos:** la gobernanza plena (N1) llega tras el primer contrato activo;
  en un piloto de días, el facilitador custodia y la plaza propone.
