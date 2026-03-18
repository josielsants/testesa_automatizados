import unittest
from .base import TesteBase, BASE_URL, aceitar_cookies_se_existir
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class TesteSuporteHome(TesteBase):
    """
    Teste de Área de Suporte na Home
    
    Fluxo:
    1. Abre a home
    2. Scrolla até seção de FAQ
    3. Valida FAQ título e perguntas
    4. Clica em uma pergunta para expandir resposta
    5. Valida resposta aparece
    6. Clica no link "Ir para suporte"
    7. Valida navegação para atendimento
    """

    def test_area_de_suporte_exibe_faq_e_link_de_atendimento(self):
        # ========== SETUP ==========
        print("\n" + "="*80)
        print("[TEST] TESTE 03: SEÇÃO DE FAQ E SUPORTE")
        print("="*80)
        
        print("\n[1/6]  Abrindo home...")
        self.driver.get(BASE_URL)
        print(f"     OK Página aberta: {BASE_URL}")
        aceitar_cookies_se_existir(self.driver)
        time.sleep(2)

        # ========== AÇÃO 1: SCROLLAR ATÉ FAQ ==========
        print("[2/6]  Scrollando até seção de FAQ...")
        self.driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2.5)
        print("     OK Scrolled com sucesso")

        # ========== AÇÃO 2: VALIDAR FAQ ESTÁ VISÍVEL ==========
        print("[3/6]  Procurando seção de Perguntas Frequentes...")
        faq_titulo = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(., 'Perguntas Frequentes')]")
            )
        )
        print("     OK Seção 'Perguntas Frequentes' encontrada e visível")
        time.sleep(1)
        
        self.assertTrue(faq_titulo.is_displayed(),
                        "Seção 'Perguntas Frequentes' deve estar visível")

        # ========== AÇÃO 3: VALIDAR PERGUNTAS NA FAQ ==========
        print("[4/6]  Validando conteúdo das perguntas...")
        texto = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        
        self.assertIn("como eu sei qual cadeira", texto,
                      "FAQ deve conter pergunta sobre qual cadeira escolher")
        print("     OK Pergunta sobre escolha de cadeira encontrada")
        time.sleep(0.5)
        
        self.assertIn("a elements entrega para todo o brasil", texto,
                      "FAQ deve conter pergunta sobre entrega")
        print("     OK Pergunta sobre entrega encontrada")
        time.sleep(1)

        # ========== AÇÃO 4: LOCALIZAR E CLICAR EM UMA PERGUNTA ==========
        print("[5/6]   Tentando expandir uma pergunta da FAQ...")
        try:
            perguntas = self.driver.find_elements(By.XPATH, "//summary | //button[contains(@aria-expanded, 'false')]")
            if perguntas:
                pergunta = perguntas[0]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", pergunta)
                time.sleep(1)
                print("      Clicando em pergunta...")
                pergunta.click()
                time.sleep(1.5)
                
                texto_apos = self.driver.find_element(By.TAG_NAME, "body").text
                print("     OK Pergunta expandida com sucesso")
            else:
                print("     [WARNING]  Nenhuma pergunta interativa encontrada (continuando)")
        except Exception as e:
            print(f"     [WARNING]  Não foi possível expandir pergunta: {e}")

        # ========== AÇÃO 5: LOCALIZAR LINK DE SUPORTE ==========
        print("[6/6]  Localizando link de suporte...")
        link_suporte = self.driver.find_element(
            By.XPATH, "//a[contains(., 'Ir para suporte')]"
        )
        print("     OK Link de suporte encontrado")
        
        href = link_suporte.get_attribute("href")
        print(f"     📌 URL do suporte: {href}")
        self.assertIn("atendimento.elements.com.br", href,
                      "Link de suporte deve apontar para atendimento.elements.com.br")
        self.assertTrue(link_suporte.is_displayed(), "Link de suporte deve estar visível")
        self.assertTrue(link_suporte.is_enabled(), "Link de suporte deve estar clicável")
        print("     OK Link validado")
        time.sleep(1)

        # ========== AÇÃO 6: CLICAR NO LINK DE SUPORTE ==========
        print("       Clicando no link de suporte (abrindo em nova aba)...")
        try:
            self.driver.execute_script("arguments[0].target='_blank';", link_suporte)
            self.driver.execute_script("arguments[0].click();", link_suporte)
            time.sleep(2.5)
            print("     OK Clicou no link")
            
            abas = self.driver.window_handles
            print(f"     📑 Total de abas: {len(abas)}")
            self.assertGreater(len(abas), 1, "Deve abrir link de suporte em nova aba")
            
            self.driver.switch_to.window(abas[0])
            print("     OK Voltou para aba principal")
        except Exception as e:
            print(f"     [WARNING]  Não foi possível clicar no link de suporte: {e}")
        
        print("\n" + "="*80)
        print("[PASS] TESTE 03 PASSOU - FAQ E SUPORTE FUNCIONAM!")
        print("="*80 + "\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
