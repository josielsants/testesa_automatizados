import os
import sys
import unittest
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import ChromeOptions, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Endereco principal do site.
BASE_URL = "https://loja.elements.com.br"

# Pasta do projeto.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pasta usada pelo Selenium para guardar arquivos temporarios.
SELENIUM_CACHE = os.path.join(PROJECT_ROOT, ".selenium")

# Pasta para guardar screenshots e HTML em caso de falha.
ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, "artifacts")

# Caminho dos navegadores instalados no Windows.
CHROME_BINARY = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE_BINARY = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def criar_driver():
    """Cria um driver do Selenium (Chrome ou Edge)."""
    os.makedirs(SELENIUM_CACHE, exist_ok=True)
    os.environ["SE_CACHE_PATH"] = SELENIUM_CACHE

    chrome_options = ChromeOptions()
    chrome_options.add_argument("--window-size=1400,900")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if os.path.exists(CHROME_BINARY):
        chrome_options.binary_location = CHROME_BINARY

    edge_options = EdgeOptions()
    edge_options.add_argument("--window-size=1400,900")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--disable-dev-shm-usage")
    if os.path.exists(EDGE_BINARY):
        edge_options.binary_location = EDGE_BINARY

    erros = []

    try:
        return webdriver.Chrome(options=chrome_options)
    except WebDriverException as erro:
        erros.append(f"Chrome: {erro.msg}")

    try:
        return webdriver.Edge(options=edge_options)
    except WebDriverException as erro:
        erros.append(f"Edge: {erro.msg}")

    raise RuntimeError("Nao foi possivel abrir o navegador. " + " | ".join(erros))


def aceitar_cookies_se_existir(driver):
    """Tenta clicar no botao de aceitar cookies, se aparecer."""
    seletores = (
        "//button[contains(translate(., 'ACEITAR', 'aceitar'), 'aceitar')]",
        "//button[contains(translate(., 'CONCORDO', 'concordo'), 'concordo')]",
    )

    for xpath in seletores:
        try:
            botao = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            botao.click()
            return
        except TimeoutException:
            continue


def salvar_artifacts(driver, nome_teste):
    """Salva screenshot e HTML da pagina em artifacts/ em caso de erro."""
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefixo = f"{timestamp}_{nome_teste}"
    
    # Salvar screenshot
    screenshot_path = os.path.join(ARTIFACTS_DIR, f"{prefixo}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot salvo: {screenshot_path}")
    
    # Salvar HTML
    html_path = os.path.join(ARTIFACTS_DIR, f"{prefixo}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"HTML salvo: {html_path}")


class TesteBase(unittest.TestCase):
    """Classe base para testes com tratamento de erro e cleanup."""
    
    @classmethod
    def setUpClass(cls):
        """Configura o driver e o wait para todos os testes da classe."""
        cls.driver = criar_driver()
        cls.wait = WebDriverWait(cls.driver, 20)

    @classmethod
    def tearDownClass(cls):
        """Fecha o driver ao fim de todos os testes."""
        cls.driver.quit()

    def tearDown(self):
        """Salva artifacts se o teste falhou."""
        # Verifica se há exceção durante o teste
        if sys.exc_info()[0] is not None:
            salvar_artifacts(self.driver, self._testMethodName)
