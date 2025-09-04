# Bibliotecas
import random
import uuid

# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Um "banco de dados" simples para demonstração
users = {}

def gerar_id_unico(banco):
    while True:
        novo_id = random.randint(1,99999999999)
        
        if all(registro["idDoUsuario"] != novo_id for registro in banco.values()):
            return novo_id
        
        
        


# Nosos Banco
@app.route('/users/register', methods=['POST'])
def register_user():
    # Obtém os dados JSON da requisição
    data = request.get_json()
    
    # Validação básica
    if not data or 'cpf' not in data or 'datadeNascimento' not in data or 'nomeCompleto' not in data or 'email' not in data or 'telefone' not in data or 'sexo' not in data:
        return jsonify({"error": "Dados inválidos: Todos os campos são obrigatórios"}), 400
    
    # Campos
    nomeCompleto = data['nomeCompleto']
    cpf = data['cpf']
    datadeNascimento = data['datadeNascimento'] 
    email = data['email']
    telefone = data['telefone']
    sexo = data['sexo']
    
    # Verifica se o usuário já existe
    if any(registro["cpf"] == cpf for registro in users.values()):
        return jsonify({"error": "Usuário já existe"}), 409

    idDoUsuario = gerar_id_unico(users)
   
    # "Salva" o novo usuário
    users[idDoUsuario] = { "idDoUsuario" : idDoUsuario, "nomeCompleto" : nomeCompleto, "cpf" : cpf, "datadeNascimento" : datadeNascimento, "telefone" : telefone, "email" : email, "sexo" : sexo}

    # Retorna uma resposta de sucesso
    return jsonify({"message": f"Usuário '{nomeCompleto}' cadastrado com sucesso!"}), 201

# --- Buscar dados de um usuário ---
@app.route('/users/<cpf>/<datadeNascimento>', methods=['GET'])
def get_user(cpf, datadeNascimento):
    
    for usuario in users.values():
        if usuario["cpf"] == cpf and usuario["datadeNascimento"] == datadeNascimento:
            return jsonify(usuario), 200
    
    return jsonify({"error": "Usuário não encontrado"}), 404


# --- Puxa tudo do Banco de Dados ---
@app.route('/users/all', methods=['GET'])
def get_all_users():
   
    dados_do_Usuario = users
        # Cria uma cópia dos dados para não enviar a senha
    user_info_to_send = dados_do_Usuario.copy()
        
        # Você pode adicionar mais dados aqui, como 'email', 'nome', etc.
        # Por exemplo: user_info_to_send['email'] = 'exemplo@teste.com'
        
    return jsonify(user_info_to_send), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
