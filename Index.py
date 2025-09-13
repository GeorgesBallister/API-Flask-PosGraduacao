# Bibliotecas que vou usar para fazer a construção da API (FLASK)
from flask import Flask, request, jsonify
from flask_cors import CORS


# ! ====================== MODULES ======================
# * Bem, aqui resolvi separa todos as "funções (def)" que os endpoints executam em modulos todos organizados dentro da pasta utils, podendo ter assim um controle muito mais versatil de como cada função vai interagir com o meu ambiente da API, isolando todos os problemas em seus respectivos lugares e adotando alguns dos conceitos abordados pelo livro "Codigo Limpo", só que aplicado ao contexto do meu ambiente e tecnologia.

# * Dito isto, todas as novas funções que forem criadas devem seguir esta "regra de negocio" para que se mantenha o ambiente organizado e facilite a manutenibilidade.

# Puxa as funções do modulo para carregar o mock
from utils.modules.ManipulacaoDoDB import load_mock

# Modulo para funções de POST
from utils.controllers.POST_Functions import RegistrarNovoUsuario

# Modulo para funções de GET
from utils.controllers.GET_Functions import encontrarUsuario_PeloCPF_E_DataDeNAS, todosOsUsuarios

# Modulo para funções de PUT
from utils.controllers.PUT_Functions import AtualizarRegistroPorID

# Modulo para funções de PUT
from utils.controllers.DELETE_Functions import ApagarDadosPorID

# ! Instância Flask e Nome da API
app = Flask("API-SENAC") 


# "Banco" este pseudo banco de dados NOSQL vai ser por completo concentrado dentro de um arquivo JSON, utilizando de sua estrutura versatio, eu consegui desenvolver todos os conceitos do CRUD dento da arquitetura de uma REST API, com todos os HTTP METHODS interagindo com este arquivo atraves dos endpoints
DADOSBD = "Dados/DataBase.json"



# ! ====================== Endpoints ======================

## === MOCK DE DADOS FICTICIOS ===
@app.route('/mock', methods={"POST"})
def enviarMock():
    return load_mock(DADOSBD);


## === HTTP POST's ===

@app.route('/users/register', methods=['POST'])
def register_user():
   return RegistrarNovoUsuario(DADOSBD);

## === HTTP GET's ===


@app.route('/users/find', methods=['GET'])
def find_user():
    return encontrarUsuario_PeloCPF_E_DataDeNAS(DADOSBD)

@app.route('/users/all', methods=['GET'])
def get_all_users():
   return todosOsUsuarios(DADOSBD)


## === HTTP PUT's ===

@app.route('/users/<id_str>', methods=['PUT'])
def update_user(id_str):
    return AtualizarRegistroPorID(DADOSBD, id_str)

## === HTTP DELETE's ===

@app.route('/users/<id_str>', methods=['DELETE'])
def delete_user(id_str):
    return ApagarDadosPorID(DADOSBD, id_str)


# ! Rodar API
if __name__ == '__main__':
    # Ajuste a porta/host se necessário
    app.run(host='127.0.0.1', port=5000, debug=True)
