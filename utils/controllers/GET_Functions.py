# Aqui contera todas as funções remetentes aos endpoints: POST

# * Bibliotecas e Modulos
from flask import jsonify, request
from utils.modules.NormalizadorDeDados import normaliza_cpf
from utils.modules.ManipulacaoDoDB import load_data
# ! A sobrecarga de metodo/parametro "dadosDB" EM TODAS as funções deve ser preenchida com a variavel "DADOSBD" do arquivo APP.PY, pois ele ira interagir com o arquivo "allData.json".

def encontrarUsuario_PeloCPF_E_DataDeNAS(dadosDB):
    
    todos_os_dados_DB = load_data(dadosDB)
    
    cpf = request.args.get('cpf').strip().lower()
    datadeNascimento  = request.args.get('datadeNascimento').strip().lower()
    
    cpf = normaliza_cpf(cpf)

    for registro in todos_os_dados_DB:
    
        cpf_Registrado = str(registro.get('cpf', '')).strip().lower()
        datadeNascimento_Registrado = str(registro.get('datadeNascimento', '')).strip().lower()
        
        if cpf_Registrado == cpf and datadeNascimento_Registrado == datadeNascimento:
            return jsonify({
                "mensage" : registro
            }), 200
        
    return jsonify({
        "Erro" : "Usuario nao encontrado, verifique sua requisicao"
    }), 404
            
    


def todosOsUsuarios(dadosDB):
    
    todos_os_dados_DB = load_data(dadosDB)
    
    if not todos_os_dados_DB:
        return jsonify({"message": "Nenhum usuário cadastrado"}), 200
    return jsonify({"usuarios": todos_os_dados_DB}), 200