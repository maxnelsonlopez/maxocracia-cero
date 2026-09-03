# Lente educativa SearXNG (opcional, B1)

El buscador de la Plataforma Educativa funciona **sin SearXNG** (las capas
semillas + Zenodo + Wayback no lo necesitan). Esta carpeta es el artefacto
opcional para la **capa web general**: una instancia SearXNG auto-hospedada
con nuestra lente educativa, que además puede federar las semillas del
buscador como uno de sus motores (gracias a `?format=searx`).

## Instalación (opcional, $0)

```powershell
docker run -d --name searxng -p 8888:8080 `
  -v "${PWD}\searxng:/etc/searxng" searxng/searxng:latest
# luego, en la plataforma educativa:
$env:BUSCADOR_SEARXNG_URL = "http://127.0.0.1:8888"
python run.py
```

`settings.maxocracia.yml` es el fragmento de configuración: mezclalo en el
`settings.yml` de tu instancia (bloque `engines:` + `search.formats` con
`json` habilitado para la API interna).

## Qué hace la lente

1. **Motores de ads fuera**: se desactivan los motores que devuelven
   resultados comerciales/promocionales.
2. **Motores independientes dentro**: Marginalia, Mojeek, wiby y Wikipedia
   (los índices no comerciales del estado del arte).
3. **Semillas federadas**: el motor `maxocracia-semillas` consulta la API del
   buscador de esta plataforma (`/api/buscador?format=searx`), de modo que
   cualquier instancia SearXNG del mundo puede agregar nuestras semillas
   verificadas a su lente educativa (el tejido forkable, en vivo).

## Variables de entorno (en la plataforma, no en SearXNG)

| Variable | Por defecto | Qué hace |
|---|---|---|
| `BUSCADOR_SEARXNG_URL` | (vacía = capa desactivada) | URL base de la instancia (ej. `http://127.0.0.1:8888`) |
| `BUSCADOR_UPSTREAM_TIMEOUT` | `6` | Timeout de todos los motores aguas arriba (segundos) |
| `BUSCADOR_ZENODO_SIZE` | `5` | Resultados por consulta a la API de Zenodo |

Fail-open: sin SearXNG, la búsqueda sigue funcionando (semillas + Zenodo);
con SearXNG caído, la capa web se reporta en `motores_fail_open`.
