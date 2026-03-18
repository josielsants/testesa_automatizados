import unittest
from .base import TesteBase, BASE_URL, aceitar_cookies_se_existir
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class TesteTituloHome(TesteBase):
    """
    Teste de Carregamento da Home Page
    
    Fluxo:
    1. Abre a home da Elements
    2. Aceita cookies e valida logo
    3. Scrolls pela página e valida seções
    4. Valida imagens carregando
    5. Interage com elementos principais
    """

    def test_home_carrega_com_titulo_logo_e_banner(self):
        # ========== SETUP ==========
        print("\n" + "="*80)
        print("[TEST-01] HOME PAGE VALIDATION")
        print("="*80)
        
        print("\n[1/7] Opening home page...")
        self.driver.get(BASE_URL)
        print("     OK - Home page loaded")
        time.sleep(1.5)
        
        print("[2/7] Accepting cookies...")
        aceitar_cookies_se_existir(self.driver)
        time.sleep(1)

        # ========== ACAO 1: VALIDAR LOGO E BANNER ==========
        print("[3/7] Waiting for logo...")
        logo = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[normalize-space()='Elements']")
            )
        )
        print("     OK - Logo found and visible")
        time.sleep(1)
        
        titulo = self.driver.title.lower()
        texto_pagina = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        
        print(f"     Page title: {self.driver.title}")
        self.assertIn("elements", titulo, "Titulo da aba deve conter 'elements'")
        self.assertTrue(logo.is_displayed(), "Logo principal deve estar visivel")
        self.assertTrue(logo.is_enabled(), "Logo deve estar clicavel")
        print("     OK - Logo and title validated")
        time.sleep(1)

        # ========== ACAO 2: VALIDAR CONTEUDO PRINCIPAL ==========
        print("[4/7] Validating main content...")
        self.assertIn("ver ofertas", texto_pagina, "Pagina deve conter 'ver ofertas'")
        self.assertIn("cadeira", texto_pagina, "Pagina deve conter 'cadeira'")
        print("     OK - Main content validated")
        time.sleep(1)
        
        # ========== ACAO 3: SCROLLAR E VALIDAR SECOES ==========
        print("[5/7] Scrolling down to check sections...")
        self.driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)
        print("     OK - Page scrolled")
        
        texto_apos_scroll = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        self.assertIn("cadeiras", texto_apos_scroll, "Categorias devem estar visiveis apos scroll")
        print("     OK - Categories found after scroll")
        
        # ========== ACAO 4: VALIDAR IMAGENS ==========
        print("[6/7] Validating images...")
        imagens = self.driver.find_elements(By.TAG_NAME, "img")
        self.assertGreater(len(imagens), 0, "Pagina deve conter imagens")
        print(f"     OK - {len(imagens)} images found")
        
        imagens_visiveis = [img for img in imagens if img.is_displayed()]
        self.assertGreater(len(imagens_visiveis), 0, "Deve haver imagens visiveis na pagina")
        print(f"     OK - {len(imagens_visiveis)} images visible")
        time.sleep(1)
        
        # ========== ACAO 5: VOLTAR AO TOPO ==========
        print("[7/7] Going back to top...")
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1.5)
        self.assertTrue(logo.is_displayed(), "Logo deve estar visivel apos voltar ao topo")
        print("     OK - Back to top successfully")
        
        print("\n" + "="*80)
        print("[PASS] TEST 01 - HOME PAGE LOADED CORRECTLY!")
        print("="*80 + "\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
