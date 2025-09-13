# ! Este arquivo deve ser executado em um terminal separado ao terminal que esta rodando a API
# ! Dentro deste script, sera executados testes automatizados para checar todas as funcionabilidades da API de forma mais pratica, comprovando e testando seu funcionamento.

# Bibliotecas
import requests

# URL da API
URLAPI = "http://127.0.0.1:5000" # TODO: Se o endereço da API mudar quando for executada, ou voce estiver utilizando o Docker, altere aqui antes de rodar

# * Testear Mock De Dados (integrar Dados Ficticios)
def testar_mock():
    res = requests.post(f"{URLAPI}/mock")
    
    if res.status_code == 201:
        return print(f"TESTE MOCK - Mock de dados enviado com sucesso ✅ {res.status_code}")
    else:
        return print(f"TESTE MOCK - Mock de dados deu ERRO! 🚫 {res.status_code}")
        

# * ======== TESTES DO POST ========
def teste_POST_Cenario1():
    registroJson = {
        'cpf' : "1234567891",
        'datadeNascimento' : "14/11/2003",
        'nomeCompleto' : "Georges Ballsiter de Oliveira",
        'email' : "Georgesballister@gmail.com",
        'telefone' : "81996732522",
        'sexo' : "M"   
    }
    res = requests.post(f"{URLAPI}/users/register", json=registroJson)
    
    if res.status_code == 201:
        return print(f"TESTE POST - (teste_POST_Cenario1) sucesso ✅ {res.status_code}")
    else:
        return print(f"TESTE POST - (teste_POST_Cenario1) ERRO! 🚫 {res.status_code}")
        

# * ======== TESTES DO GET ========

# Get ALL
def PuxarTodosOSDADOS():
    res = requests.get(f"{URLAPI}/users/all")
    
    if res.status_code == 200:
        return print(f"TESTE GET - (GetALLUSERS) sucesso ✅ {res.status_code}")
    else:
        return print(f"TESTE GET - (GetALLUSERS) ERRO! 🚫 {res.status_code}")
    
# GET BY CPF 
def PuxarUsuarioPeloCPF():
    bodyJSON = {
        "cpf" : "1234567891",
        'datadeNascimento' : "14/11/2003"
    }
    
    res = requests.get(f"{URLAPI}/users/find", params=bodyJSON)
    
    if res.status_code == 200:
        return print(f"TESTE GET - (Puxar Usuario Pelo CPF) sucesso ✅ {res.status_code}")
    else:
        return print(f"TESTE GET - (Puxar Usuario Pelo CPF) ERRO! 🚫 {res.status_code}")
# * ======== TESTES DO PUT ========
def AtualziarDado():
    id = '1'
    bodyJson = {
        
        'cpf' : "000000123123",
        'datadeNascimento' : "14/11/2003",
        'nomeCompleto' : "Calabreuson Da Silva",
        'email' : "ohhhhhMyGod@gmail.com",
        'telefone' : "81996732522",
        'sexo' : "M"  
        
    }
    
    res = requests.put(f"{URLAPI}/users/{id}", json=bodyJson)
    
    if res.status_code == 200:
        return print(f"TESTE PUT - (Atualizar Dados) sucesso ✅ {res.status_code}")
    else:
        return print(f"TESTE PUT - (Atualizar Dados) ERRO! 🚫 {res.status_code}")

# * ======== TESTES DO DELETE ========
def RemoverDado():
    id = '1'
    res = requests.delete(f"{URLAPI}/users/{id}")
    
    if res.status_code == 200:
        return print(f"TESTE DELETE - (Deletar Registro) sucesso ✅ {res.status_code}")
    else:
        return print(f"TESTE DELETE - (Deletar Registro) ERRO! 🚫 {res.status_code}")

# * ======== EXECUÇÃO DOS TESTES ========

# Significa que esses comando a baixo somente serão executados se, esse arquivo for rodado diretamene
if __name__ == "__main__":
    testar_mock()
    teste_POST_Cenario1()
    PuxarTodosOSDADOS()
    PuxarUsuarioPeloCPF()
    AtualziarDado()
    RemoverDado()