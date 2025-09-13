# Aqui contera todas as funções remetentes aos endpoints: POST

# * Bibliotecas e Modulos
from flask import jsonify, request
from utils.modules.NormalizadorDeDados import normaliza_cpf
from utils.modules.GerarID import gerarID
from utils.modules.ManipulacaoDoDB import save_data, load_data


# ! A sobrecarga de metodo/parametro "dadosDB" EM TODAS as funções deve ser preenchida com a variavel "DADOSBD" do arquivo APP.PY, pois ele ira interagir com o arquivo "allData.json".


def RegistrarNovoUsuario(DADOSBD):
    # 1: Ler o Banco e armazenar
    registros_Do_DB = load_data(DADOSBD);

    # 2: Armazenar o escopo do body JSON do HTTP Request
    dadosDoBody = request.get_json() or {}
    
     
    # 3: Define os dados obrigatorios dentro do escopo do JSON
    listaDeDadosObrigatorios = ['cpf','datadeNascimento','nomeCompleto','email','telefone','sexo'];
   
    # 4: Verificação dos dados obrigatorios dentro do escopo do JSON

    if any( # 4.5: Aqui ele verificar se qualquer um dos dadps array que esse loop gerou tem pelomenos 1 item "TRUE", se ele tiver esse if é executado.
        
        dadoObrigatorio not in dadosDoBody  # 4.2: Depois ele vai verificar a cada loop que ele passar se esses campos NÃO estão dentro do escopo do JSON no body (Retornando True)

        or not dadosDoBody[dadoObrigatorio] # 4.3: Se o campo existir ele verificara se o campo esta sem qualquer tipo de valor (Tambem retornando "True")

        for dadoObrigatorio in listaDeDadosObrigatorios # 4.1: Percorre por toda a lista que contem todos os dados que serão obrigatorios, armazenando qual informação ele vai verificar naquele loop.

        # 4.4: Por fim ele gera um array de boolean para cada item da "listaDeDadosObrigatorios"
        # True = Campo não exite
        # False = Campo existe
        ):
        
        # 4.6: Retona o erro caso algum campo obrigatorio não tenha sido passado no body
        return jsonify({"error": "Dados inválidos: Todos os campos são obrigatórios", "campos_obrigatorios": listaDeDadosObrigatorios}), 400
    
        # 4-Recaptulado:
        """
        1- Ele vai pegar os dois campos que foi passado como obrigatorio 'nome' e 'email', que estão armazenados dentro da variavel "listaDeDadosObrigatorios".

        2- Depois ele vai pegar esses campos e passar uma checagem de ler 1 dado obrigatorio por vez e verificar se ele esta NÃO esta presente no escopo do body do HTTP Request.
        
        3- Se o respectivo campo NÃO EXISTIR ele vai passar nesse teste e vai retornar como TRUE, se o campo EXISTIR ele vai falhar no teste e rentornar como FALSE.

            3.1 - Gerando assim por exemplo se o campo nome existir dentro do body mais o email não ele ficaria assim [False, True]

        4. Se no final do teste de todos os campos obrigatorios existir pelomenos um True("Aquele dado não esta no body do HTTP Request") ele retornara a mensagem de erro 400.

        4.1 Se todos os campos forem falsos ele vai passar pular este erro. 
        """

    # 5: Verifica se já existe aquele email dentro da base de dados
    # 5.1: Um loop é utilizado para percorrer cada um dos itens dentro da lista de registros_Do_DB 
    for registro in registros_Do_DB:
        
        # 5.2: Verifica da seguinte forma:
        # Ele vai comparar dois valores
        # Valor 1: O dado da key "email", do registro do banco de dados daquele momento do loop, formatado com todas as letras minusculas
        # Valor 2: O dado da key "email", do body do HTTP Request, formatado com todas as letras minusculas.
        if registro.get("email", "").strip().lower() == dadosDoBody["email"].strip().lower():
            # 5.3: Se pelomenos 1 comparação retortnar como True, ele ira executar esta mensagem de erro 409 (Conflito), senão ele so vai pular esta linha
            return jsonify({"error": "Este email já esta cadastrado em nosso sistema, por favor tente outro ."}), 409



    
    # 6. Normaliza os dados do CPF para o Padrão
    dadosDoBody['cpf'] = normaliza_cpf(dadosDoBody['cpf'])

    # ! Gerando ID unico
    # 7: Aqui ele vai gerar um novo ID, utilizando da função presente no modulo utils.modules.GerarID 
    idNovo = gerarID(DADOSBD)

    # 8: Vai agregar o novo ID a key 'id' dentro no escopo do body
    dadosDoBody["id"] = idNovo

    # 9: Verifica Duplicidade do CPF
    # 9.1: Um loop é utilizado para percorrer cada um dos itens dentro da lista de registros_Do_DB 
    for registro in registros_Do_DB:
        
         # 9.2: Verifica da seguinte forma:
        # Ele vai comparar dois valores
        # Valor 1: O dado da key "cpf", do registro do banco de dados daquele momento do loop, formatado sem espaços.
        # Valor 2: O dado da key "cpf", do body do HTTP Request, fformatado sem espaços.
        if registro.get("cpf").strip().lower() == dadosDoBody.get("cpf").strip().lower():
             # 9.3: Se pelomenos 1 comparação retortnar como True, ele ira executar esta mensagem de erro 409 (Conflito), senão ele so vai pular esta linha
            jsonify({
                "Erro" : "Este CPF já existe em nossa base de dados"
            }), 409

    # 10: Registar usuario no arquico JSON
    save_data(dadosDoBody, DADOSBD);
    return jsonify({
        "mensage" : f"Usuario {dadosDoBody["nomeCompleto"]} criado com suceso"
    }), 201