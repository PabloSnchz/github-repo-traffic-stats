import os
import pandas as pd
import requests
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ================================
# CONFIGURACIÓN
# ================================
REPO = "PabloSnchz/gw2-wallet-ligero"
TOKEN = os.getenv("GH_TOKEN")
DATA_DIR = "data"
VIEWS_FILE = os.path.join(DATA_DIR, "github_views/gw2-wallet-ligero.csv")
CLONES_FILE = os.path.join(DATA_DIR, "github_clones/gw2-wallet-ligero.csv")
TOTALS_FILE = "Páginas_y_pantallas_Ruta_de_página_y_clase_de_pantalla.csv"
RAW_GA_FILE = "download.csv"
GA_DAILY_FILE = "ga_daily_real.csv"
REPO_START_DATE = "2026-02-19"
GA_START_DATE = "2026-06-15"
TODAY = datetime.now().strftime("%Y-%m-%d")

# ================================
# FUNCIONES AUXILIARES
# ================================

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def fetch_github_traffic(repo, token, traffic_type):
    url = f"https://api.github.com/repos/{repo}/traffic/{traffic_type}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if traffic_type == "views":
            return pd.DataFrame(data["views"])
        elif traffic_type == "clones":
            return pd.DataFrame(data["clones"])
    else:
        print(f"❌ Error al obtener {traffic_type}: {response.status_code}")
        return pd.DataFrame()

def load_totals_from_ga(file_path):
    """Lee el total de vistas y usuarios desde el archivo de GA"""
    if not os.path.exists(file_path):
        print(f"⚠️ No se encontró {file_path}. Usando valores por defecto.")
        return 506, 34
    
    try:
        # Leer con manejo de comillas y saltos de línea
        df = pd.read_csv(file_path, skiprows=1, quotechar='"', on_bad_lines='skip')
        
        # Buscar la fila que contiene la ruta /gw2-wallet-ligero/
        row = df[df['Ruta de página y clase de pantalla'] == '/gw2-wallet-ligero/']
        if not row.empty:
            views = int(row['Vistas'].values[0])
            users = int(row['Usuarios activos'].values[0])
            print(f"✅ Totales cargados: {views} vistas, {users} usuarios")
            return views, users
        else:
            print("⚠️ No se encontró /gw2-wallet-ligero/ en el archivo. Usando valores por defecto.")
            return 506, 34
    except Exception as e:
        print(f"⚠️ Error al leer {file_path}: {e}. Usando valores por defecto.")
        return 506, 34

def process_raw_ga_to_daily(raw_file, output_file):
    """Convierte el CSV por horas a CSV por día"""
    if not os.path.exists(raw_file):
        print(f"⚠️ No se encontró {raw_file}. No se procesarán datos diarios.")
        return None
    
    try:
        # Leer saltando la primera línea (encabezado problemático)
        df = pd.read_csv(raw_file, skiprows=1, header=None)
        # Asignar nombres de columna
        df.columns = ['index', 'datetime', 'views', 'unique_visitors']
        
        # Eliminar la fila del total (si existe)
        df = df[df['index'] != 'Total']
        
        # Convertir a fecha
        df['date'] = df['datetime'].astype(str).str[:8]
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        
        # Agrupar por fecha y sumar
        daily = df.groupby('date')[['views', 'unique_visitors']].sum().reset_index()
        
        # Guardar
        daily.to_csv(output_file, index=False)
        print(f"✅ Datos diarios guardados en {output_file}")
        return daily
    except Exception as e:
        print(f"⚠️ Error al procesar {raw_file}: {e}")
        return None

def generate_synthetic_data(start_date, end_date, total_views, total_users):
    """Genera datos sintéticos con variación aleatoria sin sobrepasar el total"""
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    n_days = len(date_range)
    
    if n_days == 0:
        return pd.DataFrame()
    
    # Promedio diario
    avg_views = total_views / n_days
    avg_users = total_users / n_days
    
    # Generar valores aleatorios (Poisson)
    synthetic_views = np.random.poisson(lam=avg_views, size=n_days)
    synthetic_users = np.random.poisson(lam=avg_users, size=n_days)
    
    # Ajustar para que sumen exactamente el total
    diff_views = total_views - synthetic_views.sum()
    diff_users = total_users - synthetic_users.sum()
    
    # Distribuir la diferencia
    for _ in range(abs(int(diff_views))):
        idx = np.random.randint(0, n_days)
        synthetic_views[idx] += 1 if diff_views > 0 else -1
        if synthetic_views[idx] < 0:
            synthetic_views[idx] = 0
    
    for _ in range(abs(int(diff_users))):
        idx = np.random.randint(0, n_days)
        synthetic_users[idx] += 1 if diff_users > 0 else -1
        if synthetic_users[idx] < 0:
            synthetic_users[idx] = 0
    
    # Crear DataFrame
    df = pd.DataFrame({
        'date': date_range,
        'views': synthetic_views,
        'unique_visitors': synthetic_users
    })
    return df

