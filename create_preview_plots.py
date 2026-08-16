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
    if not os.path.exists(file_path):
        print(f"⚠️ No se encontró {file_path}. Usando valores por defecto.")
        return 506, 34
    try:
        df = pd.read_csv(file_path, skiprows=1, quotechar='"', on_bad_lines='skip')
        row = df[df['Ruta de página y clase de pantalla'] == '/gw2-wallet-ligero/']
        if not row.empty:
            views = int(row['Vistas'].values[0])
            users = int(row['Usuarios activos'].values[0])
            print(f"✅ Totales GA cargados: {views} vistas, {users} usuarios")
            return views, users
        else:
            print("⚠️ No se encontró /gw2-wallet-ligero/ en el archivo. Usando valores por defecto.")
            return 506, 34
    except Exception as e:
        print(f"⚠️ Error al leer {file_path}: {e}. Usando valores por defecto.")
        return 506, 34

def process_raw_ga_to_daily(raw_file, output_file):
    if not os.path.exists(raw_file):
        print(f"⚠️ No se encontró {raw_file}. No se procesarán datos diarios.")
        return None
    try:
        df = pd.read_csv(raw_file, skiprows=1, header=None)
        df.columns = ['index', 'datetime', 'views', 'unique_visitors']
        df = df[df['index'] != 'Total']
        df['date'] = df['datetime'].astype(str).str[:8]
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        daily = df.groupby('date')[['views', 'unique_visitors']].sum().reset_index()
        daily.to_csv(output_file, index=False)
        print(f"✅ Datos diarios GA guardados en {output_file}")
        return daily
    except Exception as e:
        print(f"⚠️ Error al procesar {raw_file}: {e}")
        return None

def generate_synthetic_views(start_date, end_date, total_views, total_users):
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    n_days = len(date_range)
    if n_days == 0:
        return pd.DataFrame()
    avg_views = total_views / n_days
    avg_users = total_users / n_days
    synthetic_views = np.random.poisson(lam=avg_views, size=n_days)
    synthetic_users = np.random.poisson(lam=avg_users, size=n_days)
    diff_views = total_views - synthetic_views.sum()
    diff_users = total_users - synthetic_users.sum()
    for _ in range(abs(int(diff_views))):
        idx = np.random.randint(0, n_days)
        synthetic_views[idx] += 1 if diff_views > 0 else -1
        if synthetic_views[idx] < 0: synthetic_views[idx] = 0
    for _ in range(abs(int(diff_users))):
        idx = np.random.randint(0, n_days)
        synthetic_users[idx] += 1 if diff_users > 0 else -1
        if synthetic_users[idx] < 0: synthetic_users[idx] = 0
    df = pd.DataFrame({
        'date': date_range,
        'views': synthetic_views,
        'unique_visitors': synthetic_users
    })
    return df

def generate_synthetic_clones_periods():
    """
    Genera datos sintéticos de clones basados en tu conocimiento empírico.
    Con transiciones suaves entre periodos (caídas graduales).
    Periodo 1: Febrero - Abril (Promedio 450)
    Periodo 2: Mayo - Junio (Promedio 225 - caída del 50%)
    Periodo 3: Julio - 14 de Agosto (Promedio 14 - 100 por semana)
    """
    
    # Definir los puntos de control (fecha, valor_promedio)
    # Usamos puntos intermedios para crear curvas suaves
    control_points = [
        ("2026-02-19", 450),  # Inicio: 450
        ("2026-04-20", 450),  # Se mantiene alto hasta el 20 de abril
        ("2026-05-10", 340),  # Empieza a bajar suavemente
        ("2026-06-01", 225),  # Llega a 225 a principios de junio
        ("2026-06-20", 225),  # Se mantiene en 225
        ("2026-07-10", 120),  # Empieza a bajar de nuevo
        ("2026-08-01", 14),   # Llega a 14 en agosto
        ("2026-08-14", 14)    # Se mantiene en 14 hasta el 14 de agosto
    ]
    
    # Convertir a DataFrame
    df_control = pd.DataFrame(control_points, columns=['date', 'avg_clones'])
    df_control['date'] = pd.to_datetime(df_control['date'])
    df_control.set_index('date', inplace=True)
    
    # Generar todos los días desde el inicio hasta el final
    start_date = pd.to_datetime("2026-02-19")
    end_date = pd.to_datetime("2026-08-14")
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Interpolar los valores promedio para cada día (transición suave)
    # Reindexamos el DataFrame de control para que tenga todos los días y luego interpolamos
    df_control_daily = df_control.reindex(all_dates).interpolate(method='linear')
    
    # Ahora generamos datos aleatorios basados en esos promedios diarios
    clones = []
    unique = []
    
    for date in all_dates:
        avg = df_control_daily.loc[date, 'avg_clones']
        # Generar un valor aleatorio alrededor del promedio (con ruido)
        val_clones = int(np.random.poisson(lam=avg))
        val_unique = int(np.random.poisson(lam=avg * 0.85))  # 85% de los clones son únicos aprox
        
        # Asegurar mínimo 1
        if val_clones < 1: val_clones = 1
        if val_unique < 1: val_unique = 1
        
        clones.append(val_clones)
        unique.append(val_unique)
    
    # Crear DataFrame final
    df = pd.DataFrame({
        'date': all_dates,
        'count': clones,
        'unique': unique
    })
    
    print(f"✅ Datos sintéticos de clones generados (curva suave): {len(df)} días")
    return df

