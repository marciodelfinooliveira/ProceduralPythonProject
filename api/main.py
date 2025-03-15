import requests


def inputCep() -> str:
    """
    O método solicita ao usuário que insira um CEP e verifica se o valor inserido
    é uma string de no máximo 8 dígitos e contém apenas números, caso o CEP seja
    inválido uma exception é levantada.

    @return: Retorna o CEP válido inserido pelo usuário.
    @rtype: str

    @raises ValueError: Se o CEP inserido não for uma string de 8 dígitos numéricos.
    @raises Exception: Se ocorrer um erro inesperado durante a execução do método.
    """
    try:
        cep = input("Insira o número do CEP para consulta: ")
        
        if len(cep) != 8 or not cep.isdigit():
            raise ValueError("CEP inválido. O CEP deve conter exatamente 8 dígitos numéricos.")
        return cep
    
    except Exception as e:
        raise Exception(f"Erro ao fazer a requisição: {e}")


def requestGetToViaCep(cep: str) -> dict:
    """
    O método faz uma requisição GET à API do ViaCEP e verifica se o CEP fornecido
    é válido e foi encontrado, caso a resposta esteja vazia ou o CEP não seja encontrado,
    uma exceção é levantada com uma mensagem de erro apropriada.

    @param cep: Uma string representando o CEP a ser consultado.
    @type cep: str
    @return: Retorna um dicionário com os dados do CEP se a resposta for válida.
    @rtype: dict

    @raises ValueError: Se o CEP não for encontrado ou a resposta da API for inválida.
    @raises requests.exceptions.RequestException: Se ocorrer um erro durante a requisição HTTP.
    @raises Exception: Se ocorrer um erro inesperado durante a execução do método.
    """
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        
        if response.status_code != 200 or 'erro' in response.json():
            raise ValueError(f"CEP {cep} não encontrado ou resposta inválida.")
        return response.json()
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao fazer a requisição: {e}")
    
    except ValueError as e:
        raise ValueError(f"Erro ao processar a resposta: {e}")
    
    except Exception as e:
        raise Exception(f"Erro inesperado: {e}")


def filterCityInResponse(dicionario: dict) -> str:
    """
    O método verifica se a chave 'localidade' está presente no dicionário e retorna
    o valor associado a essa chave, caso a chave não exista ou ocorra algum erro,
    uma exceção é levantada.

    @param dicionario: Dicionário contendo os dados retornados do ViaCep.
    @type dicionario: dict

    @return: Valor correspondente à chave 'localidade'.
    @rtype: str

    @raises KeyError: Se a chave 'localidade' não estiver presente no dicionário.
    @raises Exception: Se ocorrer um erro inesperado durante a execução do método.
    """
    try:
        if 'localidade' in dicionario:
            return dicionario['localidade']            
        raise KeyError("A chave 'localidade' não foi encontrada no dicionário.")
    
    except Exception as e:
        raise Exception(f"Erro ao filtrar a localidade: {e}")


