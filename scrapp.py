from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# **Configuración del navegador**
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")  # Evitar detección como bot
options.add_argument("--log-level=3")  # Reducir logs en consola
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# **Inicializar WebDriver**
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# **Abrir la URL de FIBA**
url = "https://www.fiba.basketball/en/events/basketball-champions-league-americas-24-25/teams"
driver.get(url)

# **Esperar unos segundos para que la página cargue completamente**
time.sleep(5)

print("✅ Página abierta correctamente. Realiza el clic manualmente.")


ruta_guardado = r"df_info_teams.csv"

# **PASO 4: Esperar que el contenedor de equipos esté disponible**

""" try:
    equipos_contenedor = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_1njabzg0"))  # Grid de equipos
    )
    print("✅ Contenedor de equipos detectado.")

except Exception as e:
    print(f"❌ No se encontró la sección de equipos. Error: {e}")
 """
# **Lista para almacenar los datos extraídos**
teams_data = []

# **Buscar todos los elementos de los equipos dentro del contenedor**
equipos = driver.find_elements(By.XPATH, '//*[@id="themeWrapper"]/div[2]/div/div/div/div[3]/div[1]/div/div/a')

# Confirmamos cuántos equipos se detectaron
print(f"✅ Se encontraron {len(equipos)} equipos.")

# **Iterar sobre cada equipo para extraer la información**
for equipo in equipos:
    try:
        # **Extraer Nombre del Club**
        nombre_equipo = equipo.find_element(By.XPATH, './div[2]/h2/span').text.strip()

        # **Extraer URL del Logo**
        logo_element = equipo.find_element(By.XPATH, './div[2]/div/div/img')
        logo_url = logo_element.get_attribute("src")

        # **Extraer Texto Adicional**
        texto_extra = equipo.find_element(By.XPATH, './div[2]/span/div').text.strip()

        # **Agregar los datos a la lista**
        teams_data.append([nombre_equipo, logo_url, texto_extra])
        print(f"✅ Extraído: {nombre_equipo} - {logo_url} - {texto_extra}")

    except Exception as e:
        print(f"⚠️ Error al extraer datos de un equipo. Detalles: {e}")

# **Crear el DataFrame**
df_info_teams = pd.DataFrame(teams_data, columns=["Team", "Url", "Name"])

# **Mostrar en la consola**
print("\n✅ DataFrame generado:")
print(df_info_teams)

# **Guardar en la ruta especificada**
df_info_teams.to_csv(ruta_guardado, index=False)
print(f"✅ Archivo guardado en: {ruta_guardado}")