from re import M
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
import getpass
from time import sleep
import sqlite3
import datetime
from tqdm import tqdm
import os
from colorama import init, Fore, Style

def clearScreen():
    os.system('clear')

init()

anosDados = []

credenciais = []

clearScreen()

quantidade = int(input('Quantas escolas deseja fazer a raspagem? '))

clearScreen()

for q in range(quantidade):
    if quantidade == 1:
        clearScreen()
        email = str(input('Digite o email usado para logar no sistema Saber: '))
        clearScreen()
        senha = getpass.getpass('Agora digite a senha usada para logar no sistema Saber: ')
        clearScreen()

    else:
        print(f'Digite as informações da {q+1}ª escola:')
        clearScreen()
        email = str(input(f'Digite o email usado para logar no sistema Saber da {q+1}ª escola: '))
        clearScreen()
        senha = getpass.getpass(f'Agora digite a senha usada para logar no sistema Saber da {q+1}ª escola: ')
        clearScreen()
    
    escola = {}
    escola['email'] = email
    escola['senha'] = senha

    credenciais.append(escola)

    print(Fore.GREEN + 'Credenciais adicionadas!' + Style.RESET_ALL)
    clearScreen()

quantidade = int(input('Quantos anos você deseja fazer a raspagem? '))

clearScreen()

for q in range(quantidade):
    clearScreen()
    if quantidade == 1:
        ano = str(input('Digite o ano: '))

    else:
        print(f'Digite os anos que deseja raspar:')
        ano = str(input(f'Digite o {q+1}ª ano: '))
    
    anosDados.append(ano)

    print(Fore.GREEN + 'Informações adicionadas!' + Style.RESET_ALL)
    clearScreen()

print(Fore.YELLOW + 'AVISO! Não minimize o navegador, causará erro durante o processo. Divida a tela para acompanhar o progresso por aqui.' + Style.RESET_ALL)
sleep(5)
clearScreen()

serv = Service(ChromeDriverManager().install())

navegador = webdriver.Chrome(service=serv) 

def logar(email, senha):
    navegador.find_element('xpath', '//*[@id="user_email"]').send_keys(email)
    navegador.find_element('xpath', '//*[@id="user_password"]').send_keys(senha)
    navegador.find_element('xpath', '//*[@id="new_user"]/button').click()

def menuSuspenso(xpathMenu, ano):
    # Localize o elemento do menu suspenso
    menu = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, xpathMenu)))
    # Clique no elemento para exibir as opções
    menu.click()
    # Localize a opção desejada pelo texto do link
    opcao = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{ano}')]")))
    # Clique na opção desejada
    opcao.click()
    # Clicando no botão de busca
    busca = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="enrollments_searchbar"]/div[2]/div/div/span/button')))
    busca.click()
    sleep(6)

def scraper():
    # coletanto os dados

    individuo = {}

    nome = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[12]/div[1]/span[2]')
    nome = nome.text


    nascimento = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[12]/div[2]/div[2]')
    nascimento = nascimento.text
    nascimento = nascimento[12:]

    try:
        data_nascimento = datetime.datetime.strptime(f'{nascimento}', '%d/%m/%Y')
        data_atual = datetime.datetime.now()
        idade = data_atual.year - data_nascimento.year
        if data_atual.month < data_nascimento.month or (data_atual.month == data_nascimento.month and data_atual.day < data_nascimento.day):
            idade -= 1
    except:
        idade = ''

    try:
        cpf = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[12]/div[2]/div[3]')
        cpf = cpf.text
        cpf = cpf[5:]
        if cpf == '-':
            cpf = ' '
    except:
        cpf = " "

    try:
        inep = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[12]/div[2]/div[1]')
        inep = inep.text
        inep = inep[6:]
        inep = int(inep)
    except:
        inep = " "
    
    try:
        matricula = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[2]/div/div/span[2]')
        matricula = matricula.text
        matricula = int(matricula)
    except:
        matricula = " "

    try:
        ano = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[3]/div/span[2]')
        ano = ano.text
        ano = int(ano)
    except:
        ano = " "
    
    try:
        necessidadeEspecial = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[4]/div/div/span[2]')
        necessidadeEspecial = nome.text
    except:
        necessidadeEspecial = ' '
        
    try:
        serie = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[8]/div/span[2]')
        serie = serie.text
    except:
        serie = " "
        

    try:
        turma = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[11]/div[1]/span[2]')
        turma = turma.text
    except:
        turma = " "
        

    try:
        turno = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[5]/div/span[2]')
        turno = turno.text
    except:
        turno = " "
        

    try:
        modalidade = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[6]/div/span[2]')
        modalidade = modalidade.text
    except:
        modalidade = " "
        

    try:
        situacao = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[13]/div[1]/select')
        selecionado = Select(situacao)
        selecionado = selecionado.first_selected_option
        selecionado = selecionado.text
    except:
        selecionado = " "

    try:
        responsavel = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[17]/div[1]/input')
        responsavel = str(responsavel.get_attribute('value'))
        responsavel = responsavel.lower()
        responsavel = responsavel.title()
    except:
        responsavel = " "
    
    try:
        contato = navegador.find_element(By.XPATH, '/html/body/div[5]/div/form/div[20]/div/div[1]/input')
        contato = str(contato.get_attribute('value'))
    except:
        contato = " "


    individuo.update({
        'nome': nome,
        'nascimento':nascimento,
        'idade': idade,
        'cpf':cpf,
        'inep':inep,
        'matricula':matricula,
        'ano':ano,
        'necessidadeEspecial': necessidadeEspecial,
        'serie':serie,
        'turma':turma,
        'turno':turno,
        'modalidade':modalidade,
        'situacao': selecionado,
        'responsavel':responsavel,
        'contato':contato
    })

    return individuo

