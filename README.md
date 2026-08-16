# 📊 Historial de Tráfico Acumulado — Bóveda del Gato Negro

> Herramienta automatizada para recolectar, almacenar y visualizar el tráfico histórico de repositorios GitHub, **rompiendo el límite nativo de 14 días**.

---

## 🌐 Demo en vivo

Puedes ver el dashboard completamente funcional aquí:  
👉 **[https://pablosnchz.github.io/github-repo-traffic-stats/](https://pablosnchz.github.io/github-repo-traffic-stats/)**

---

## 🚀 ¿Qué hace este proyecto?

Este sistema nació con un objetivo claro: **evitar que GitHub borre las estadísticas de tráfico cada 14 días**.

- ✅ **Recolecta diariamente** las métricas de visitas (`views`) y clones (`clones`) mediante GitHub Actions.
- ✅ **Almacena los datos** de forma permanente en archivos CSV dentro del propio repositorio.
- ✅ **Genera gráficos** en formato `.webp` con fondo oscuro y estilo visual idéntico a la **Bóveda del Gato Negro**.
- ✅ **Despliega un dashboard público** con diseño oscuro, explicaciones en español y métricas acumulativas.

---

## 📈 Proyectos monitoreados actualmente

| Repositorio | Descripción |
|-------------|-------------|
| [`PabloSnchz/gw2-wallet-ligero`](https://github.com/PabloSnchz/gw2-wallet-ligero) | WebApp para Guild Wars 2: Cartera, MetaEventos, Cámara del Brujo, Raids y más. |

---

## 🛠️ Tecnologías utilizadas

- **Python** (Pandas + Matplotlib) → Procesamiento de datos y generación de gráficos.
- **GitHub Actions** → Ejecución diaria automatizada del script.
- **GitHub Pages** → Alojamiento del dashboard público.
- **HTML + CSS** → Interfaz visual con estilo oscuro unificado.

---

## 📂 Estructura del proyecto

- `github-repo-traffic-stats/` (Carpeta raíz)
  - `.github/workflows/` → Workflows de GitHub Actions.
  - `data/` → Archivos CSV con el histórico acumulado.
  - `preview_plots/` → Gráficos generados diariamente (.webp).
  - `index.html` → Dashboard público (GitHub Pages).
  - `create_preview_plots.py` → Script principal de Python.
  - `query_github_traffic.py` → Consulta a la API de GitHub.
  - `README.md` → Este archivo.

---

## 🧠 ¿Cómo funciona?

1. El workflow `Query GitHub Traffic Data` se ejecuta diariamente (23:30 UTC).
2. Consulta la API de GitHub y obtiene los últimos 14 días de tráfico.
3. El workflow `Update Preview Plots` ejecuta el script Python, que:
   - Fusiona los nuevos datos con el histórico acumulado.
   - Limpia duplicados y genera gráficos.
4. Los archivos `.webp` y el `index.html` se actualizan automáticamente.
5. GitHub Pages despliega los cambios en tiempo real.

---

## 📊 Dashboard público

El dashboard incluye dos secciones principales:

- **Vistas diarias:** Muestra la evolución de visitas y usuarios únicos.  
- **Clones diarios:** Muestra la evolución de clones y clonadores únicos.

Cada gráfico cuenta con una **descripción explicativa** en español y sigue el diseño visual de la **Bóveda del Gato Negro**.

👉 **[Ver el dashboard en vivo](https://pablosnchz.github.io/github-repo-traffic-stats/)**

---

## 📜 Licencia

Este proyecto está bajo la licencia **MIT**.  
Puedes usarlo, modificarlo y adaptarlo libremente.

---

## 🐈‍⬛ Proyecto relacionado

Este sistema de métricas forma parte del ecosistema de la **Bóveda del Gato Negro**:

- [Repositorio principal (WebApp GW2)](https://github.com/PabloSnchz/gw2-wallet-ligero)
- [Link in Bio (Instagram / Redes)](https://pablosnchz.github.io/bio/)

---

*Hecho con ❤️ para la comunidad · Bóveda del Gato Negro*
