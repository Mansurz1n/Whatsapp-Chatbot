from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip
import time
import openai


# navegador
def iniciar_navegador():
  Chrome_Profile_Path =  r"C:\Users\gabco\AppData\Local\Google\Chrome\User Data\Default"


  options = webdriver.ChromeOptions()
  options.add_argument(f"user-data-dir={Chrome_Profile_Path}")
  options.add_argument("--log-level=3")
  service= Service(ChromeDriverManager().install())
  nav = webdriver.Chrome(service=service,options=options)
  return nav
# ChatGPT
def chatbot_resposta(mensagem):
    openai.api_key = ""  # Substitua pela sua chave
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        store = True,
        messages=[{"role": "user", "content": mensagem}]
    )
    return response.choices[0].message["content"]


#Monitor do chat 
def monitorar_chat(nav):
    print("Bot iniciado. Monitorando mensagens...")
    resposta_anterior = ""
    
    while True:
        try:
            time.sleep(5)
            
            # Atualize este XPATH conforme necessário
            mensagens = nav.find_elements(
                By.XPATH,
                '//div[contains(@class, "message-in")]//div[contains(@class, "copyable-text")]'
            )
            
            if mensagens:
                ultima_msg = mensagens[-1].text
                
                if ultima_msg == resposta_anterior:
                    continue
                
                print(f"Mensagem recebida: {ultima_msg}")
                
                resposta = chatbot_resposta(ultima_msg)
                resposta_anterior = resposta
                
                pyperclip.copy(resposta)
                nav.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]').send_keys(Keys.CONTROL + "v" + Keys.ENTER)
                print(f"Resposta enviada: {resposta}")
                
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(10)
            break

if __name__ == "__main__":
    nav = iniciar_navegador()
    nav.get("https://web.whatsapp.com")
    input("⚠️ Faça login no WhatsApp Web e pressione Enter...")
    monitorar_chat(nav)