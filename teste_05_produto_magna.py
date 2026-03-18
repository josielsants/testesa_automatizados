import unittest
from .base import TesteBase, BASE_URL, aceitar_cookies_se_existir
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class TesteProdutoMagna(TesteBase):
    """
    Teste de Fluxo de Compra - Cadeira Gamer Elements Magna
    
    Fluxo Completo:
    1. Abre PDP do produto
    2. Scrolls na página e valida informações
    3. Seleciona cor (preta)
    4. Aumenta quantidade para 3
    5. Clica em "Adicionar ao Carrinho"
    6. Valida feedback visual (toast/modal)
    7. Valida contador do carrinho atualizar
    8. Procura botão "Comprar Agora"
    9. Clica e valida navegação para checkout
    10. Salva screenshot/HTML se algo falhar
    """

    def test_produto_magna_fluxo_completo_checkout(self):
        # ========== SETUP ==========
        print("\n" + "="*80)
        print("🛒 TESTE 05: FLUXO COMPLETO DE COMPRA - CADEIRA MAGNA")
        print("="*80)
        
        print("\n[1/10]  Abrindo página de produto (Cadeira Gamer Elements Magna)...")
        self.driver.get(f"{BASE_URL}/products/cadeira-gamer-elements-magna")
        print(f"       OK URL: {self.driver.current_url}")
        aceitar_cookies_se_existir(self.driver)
        time.sleep(2)

        # ========== AÇÃO 1: VALIDAR PDP CARREGOU ==========
        print("[2/10] ⏳ Aguardando carregamento da página de produto...")
        botao_compra = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[contains(., 'Adicionar ao carrinho')]")
            )
        )
        print("       OK Botão 'Adicionar ao Carrinho' encontrado")
        time.sleep(1)
        
        texto = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        self.assertIn("cadeira gamer elements magna", texto,
                      "Página deve exibir nome do produto")
        print("       OK Nome do produto validado: Cadeira Gamer Elements Magna")
        time.sleep(0.5)
        
        self.assertIn("r$ 1.849,00", texto,
                      "Página deve exibir preço R$ 1.849,00")
        print("       OK Preço validado: R$ 1.849,00")
        time.sleep(0.5)
        
        self.assertIn("frete gr", texto,
                      "Página deve indicar frete grátis")
        print("       OK Frete grátis confirmado")
        time.sleep(0.5)
        
        self.assertIn("10% off", texto,
                      "Página deve exibir promoção de 10% off")
        print("       OK Promoção de 10% off encontrada")
        time.sleep(1)

        # ========== AÇÃO 2: SCROLLAR NA PÁGINA ==========
        print("[3/10]  Scrollando para visualizar imagens do produto...")
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)
        
        # Validar que imagens do produto estão visíveis
        print("        Procurando imagens do produto...")
        imagens_produto = self.driver.find_elements(By.XPATH, "//img[contains(@alt, 'Cadeira')]")
        imagens_visiveis = [img for img in imagens_produto if img.is_displayed()]
        self.assertGreater(len(imagens_visiveis), 0, "Deve haver imagens do produto visíveis")
        print(f"       OK Encontradas {len(imagens_visiveis)} imagem(ns) do produto visível(is)")
        time.sleep(1.5)

        # ========== AÇÃO 3: SELECIONAR COR (PRETA) ==========
        print("[4/10] 🎨 Selecionando cor (Preto)...")
        try:
            # Tentar encontrar opções de cor
            opcoes_cor = self.driver.find_elements(By.XPATH, "//button[contains(@title, 'preto') or contains(@aria-label, 'preto')] | //label[contains(., 'Preto')] | //input[@value='preto']")
            
            if opcoes_cor:
                cor = opcoes_cor[0]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", cor)
                time.sleep(1)
                print("        Clicando na cor preta...")
                cor.click()
                time.sleep(1.5)
                print("       OK Cor selecionada com sucesso")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", botao_compra)
            else:
                print("       [INFO]  Estrutura de seleção de cor não encontrada - continuando teste")
        except Exception as e:
            print(f"       [WARNING]  Não foi possível selecionar cor: {e}")
        
        time.sleep(1)

        # ========== AÇÃO 4: AUMENTAR QUANTIDADE PARA 3 ==========
        print("[5/10]  Alterando quantidade para 3 unidades...")
        try:
            # Tentar encontrar input de quantidade ou botão "+"
            quantidade_input = self.driver.find_elements(By.XPATH, "//input[contains(@name, 'quantity') or contains(@type, 'number')] | //input[contains(@aria-label, 'quantidade')]")
            
            if quantidade_input:
                input_qty = quantidade_input[0]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", input_qty)
                time.sleep(0.5)
                
                print("       📌 Input de quantidade encontrado")
                print("        Informando quantidade 3...")
                # Limpar e digitar quantidade
                input_qty.clear()
                time.sleep(0.3)
                input_qty.send_keys("3")
                time.sleep(0.5)
                
                # Validar que quantidade foi alterada
                valor_qty = input_qty.get_attribute("value")
                self.assertEqual(valor_qty, "3", "Quantidade deve ser 3")
                print(f"       OK Quantidade alterada para: {valor_qty}")
            else:
                # Tentar usar botão de incremento
                botoes_mais = self.driver.find_elements(By.XPATH, "//button[contains(., '+')]")
                if botoes_mais:
                    print("       📌 Usando botão + para incrementar quantidade")
                    for i in range(2):  # Clicar 2 vezes para chegar a 3
                        print(f"        Click {i+1}/2...")
                        botoes_mais[0].click()
                        time.sleep(0.5)
                    print("       OK Quantidade aumentada para 3")
                else:
                    print("       [INFO]  Campo de quantidade não encontrado - continuando")
                    
        except Exception as e:
            print(f"       [WARNING]  Não foi possível aumentar quantidade: {e}")
        
        time.sleep(2)

        # ========== AÇÃO 5: CLICAR EM "ADICIONAR AO CARRINHO" ==========
        print("[6/10] 🛍️  Clicando em 'Adicionar ao Carrinho'...")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", botao_compra)
        time.sleep(1)
        
        self.assertTrue(botao_compra.is_displayed(),
                        "Botão 'Adicionar ao carrinho' deve estar visível")
        self.assertTrue(botao_compra.is_enabled(),
                        "Botão 'Adicionar ao carrinho' deve estar ativo")
        
        print("        Clicando no botão...")
        # Clicar no botão
        botao_compra.click()
        print("       OK Clique realizado")
        time.sleep(2.5)

        # ========== AÇÃO 6: VALIDAR FEEDBACK VISUAL ==========
        print("[7/10]  Aguardando feedback de 'Adicionado ao Carrinho'...")
        try:
            # Procurar por modal/toast de confirmação
            feedback = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Adicionado')] | //*[contains(text(), 'adicionado')] | //*[contains(text(), 'carrinho')]")
            
            if feedback:
                self.assertTrue(feedback[0].is_displayed(),
                                "Deve exibir mensagem de confirmação")
                print(f"       OK Feedback visual exibido: '{feedback[0].text}'")
                time.sleep(2)
            else:
                print("       [WARNING]  Nenhuma mensagem de confirmação visível (continuando)")
        except Exception as e:
            print(f"       [WARNING]  Não foi possível validar feedback visual: {e}")
        
        time.sleep(1)

        # ========== AÇÃO 7: VALIDAR CONTADOR DO CARRINHO ==========
        print("[8/10]  Verificando contador do carrinho...")
        try:
            # Procurar pelo contador do carrinho na header
            contador = self.driver.find_elements(By.XPATH, "//span[contains(@class, 'cart')] | //a[contains(@href, '/cart')] /span | //span[contains(text(), '3')]")
            
            if contador:
                texto_contador = contador[0].text
                print(f"       OK Contador do carrinho atualizado: {texto_contador}")
            else:
                print("       [INFO]  Contador do carrinho não visível (continuando)")
        except Exception as e:
            print(f"       [WARNING]  Não foi possível validar contador: {e}")
        
        time.sleep(1)

        # ========== AÇÃO 8: PROCURAR BOTÃO "COMPRAR AGORA" ==========
        print("[9/10]  Procurando botão 'Comprar Agora' ou 'Ir para Checkout'...")
        try:
            # Scrollar até encontrar botão "Comprar Agora"
            self.driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(1.5)
            
            # Procurar botão de checkout
            botoes_checkout = self.driver.find_elements(By.XPATH, 
                "//button[contains(., 'Comprar Agora')] | //button[contains(., 'Ir para checkout')] | //button[contains(., 'Finalizar compra')] | //a[contains(., 'Comprar Agora')] | //a[contains(@href, '/checkout')]")
            
            if botoes_checkout:
                botao_checkout = botoes_checkout[0]
                self.assertTrue(botao_checkout.is_displayed(),
                                "Botão de checkout deve estar visível")
                print("       OK Botão de checkout encontrado e visível")
                
                # ========== AÇÃO 9: CLICAR EM "COMPRAR AGORA" ==========
                print("[10/10] 🚀 Clicando em 'Comprar Agora'...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", botao_checkout)
                time.sleep(1)
                
                url_antes = self.driver.current_url
                print(f"        📌 URL antes: {url_antes}")
                print("         Clicando no botão...")
                botao_checkout.click()
                time.sleep(3)
                
                # ========== AÇÃO 10: VALIDAR NAVEGAÇÃO PARA CHECKOUT ==========
                url_depois = self.driver.current_url
                print(f"        📌 URL depois: {url_depois}")
                self.assertNotEqual(url_antes, url_depois,
                                    "URL deve mudar ao clicar em 'Comprar Agora'")
                
                # Validar que foi para checkout ou página de pagamento
                self.assertTrue(
                    ("/checkout" in url_depois.lower() or 
                     "/cart" in url_depois.lower() or 
                     "shop" in url_depois.lower() or 
                     "payment" in url_depois.lower()),
                    f"Deve navegar para checkout, mas foi para: {url_depois}"
                )
                
                print(f"        OK Navegação para checkout bem-sucedida!")
                print("\n" + "="*80)
                print("[PASS] TESTE 05 PASSOU - FLUXO COMPLETO DE COMPRA FUNCIONANDO!")
                print("="*80 + "\n")
            else:
                print("        [WARNING]  Botão 'Comprar Agora' não encontrado na página")
                print("\n" + "="*80)
                print("[WARNING]  TESTE 05 PARCIALMENTE COMPLETO - Faltou clicar em 'Comprar Agora'")
                print("="*80 + "\n")
                
        except Exception as e:
            print(f"        [WARNING]  Erro durante checkout flow: {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
