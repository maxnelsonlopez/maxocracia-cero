# Guía de Arquitectura Frontend: Maxocracia Unificada

Este documento sirve como manual técnico para entender, mantener y expandir el frontend de la Maxocracia tras la migración a **Next.js 15** e integración con **Flask**.

## 🏗️ Estructura del Repositorio

El proyecto opera bajo una arquitectura híbrida:

1.  **Backend (`/app`)**: Servidor Flask que maneja la lógica de negocio, base de datos (SQLite) y autenticación JWT.
2.  **Frontend (`/frontend`)**: Aplicación Next.js 15 (App Router) que contiene toda la interfaz de usuario moderna.
3.  **Puente (`/app/static/dist`)**: Carpeta donde se aloja el build estático del frontend para que Flask lo sirva en producción.

## 🚀 Flujo de Desarrollo e Integración

### 1. Desarrollo Local
Para trabajar en el frontend con hot-reload:
```bash
cd frontend
npm run dev
```
*Nota: Asegúrate de que el backend de Flask esté corriendo (`python run.py`) para que las llamadas a la API funcionen.*

### 2. Sincronización con Producción
Cuando los cambios en `/frontend` estén listos, deben "compilarse" hacia el servidor Flask:
```bash
python scripts/build_front.py
```
Este script:
1.  Limpia la carpeta `app/static/dist`.
2.  Ejecuta `npm run build` en la carpeta frontend.
3.  Mueve los archivos generados a la ubicación correcta en el backend.

## ➕ Cómo agregar una Nueva Sección

Para añadir una nueva funcionalidad (ej: una sección de "Gobernanza"):

### Paso 1: Crear la Ruta en Next.js
Crea una carpeta en `frontend/app/` con el nombre de la sección y un archivo `page.tsx`.
*   Ejemplo: `frontend/app/governance/page.tsx`.

### Paso 2: Usar el Design System
Importa los componentes base para mantener la estética Glassmorphism:
```tsx
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
// ...
```

### Paso 3: Conectar con la API
Usa el wrapper de API centralizado para peticiones al backend:
```tsx
import { apiFetch } from "@/lib/api";

const data = await apiFetch("/governance/stats");
```

### Paso 4: Actualizar la Navegación Global
Modifica `frontend/app/components/Navigation.tsx` para añadir el link en el sidebar o el menú desplegable.

### Paso 5: Desplegar
Ejecuta `python scripts/build_front.py` para que la nueva ruta sea accesible desde el dominio principal.

## 🛠️ Cómo actualizar secciones existentes

*   **Lógica de Negocio**: Si necesitas cambiar cómo se calcula algo, busca en `frontend/lib/logic/` o en los controladores del backend (`app/vhv_bp.py`, etc.).
*   **Diseño/Estilos**: La configuración global de Tailwind CSS v4 está en `frontend/app/globals.css`. Los componentes individuales usan clases de Tailwind.
*   **Textos/Traducciones**: Actualmente los textos están hardcoded en los componentes de React.

## 📋 Información Relevante

*   **Autenticación**: El frontend maneja tokens JWT almacenados en `localStorage` bajo la clave **`mc_access_token`** (¡no usar `mc_token`, esa clave no existe!). El componente `AuthContext` gestiona el estado de sesión.
    *   **Regla de Oro**: **Usar siempre `apiFetch` de `@/lib/api`** para cualquier petición al backend. Este wrapper inyecta automáticamente el header `Authorization: Bearer <mc_access_token>`. Nunca usar `fetch()` directo con headers manuales en páginas de admin — es la causa raíz de los fallos de autenticación intermitentes.
*   **Visualizaciones**: Usamos `chart.js` y `react-chartjs-2`. Para grafos de red, usamos `react-flow`.
*   **Rutas SPA**: Flask está configurado con un "catch-all" en `app/__init__.py` que redirige cualquier ruta no encontrada al `index.html` de Next.js, permitiendo que el App Router de Next maneje la navegación.

*   **Auditoría y Estabilización (19 de Mayo de 2026)**: Se saneó el 100% del tipado explícito `any` en los componentes del panel de administración (`/admin/dashboard`, `/admin/sdv`, `/admin/reports`, `/admin/network`, `/admin/users`), reemplazándolos con interfaces TypeScript robustas. También se solucionaron problemas de re-renderizado circular en cascada de React 19 y se crearon placeholders interactivos y dinámicos para configuración y suscripciones.

---
*Documento actualizado y estabilizado por Antigravity (Gemini AI Assistant - Google DeepMind) tras la auditoría integral de Mayo 2026.*
