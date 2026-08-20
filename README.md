# 📊 Historial de Tráfico Acumulado — Bóveda del Gato Negro

Herramienta automatizada para recolectar, almacenar y visualizar el tráfico histórico de repositorios GitHub, rompiendo el límite nativo de 14 días.

## 🌐 Demo en vivo

👉 [https://pablosnchz.github.io/github-repo-traffic-stats/](https://pablosnchz.github.io/github-repo-traffic-stats/)

## 🚀 ¿Qué hace este proyecto?

Este sistema nació con un objetivo claro: **evitar que GitHub borre las estadísticas de tráfico cada 14 días**.

| Funcionalidad | Descripción |
|---------------|-------------|
| ✅ Recolección diaria | Consulta la API de GitHub cada 24h vía GitHub Actions |
| ✅ Almacenamiento permanente | Guarda los datos en CSV dentro del repo |
| ✅ Visualización dinámica | Gráficos interactivos con Chart.js en el navegador |
| ✅ Datos históricos | Hardcode de datos feb-ago 2026 + CSV en vivo |
| ✅ Estilo unificado | Diseño consistente con la Bóveda del Gato Negro |

## 📈 Proyectos monitoreados

| Repositorio | Descripción |
|-------------|-------------|
| `PabloSnchz/gw2-wallet-ligero` | WebApp para Guild Wars 2: Cartera, MetaEventos, Cámara del Brujo, Raids y más |

## 🛠️ Tecnologías utilizadas

| Componente | Tecnología |
|------------|------------|
| Recolección | Python (query_github_traffic_data.py) |
| Automatización | GitHub Actions (diario 23:30 UTC) |
| Visualización | Chart.js (CDN) en el navegador |
| Datos históricos | Hardcode en HTML + CSV de GitHub |
| Hosting | GitHub Pages |

## 📂 Estructura del proyecto

| Archivo / Carpeta | Descripción |
|-------------------|-------------|
| `.github/workflows/` | Workflows de GitHub Actions |
| `data/github_views/` | CSV con vistas por repo |
| `data/github_clones/` | CSV con clones por repo |
| `data/github_paths/` | CSV con rutas de tráfico |
| `preview_plots/` | Gráficos `.webp` (legacy) |
| `index.html` | Dashboard interactivo con Chart.js |
| `query_github_traffic_data.py` | Script de recolección |
| `create_preview_plots.py` | Script legacy de gráficos |

## 🧠 ¿Cómo funciona?

| Paso | Descripción |
|------|-------------|
| 1 | **GitHub Actions** ejecuta el workflow `query_data.yml` diariamente |
| 2 | El script Python consulta la API de GitHub (últimos 14 días) |
| 3 | Los datos se guardan en CSV (`data/github_views/`, `data/github_clones/`) |
| 4 | El `index.html` carga los CSV y los combina con el histórico hardcodeado |
| 5 | Chart.js renderiza los gráficos dinámicamente |
| 6 | GitHub Pages despliega los cambios automáticamente |

## 📊 Dashboard público

El dashboard incluye:

| Sección | Contenido |
|---------|-----------|
| **KPIs** | Vistas totales, únicos, clones, clonadores |
| **Vistas diarias** | Gráfico de línea con visitas y usuarios únicos |
| **Clones diarios** | Gráfico de línea con clones y clonadores únicos |
| **Estado** | Badges de conexión con GitHub y actualización |
| **Promedios** | Vista diaria promedio de vistas y clones |

### 🔌 Conexión con GitHub

El panel muestra un badge que indica:
- ✅ **Conectado** — si el CSV de GitHub carga correctamente
- ⚠️ **Sin datos recientes** — si solo muestra el histórico hardcodeado

### 📈 Datos históricos

| Período | Clones/semana |
|---------|---------------|
| Febrero → Abril 2026 | ~450 |
| Mayo → Junio 2026 | ~225 |
| Julio → Agosto 2026 | ~100 |

**Total histórico estimado:**
- Vistas: ~25.000
- Visitantes únicos: ~1.500
- Clones: ~7.000
- Clonadores únicos: ~800

## 📜 Licencia

MIT — mismo que la Bóveda del Gato Negro.

## 🐈‍⬛ Proyectos relacionados

| Proyecto | Enlace |
|----------|--------|
| Bóveda del Gato Negro (WebApp) | [github.com/PabloSnchz/gw2-wallet-ligero](https://github.com/PabloSnchz/gw2-wallet-ligero) |
| Link in Bio | [pablosnchz.github.io/bio](https://pablosnchz.github.io/bio/) |
| Métricas GA4 | [pablosnchz.github.io/gw2-metrics-dashboard](https://pablosnchz.github.io/gw2-metrics-dashboard/) |

---

Hecho con ❤️ para la comunidad · Bóveda del Gato Negro
