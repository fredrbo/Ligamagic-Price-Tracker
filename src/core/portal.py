from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

class Portal:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        
    def fazer_login(self, email, senha):
        """Realiza o login na plataforma LigaMagic."""
        try:
            self.logger.info("Iniciando processo de login...")
            
            # Aguarda o botão de login aparecer e clica nele
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="dropdownMenuLogin"]/div'))
            )
            login_button.click()
            self.logger.info("Modal de login aberto")
            
            # Aguarda o modal de login aparecer
            time.sleep(2)  # Pequena pausa para garantir que o modal esteja visível
            
            # Preenche o email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.send_keys(email)
            
            # Preenche a senha
            senha_field = self.driver.find_element(By.ID, "senha")
            senha_field.send_keys(senha)
            
            # Clica no botão de login
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            self.logger.info("Tentativa de login realizada")
            
            # Aguarda um momento para o login ser processado
            time.sleep(3)
            
            # Verifica se o login foi bem sucedido
            try:
                # Verifica se o elemento de login ainda está presente (login falhou)
                if self.driver.find_elements(By.XPATH, '//*[@id="dropdownMenuLogin"]/div'):
                    self.logger.error("Falha no login - Credenciais inválidas ou erro no processo")
                    return False
                else:
                    self.logger.info("Login realizado com sucesso!")
                    return True
                    
            except Exception as e:
                self.logger.error(f"Erro ao verificar status do login: {str(e)}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro durante o processo de login: {str(e)}")
            return False