def fracionador(nAlunos, contador, nRepeticoes):
    x = nAlunos - contador
    if x > nRepeticoes:
        numero = nRepeticoes
    else:
        numero = x
    return numero



navegador.get('https://saber.pb.gov.br/')

dados = []

for credencial in credenciais:
    
    email = credencial['email']
    senha = credencial['senha']

    print(Fore.YELLOW + 'Logando...' + Style.RESET_ALL)
    #Fazendo login
    logar(email, senha)
    sleep(3)

    #Adquirindo o código da escola com base na url
    url = navegador.current_url
    url = url[-4:]
    codigoEscola = url
    
    #Adquirindo o nome da escola em questão
    nomeEscola = navegador.find_element('xpath', '/html/body/div[5]/div/div[3]/div/div[1]/div[1]/div[1]/h2').text
    nomeEscola = nomeEscola
    if 'Emef' in nomeEscola:
        nomeEscola = nomeEscola[5:]
        nomeEscola = 'Escola Municipal de Ensino Fundamental ' + nomeEscola


    """Coletando as turmas"""
    for ano in anosDados:

        navegador.get(f'https://saber.pb.gov.br/platform/schools/{codigoEscola}/enrollments') #Entrando na lista de turmas;
        menuSuspenso('//*[@id="enrollments_searchbar"]/div[1]/div[1]/div[2]/a', ano)

        numeroDeAlunos = navegador.find_element('xpath', '//*[@id="body"]/div/div[2]/div[2]/div/div[1]/div/div').text
        numeroDeAlunos = numeroDeAlunos[:3]
        numeroDeAlunos = int(numeroDeAlunos)
        
        contador = 0

        pbar = tqdm(total=numeroDeAlunos)

        paginador = 2
        while contador != numeroDeAlunos:
            repeticoes = fracionador(numeroDeAlunos, contador, 30)
            for dado in range(repeticoes):
                numeral = dado+1
                # Clicando no elemento editar matricula e abrindo ele em outra aba
                elemento = navegador.find_element('xpath',f'//*[@id="body"]/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[{numeral}]/td[10]/a[1]')
                actions = ActionChains(navegador)
                actions.key_down(Keys.CONTROL).click(elemento).key_up(Keys.CONTROL).perform()
                navegador.switch_to.window(navegador.window_handles[1]) # muda para a nova aba


                while True:    
                    try:
                        individuo = scraper()
                        break
                    except:
                        print(Fore.RED + 'Erro na rede' + Style.RESET_ALL)
                        navegador.refresh()
                individuo['escola'] = nomeEscola
                nominador = individuo['nome']
                turm = individuo['turma']
                marcAno = individuo['ano']
                idade = individuo['idade']

                clearScreen()
                print(f'{nomeEscola} / {ano}')
                pbar.update(1)
                print(f'     {nominador} - {idade} anos - {turm}')
                
                dados.append(individuo)
                contador+=1

                # fechando a aba
                navegador.close()
                # muda para a aba anterior
                navegador.switch_to.window(navegador.window_handles[0])
            
            try:
                mudarPagina = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[5]/div/div[2]/div[2]/div/div[3]/div/div/a[{paginador}]')))
                mudarPagina.click()
            except:
                pass
            paginador+=1

        print(Fore.GREEN + f'Dados de {nomeEscola} concluídos' + Style.RESET_ALL)    
        clearScreen()    
        pbar.close()

    sair = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginbar"]/li[6]/a')))
    sair.click()
    print(Fore.YELLOW + 'Saindo...' + Style.RESET_ALL)  

navegador.quit()

print(Fore.YELLOW + 'Digite o caminho juntamente com o nome do arquivo: \nEx: /home/fulanencio/Documentos/nomeDoArquivo.json' + Style.RESET_ALL)
nomeArquivo = str(input('caminho/nome: '))
clearScreen()


print(Fore.YELLOW + 'Gerando arquivo .json...' + Style.RESET_ALL)
with open(nomeArquivo, "w") as alunos: 
    json.dump(dados, alunos, indent=4, ensure_ascii=False)
clearScreen()
print(Fore.GREEN + 'Arquivo .json gerando com sucesso!' + Style.RESET_ALL)

print(Fore.RED + 'Fechando o programa!' + Style.RESET_ALL)
sleep(2)
exit()