def merge_all_data(ga_daily, synthetic_data, api_data):
    api_data['date'] = pd.to_datetime(api_data['date'])
    api_data.set_index('date', inplace=True)
    combined = pd.concat([synthetic_data, ga_daily])
    combined.set_index('date', inplace=True)
    combined = combined.combine_first(api_data)
    combined = combined[~combined.index.duplicated(keep='last')]
    return combined.sort_index()

def plot_traffic(df, title, ylabel, file_name, show_unique=True):
    if df.empty:
        print(f"⚠️ No hay datos para graficar: {title}")
        return
    plt.figure(figsize=(14, 7))
    
    # Determinar qué columnas graficar
    if 'views' in df.columns:
        plt.plot(df.index, df['views'], marker='o', linestyle='-', color='#1f77b4', label='Vistas / Clones', markersize=2)
        if show_unique and 'unique_visitors' in df.columns:
            plt.plot(df.index, df['unique_visitors'], marker='o', linestyle='-', color='#d62728', label='Únicos', markersize=2)
    elif 'count' in df.columns:
        plt.plot(df.index, df['count'], marker='o', linestyle='-', color='#1f77b4', label='Clones', markersize=2)
        if show_unique and 'unique' in df.columns:
            plt.plot(df.index, df['unique'], marker='o', linestyle='-', color='#d62728', label='Clonadores Únicos', markersize=2)
    
    plt.title(title, fontsize=16)
    plt.ylabel(ylabel, fontsize=12)
    plt.xlabel("Fecha", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
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

# 1. VISTAS (Mismo proceso de antes)
total_views, total_users = load_totals_from_ga(TOTALS_FILE)
ga_daily_df = process_raw_ga_to_daily(RAW_GA_FILE, GA_DAILY_FILE)
if ga_daily_df is None:
    ga_daily_df = pd.DataFrame(columns=['date', 'views', 'unique_visitors'])

ga_views_sum = ga_daily_df['views'].sum() if not ga_daily_df.empty else 0
ga_users_sum = ga_daily_df['unique_visitors'].sum() if not ga_daily_df.empty else 0
remaining_views = max(0, total_views - ga_views_sum)
remaining_users = max(0, total_users - ga_users_sum)

print(f"📊 Vistas - Total GA: {total_views} vistas, {total_users} usuarios")
print(f"📊 Vistas - Cubierto por GA: {ga_views_sum} vistas, {ga_users_sum} usuarios")
print(f"📊 Vistas - Restante para distribuir: {remaining_views} vistas, {remaining_users} usuarios")

synthetic_start = pd.to_datetime(REPO_START_DATE)
synthetic_end = pd.to_datetime(GA_START_DATE) - timedelta(days=1)
synthetic_views_df = generate_synthetic_views(synthetic_start, synthetic_end, remaining_views, remaining_users)
print(f"✅ Vistas sintéticas generadas: {len(synthetic_views_df)} días")

api_views = fetch_github_traffic(REPO, TOKEN, "views")
if not ga_daily_df.empty:
    final_views = merge_all_data(ga_daily_df, synthetic_views_df, api_views)
else:
    final_views = pd.concat([synthetic_views_df, api_views])
    final_views.set_index('date', inplace=True)
    final_views = final_views[~final_views.index.duplicated(keep='last')]

ensure_dir(VIEWS_FILE)
final_views.to_csv(VIEWS_FILE)
print(f"✅ Datos de vistas guardados en {VIEWS_FILE}")

# 2. CLONES (NUEVO: Reconstrucción sintética basada en tu conocimiento)
print("\n🔄 Generando datos de clones...")
synthetic_clones_df = generate_synthetic_clones_periods()

api_clones = fetch_github_traffic(REPO, TOKEN, "clones")
if not api_clones.empty:
    final_clones = merge_all_data(pd.DataFrame(), synthetic_clones_df, api_clones)
else:
    final_clones = synthetic_clones_df.copy()
    final_clones.set_index('date', inplace=True)
    final_clones = final_clones[~final_clones.index.duplicated(keep='last')]

ensure_dir(CLONES_FILE)
final_clones.to_csv(CLONES_FILE)
print(f"✅ Datos de clones guardados en {CLONES_FILE}")

# 3. GENERAR GRÁFICOS
print("\n🎨 Generando gráficos...")
plot_traffic(final_views, "Vistas diarias - gw2-wallet-ligero (Histórico + API)", "Vistas", "github_views.webp")
if not final_clones.empty:
    plot_traffic(final_clones, "Clones diarios - gw2-wallet-ligero (Reconstrucción + API)", "Clones", "github_clones.webp")
else:
    print("⚠️ No hay datos de clones para graficar.")

print("\n🎉 Proceso completado exitosamente.")