def merge_all_data(ga_daily, synthetic_data, api_data, api_type):
    """Fusiona datos sintéticos + GA diario + API"""
    # Asegurar formato de fecha
    api_data['date'] = pd.to_datetime(api_data['date'])
    api_data.set_index('date', inplace=True)
    
    # Combinar: sintético + GA + API (API sobreescribe GA en fechas duplicadas)
    combined = pd.concat([synthetic_data, ga_daily])
    combined.set_index('date', inplace=True)
    combined = combined.combine_first(api_data)
    combined = combined[~combined.index.duplicated(keep='last')]
    return combined.sort_index()

def plot_traffic(df, title, ylabel, file_name):
    """Genera gráfico y lo guarda en preview_plots/"""
    if df.empty:
        print(f"⚠️ No hay datos para graficar: {title}")
        return
    
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['views' if 'views' in df.columns else 'count'], 
             marker='o', linestyle='-', color='#1f77b4', markersize=3)
    plt.title(title, fontsize=16)
    plt.ylabel(ylabel, fontsize=12)
    plt.xlabel("Fecha", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()
    
    ensure_dir("preview_plots/")
    plt.savefig(f"preview_plots/{file_name}", dpi=100, bbox_inches='tight')
    plt.close()
    print(f"✅ Gráfico guardado: preview_plots/{file_name}")

# ================================
# EJECUCIÓN PRINCIPAL
# ================================

print("🚀 Iniciando generación de datos y gráficos...")

# 1. Cargar totales de GA
total_views, total_users = load_totals_from_ga(TOTALS_FILE)

# 2. Procesar GA por horas a diario
ga_daily_df = process_raw_ga_to_daily(RAW_GA_FILE, GA_DAILY_FILE)
if ga_daily_df is None:
    # Si no hay archivo, crear DataFrame vacío
    ga_daily_df = pd.DataFrame(columns=['date', 'views', 'unique_visitors'])
else:
    print(f"✅ Datos GA diarios: {len(ga_daily_df)} días")

# 3. Calcular cuánto ha sido cubierto por GA
ga_views_sum = ga_daily_df['views'].sum() if not ga_daily_df.empty else 0
ga_users_sum = ga_daily_df['unique_visitors'].sum() if not ga_daily_df.empty else 0

# 4. Calcular lo que falta por distribuir en el periodo sintético
remaining_views = total_views - ga_views_sum
remaining_users = total_users - ga_users_sum

if remaining_views < 0: remaining_views = 0
if remaining_users < 0: remaining_users = 0

print(f"📊 Total GA: {total_views} vistas, {total_users} usuarios")
print(f"📊 Cubierto por GA: {ga_views_sum} vistas, {ga_users_sum} usuarios")
print(f"📊 Restante para distribuir: {remaining_views} vistas, {remaining_users} usuarios")

# 5. Generar datos sintéticos (desde 19/02 al 14/06)
synthetic_start = pd.to_datetime(REPO_START_DATE)
synthetic_end = pd.to_datetime(GA_START_DATE) - timedelta(days=1)

synthetic_df = generate_synthetic_data(synthetic_start, synthetic_end, remaining_views, remaining_users)
print(f"✅ Datos sintéticos generados: {len(synthetic_df)} días")

# 6. Obtener datos de API (últimos 14 días)
api_views = fetch_github_traffic(REPO, TOKEN, "views")
api_clones = fetch_github_traffic(REPO, TOKEN, "clones")

# 7. Fusionar todo para Views
if not ga_daily_df.empty:
    final_views = merge_all_data(ga_daily_df, synthetic_df, api_views, 'views')
else:
    # Si no hay GA, solo sintético + API
    final_views = pd.concat([synthetic_df, api_views])
    final_views.set_index('date', inplace=True)
    final_views = final_views[~final_views.index.duplicated(keep='last')]

# 8. Para Clones, solo usamos API (no hay datos históricos de clones)
if not api_clones.empty:
    final_clones = api_clones.copy()
    final_clones['date'] = pd.to_datetime(final_clones['date'])
    final_clones.set_index('date', inplace=True)
else:
    final_clones = pd.DataFrame()

# 9. Guardar en data/
ensure_dir(VIEWS_FILE)
ensure_dir(CLONES_FILE)
final_views.to_csv(VIEWS_FILE)
if not final_clones.empty:
    final_clones.to_csv(CLONES_FILE)
print(f"✅ Datos guardados en {VIEWS_FILE} y {CLONES_FILE}")

# 10. Generar gráficos
plot_traffic(final_views, "Vistas diarias - gw2-wallet-ligero (Histórico + API)", "Vistas", "github_views.webp")
if not final_clones.empty:
    plot_traffic(final_clones, "Clones diarios - gw2-wallet-ligero (API)", "Clones", "github_clones.webp")
else:
    print("⚠️ No hay datos de clones para graficar.")

print("🎉 Proceso completado exitosamente.")
