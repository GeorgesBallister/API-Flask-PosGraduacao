# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# "Banco" em memória
users = {}  

def normaliza_cpf(cpf: str) -> str:
    return ''.join(ch for ch in cpf if ch.isdigit())

@app.route('/users/register', methods=['POST'])
def register_user():
    data = request.get_json() or {}
    obrig = ['cpf','datadeNascimento','nomeCompleto','email','telefone','sexo']
    if any(c not in data or not data[c] for c in obrig):
        return jsonify({"error": "Dados inválidos: Todos os campos são obrigatórios", "campos_obrigatorios": obrig}), 400

    # normaliza entradas
    data['cpf'] = normaliza_cpf(data['cpf'])

    # regra simples para id
    novo_id = max([u["idDoUsuario"] for u in users.values()], default=0) + 1
    data['idDoUsuario'] = novo_id

    # previne duplicidade por cpf + data nasc
    for u in users.values():
        if u['cpf'] == data['cpf']:
            return jsonify({"error": "Usuário já cadastrado (CPF) ."}), 409

    users[str(novo_id)] = data
    return jsonify({"message": "Usuário cadastrado com sucesso!", "usuario": data}), 201

@app.route('/users/find', methods=['GET'])
def find_user():
    cpf = request.args.get('cpf', '')
    datadeNascimento  = request.args.get('datadeNascimento', '')
    if not cpf or not datadeNascimento:
        return jsonify({"error": "Informe cpf e datadeNascimento na query string"}), 400

    cpf = normaliza_cpf(cpf)
    for u in users.values():
        if u['cpf'] == cpf and u['datadeNascimento'] == datadeNascimento:
            return jsonify({"usuario": u}), 200

    return jsonify({"message": "Usuário não encontrado"}), 404

# NOVA ROTA - retorna todos os registros
@app.route('/users/all', methods=['GET'])
def get_all_users():
    if not users:
        return jsonify({"message": "Nenhum usuário cadastrado"}), 200
    return jsonify({"usuarios": list(users.values())}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
