# Guía de Despliegue en Producción (Cloudflare Tunnels + Windows)

Esta guía te ayudará a exponer tu servidor local (ejecutándose en Windows) a tu nuevo dominio de Cloudflare de forma **segura, cifrada y sin abrir puertos en tu router** (sin *Port Forwarding*).

## ¿Por qué Cloudflare Tunnels?
Al usar un túnel de Cloudflare (`cloudflared`), tu servidor inicia una conexión segura *de salida* hacia la red global de Cloudflare. El tráfico que va a tu dominio entra por los servidores de Cloudflare y baja por ese túnel hasta tu aplicación local. Esto oculta tu dirección IP pública, evita ataques DDoS directos a tu red y te otorga certificados SSL (HTTPS) gratuitos.

## Paso 1: Configurar el dominio en Cloudflare
1. Entra a tu panel de [Cloudflare](https://dash.cloudflare.com).
2. Asegúrate de que el dominio que compraste está activo.
3. No necesitas configurar los registros DNS manualmente (A o CNAME) para el servidor, el túnel lo hará por ti.

## Paso 2: Crear el Túnel en Zero Trust
1. En el panel lateral izquierdo de Cloudflare, ve a **Zero Trust**.
2. Ve a **Networks** -> **Tunnels**.
3. Haz clic en **Create a tunnel**.
4. Selecciona **Cloudflared** y haz clic en Next.
5. Dale un nombre (ej. `maxocracia-server`) y guarda.

## Paso 3: Instalar el Conector en Windows
Cloudflare te mostrará una pantalla con instrucciones de instalación para tu sistema operativo.
1. Selecciona el entorno **Windows**.
2. Copia y ejecuta el comando que te dan en un terminal de PowerShell (abierto como Administrador). Será algo así:
   ```powershell
   cloudflared.exe service install eyJh... (un token muy largo)
   ```
3. Esto instalará el servicio en segundo plano. En la web de Cloudflare, verás que el estado cambia a **Connected** en unos segundos. Haz clic en Next.

## Paso 4: Configurar el Enrutamiento (Public Hostname)
Ahora le diremos a Cloudflare qué subdominio apuntará a tu servidor local.
1. **Public Hostname Page**:
   - **Subdomain**: Déjalo vacío si quieres usar `tudominio.com` o escribe `app` si quieres usar `app.tudominio.com`.
   - **Domain**: Selecciona el dominio que compraste en el desplegable.
2. **Service**:
   - **Type**: Selecciona `HTTP`.
   - **URL**: Escribe `localhost:5001`.
3. Guarda el hostname (Save).

## Paso 5: Iniciar tu Servidor en Producción
Asegúrate de que en el archivo `.env` de la raíz del proyecto tienes:
```env
FLASK_ENV=production
PORT=5001
FRONTEND_URL=https://tudominio.com
```

Inicia el servidor normalmente:
```bash
python run.py
```
Verás que el mensaje indica: `Iniciando servidor de PRODUCCIÓN con Waitress en el puerto 5001...`

## ¡Listo!
Entra a `https://tudominio.com` (o el subdominio que configuraste). El tráfico llegará seguro hasta tu máquina mediante HTTPS oficial provisto por Cloudflare.
