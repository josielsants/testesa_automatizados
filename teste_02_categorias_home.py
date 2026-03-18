import unittest
from .base import TesteBase, BASE_URL, aceitar_cookies_se_existir
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


class TesteCategoriasHome(TesteBase):
    """
    Teste de Menu de Categorias da Home
    
    Fluxo:
    1. Abre a home
    2. Valida que categorias estão visíveis
    3. Clica em cada categoria (Cadeiras, Mesas, Acessórios)
    4. Valida que navegação funcionou corretamente
    5. Valida URL e conteúdo de cada categoria
    """

    def test_menu_principal_mostra_categorias_e_links_validos(self):
        # ========== SETUP ==========
        print("\n" + "="*80)
        print("[TEST-02] CATEGORY NAVIGATION")
        print("="*80)
        
        print("\n[1/5] Opening home...")
        self.driver.get(BASE_URL)
        print("     OK - Home page loaded")
        aceitar_cookies_se_existir(self.driver)
        time.sleep(2)

        # ========== ACAO 1: VALIDAR CATEGORIAS VISIVEIS ==========
        print("[2/5] Looking for categories...")
        texto = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        
        self.assertIn("cadeiras", texto, "Menu deve exibir categoria 'cadeiras'")
        print("     OK - Cadeiras category found")
        time.sleep(0.5)
        
        self.assertIn("mesas", texto, "Menu deve exibir categoria 'mesas'")
        print("     OK - Mesas category found")
        time.sleep(0.5)
        
        self.assertIn("acess", texto, "Menu deve exibir categoria de acessorios")
        print("     OK - Acessorios category found")
        time.sleep(1)

        # ========== ACAO 2: LOCALIZAR E VALIDAR LINKS ==========
        print("[3/5] Locating category links...")
        link_cadeiras = self.driver.find_element(
            By.XPATH, "(//a[contains(@href, '/collections/cadeiras')])[1]"
        )
        print("     OK - Cadeiras link found")
        
        link_acessorios = self.driver.find_element(
            By.XPATH, "(//a[contains(@href, '/collections/acessorios')])[1]"
        )
        print("     OK - Acessorios link found")
        
        link_mesas = self.driver.find_element(
            By.XPATH, "(//a[contains(@href, '/collections/mesa')])[1]"
        )
        print("     OK - Mesas link found")
        time.sleep(1)
        
        # Validar URLs
        self.assertIn("/collections/cadeiras", link_cadeiras.get_attribute("href"),
                      "Link de cadeiras deve estar correto")
        self.assertIn("/collections/acessorios", link_acessorios.get_attribute("href"),
                      "Link de acessorios deve estar correto")
        self.assertIn("/collections/mesa", link_mesas.get_attribute("href"),
                      "Link de mesas deve estar correto")
        print("     OK - Link URLs validated")

        # ========== ACAO 3: CLICAR EM CADEIRAS E VALIDAR NAVEGACAO ==========
        print("[4/5] Clicking CADEIRAS...")
        url_anterior = self.driver.current_url
        
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", link_cadeiras)
            time.sleep(1)
            link_cadeiras.click()
        except:
            self.driver.execute_script("arguments[0].click();", link_cadeiras)
        
        time.sleep(3)
        print("     OK - Clicked Cadeiras")
        
        url_nova = self.driver.current_url
        print(f"     New URL: {url_nova}")
        self.assertNotEqual(url_anterior, url_nova, "URL deve mudar ao clicar em categoria")
        self.assertIn("/collections/cadeiras", url_nova, "Deve navegar para pagina de cadeiras")
        print("     OK - Navigation to Cadeiras confirmed")
        
        # Validar que página de cadeiras carregou
        texto_cadeiras = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        self.assertIn("cadeira", texto_cadeiras, "Pagina deve exibir produtos de cadeira")
        print("     OK - Cadeiras page loaded")
        time.sleep(1.5)

        # ========== ACAO 4: VOLTAR E CLICAR EM MESAS ==========
        print("     Going back to home...")
        self.driver.back()
        time.sleep(3)
        print("     OK - Returned to home")
        
        print("     Clicking MESAS...")
        link_mesas = self.driver.find_element(
            By.XPATH, "(//a[contains(@href, '/collections/mesa')])[1]"
        )
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", link_mesas)
            time.sleep(1)
            link_mesas.click()
        except:
            self.driver.execute_script("arguments[0].click();", link_mesas)
        
        time.sleep(3)
        print("     OK - Clicked Mesas")
        
        url_mesas = self.driver.current_url
        print(f"     New URL: {url_mesas}")
        self.assertIn("/collections/mesa", url_mesas, "Deve navegar para pagina de mesas")
        print("     OK - Navigation to Mesas confirmed")
        time.sleep(1.5)
        
        # ========== ACAO 5: VOLTAR E CLICAR EM ACESSORIOS ==========
        print("     Going back to home...")
        self.driver.back()
        time.sleep(3)
        print("     OK - Returned to home")
        
        print("[5/5] Clicking ACESSORIOS...")
        link_acessorios = self.driver.find_element(
            By.XPATH, "(//a[contains(@href, '/collections/acessorios')])[1]"
        )
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", link_acessorios)
            time.sleep(1)
            link_acessorios.click()
        except:
            self.driver.execute_script("arguments[0].click();", link_acessorios)
        
        time.sleep(3)
        print("     OK - Clicked Acessorios")
        
        url_acessorios = self.driver.current_url
        print(f"     New URL: {url_acessorios}")
        self.assertIn("/collections/acessorios", url_acessorios, "Deve navegar para pagina de acessorios")
        print("     OK - Navigation to Acessorios confirmed")
        
        texto_acessorios = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        self.assertIn("acess", texto_acessorios, "Pagina de acessorios deve carregar")
        print("     OK - Acessorios page loaded")
        
        print("\n" + "="*80)
        print("[PASS] TEST 02 - ALL CATEGORIES WORKING!")
        print("="*80 + "\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
