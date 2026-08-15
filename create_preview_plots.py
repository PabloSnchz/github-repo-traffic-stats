import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
from datetime import datetime, timedelta
import os

def create_plot(df, title, filename):
    # 1. Asegurar formato de fecha pura y limpiar duplicados del origen de inmediato
    df.index = pd.to_datetime(df.index).date
    df = df[~df.index.duplicated(keep='last')]
    
    if df.empty:
        return
        
    first_day = df.index.min()
    last_day = df.index.max()
    
    if first_day == last_day:
        first_day = first_day - timedelta(days=7)

    # add zeros if there is no value 
    date_range = pd.date_range(start=first_day, end=last_day, freq='D').date
    df_full = pd.DataFrame(index=date_range, columns=df.columns).fillna(0)
    
    df_full.index = pd.to_datetime(df_full.index).date
    df_full = df_full[~df_full.index.duplicated(keep='last')]
    
    df_full.update(df)
    
    total_views = df_full["count"].sum()
    total_uniques = df_full["uniques"].sum()
    
    plt.figure(figsize=(12, 6))
    plt.plot(df_full.index, df_full["count"], label="Views", color='blue')
    plt.plot(df_full.index, df_full["uniques"], label="Unique Visitors", color='red')
    
    plt.title(f"{title} ({total_views} Views, {total_uniques} Unique Visitors)")
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.legend()
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(filename, dpi=100, bbox_inches='tight', format='webp')
    plt.close()

def main():
    with open('github_username.txt', 'r') as file:
        owner = file.read().strip()

    data_dir = 'data/github_views'
    plots_dir = 'preview_plots'
    os.makedirs(plots_dir, exist_ok=True)

    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith('.csv'):
            repo = filename[:-4]
            
            views_df = pd.read_csv(os.path.join(data_dir, filename), parse_dates=['date'])
            views_df.set_index('date', inplace=True)
            
            plot_filename = f'{plots_dir}/{repo}.webp'
            create_plot(views_df, f'{owner}/{repo}', plot_filename)
            print(f"Created plot for {owner}/{repo}")

    # --- GENERACIÓN DINÁMICA DE CAJAS EN ESPAÑOL ---
    cards_html = ""
    
    # Escanear la carpeta de gráficos para renderizar de manera automática todas las cajas existentes
    if os.path.exists(plots_dir):
        for plot_file in sorted(os.listdir(plots_dir)):
            if plot_file.endswith('.webp'):
                # Identificar dinámicamente si es gráfico de Visitas o de Clones
                tipo_grafico = "Clonaciones y Descargas" if "clones" in plot_file.lower() else "Visitas y Tráfico Web"
                repo_name = plot_file.replace('.webp', '').replace('_clones', '')
                
                # Definir la explicación en español según el tipo de gráfico detectado
                if "clones" in plot_file.lower():
                    descripcion = f"Este panel detalla el volumen histórico de descargas y clones locales del repositorio <strong>{repo_name}</strong>. Permite evaluar cuántos desarrolladores están interactuando activamente con el código base en sus entornos de trabajo locales tras descubrir el proyecto."
                else:
                    descripcion = f"Este panel consolida el comportamiento histórico de la comunidad en tu repositorio <strong>{repo_name}</strong>. La línea azul refleja las vistas totales acumuladas y la línea roja muestra a los usuarios únicos semanales."

                cards_html += f"""
        <div class="card">
            <h2>Repositorio: {repo_name} ({tipo_grafico})</h2>
            <img class="plot-img" src="{plots_dir}/{plot_file}" alt="Gráfico {plot_file}">
            <div class="description-box">
                <h3>¿Qué muestra este gráfico?</h3>
                <p>{descripcion}</p>
            </div>
        </div>
                """

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estadísticas Históricas de Tráfico - GitHub</title>
    <style>
        :root {{
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --text-color: #c9d1d9;
            --text-muted: #8b949e;
            --accent-color: #58a6ff;
            --border-color: #30363d;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        header {{
            text-align: center;
            margin-bottom: 40px;
            max-width: 800px;
        }}
        h1 {{
            color: #fff;
            margin-bottom: 10px;
        }}
        p.subtitle {{
            color: var(--text-muted);
            font-size: 1.1rem;
        }}
        .container {{
            max-width: 900px;
            width: 100%;
        }}
        .card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 24px;
            margin-bottom: 30px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }}
        .card h2 {{
            margin-top: 0;
            color: var(--accent-color);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
        }}
        .plot-img {{
            width: 100%;
            height: auto;
            border-radius: 4px;
            margin-top: 15px;
            background-color: #fff;
            padding: 10px;
            box-sizing: border-box;
        }}
        .description-box {{
            margin-top: 20px;
            background-color: rgba(88, 166, 255, 0.05);
            border-left: 4px solid var(--accent-color);
            padding: 15px;
            border-radius: 0 4px 4px 0;
        }}
        .description-box h3 {{
            margin-top: 0;
            font-size: 1rem;
            color: #fff;
        }}
        .description-box p {{
            margin: 5px 0 0 0;
            font-size: 0.95rem;
            line-height: 1.5;
            color: var(--text-color);
        }}
        footer {{
            margin-top: 5px;
            color: var(--text-muted);
            font-size: 0.85rem;
            text-align: center;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Historial de Tráfico Acumulado</h1>
        <p class="subtitle">Visualización y respaldo de métricas a largo plazo para evitar la restricción de 14 días de GitHub.</p>
    </header>
    <div class="container">
        {cards_html}
    </div>
    <footer>
        <p>Actualizado automáticamente mediante GitHub Actions en tu repositorio fork.</p>
    </footer>
</body>
</html>"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("index.html sobreescrito dinámicamente con todas las gráficas")

if __name__ == "__main__":
    main()
