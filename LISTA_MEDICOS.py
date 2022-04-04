from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
try:
    url = 'https://portal.cfm.org.br/busca-medicos/'
    browser = Firefox()
    browser.implicitly_wait(20)
    browser.get(url)
    sleep(1)
    browser.find_element(By.XPATH,'/html/body/div[1]/div[4]/div[2]/button').click()
    sleep(1)
    uf = browser.find_element(By.NAME,'uf')
    sleep(1)
    uf.send_keys('M'* 2)
    uf.send_keys(Keys.ENTER)
    sit = browser.find_element(By.NAME,'tipoSituacao')
    sit.send_keys('A')
    sit.send_keys(Keys.ENTER)
    espec = browser.find_element(By.NAME,'especialidade')
    espec.send_keys('CCCCCCCCCCCCCCC')
    espec.send_keys(Keys.ENTER)
    sleep(4)
    browser.find_element(By.XPATH,'/html/body/div[1]/div[1]/section[2]/div/div/div/article/div[2]/div/div/form/div/div[4]/div[2]/button').click()
except Exception as erroentrada:
    print(f'erro na entrada dos dados{erroentrada}')
    browser.find_element(By.XPATH,'/html/body/div[1]/div[1]/section[2]/div/div/div/article/div[2]/div/div/form/div/div[4]/div[2]/button').click()
else:
    listademedicos = []
    dadosdosmedicos = {}
    sleep(2)
try:
    for num in range(1, 550):#3247
        paginacao = browser.find_element(By.ID,'paginacao')
        listapaginas = paginacao.find_elements(By.TAG_NAME,'li')
        sleep(0.01)
        for ancora in listapaginas:
            a = ancora.text
            if a == str(num):
                ancora.click()
                break
        sleep(2)
        medicos = browser.find_elements(By.CLASS_NAME,'card-body')
        sleep(2)
        for dados in medicos:
            dadosdosmedicos['Nome:']= dados.find_element(By.TAG_NAME,'h4').text
            dadosdosmedicos['CRM:'] = dados.find_element(By.CLASS_NAME,'col-md-4').text
            dadosdosmedicos['Data de inscricao:'] = dados.find_elements(By.CLASS_NAME,'col-md-4')[1].text
            dadosdosmedicos['Primeira Inscricao na UF:'] = dados.find_elements(By.CLASS_NAME,'col-md-4')[2].text
            dadosdosmedicos['Inscricao:'] = dados.find_elements(By.CLASS_NAME,'col-md-4')[3].text
            dadosdosmedicos['Situacao:'] = dados.find_elements(By.CLASS_NAME,'col-md')[0].text
            dadosdosmedicos['Inscricao em outro estado:'] = dados.find_element(By.TAG_NAME,'span').text
            if len(dados.find_elements(By.CLASS_NAME,'col-md-12')) <= 2:
                dadosdosmedicos['Especialidades:'] = dados.find_elements(By.CLASS_NAME,'col-md-12')[1].text
            else:
                dadosdosmedicos['Especialidades:'] = dados.find_elements(By.CLASS_NAME, 'col-md-12')[2].text
            dadosdosmedicos['Endereço:'] = dados.find_element(By.CLASS_NAME,'col-md-7').text
            dadosdosmedicos['telefone:'] = dados.find_elements(By.CLASS_NAME,'col-md-7')[1].text
            listademedicos.append(dadosdosmedicos.copy())

except Exception as erroconsulta:
    print(erroconsulta.__class__)
    print(erroconsulta.__cause__)
    print(erroconsulta.__context__)
    print(erroconsulta)
else:
    print('Deu certo, sem erros')

finally:
    arquivo = pd.DataFrame(listademedicos)
    arquivo.to_csv('listaMG_CP.csv')
4J
#for med in listademedicos:
#    for campos, values in med.items():
#        print(f'{campos}:{values}')
#    print('='*30)
