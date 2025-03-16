import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
import logging

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


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
            logger.info("CEP inválido. O CEP deve conter exatamente 8 dígitos numéricos.")
            raise ValueError("CEP inválido. O CEP deve conter exatamente 8 dígitos numéricos.")
        
        return cep
    except Exception as e:
        logger.info(f"Erro ao fazer a requisição: {e}")
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
        
        if response.status_code != 200:
            logger.info(f"CEP {cep} não encontrado ou resposta inválida.")
            raise ValueError(f"CEP {cep} não encontrado ou resposta inválida.")
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.info(f"Erro ao fazer a requisição: {e}")
        raise Exception(f"Erro ao fazer a requisição: {e}")
    except ValueError as e:
        logger.info(f"Erro ao processar a resposta: {e}")
        raise ValueError(f"Erro ao processar a resposta: {e}")
    except Exception as e:
        logger.info(f"Erro inesperado: {e}")
        raise Exception(f"Erro inesperado: {e}")
    

def setString(cityCode: str) -> str:
    """
    Remove o último caractere de uma string que representa o código da cidade
    para ajusta-lo ao parametro esperado da API do IBGE.

    @param cityCode: O código da cidade como uma string.
    @type cityCode: str
    @return: O código da cidade sem o último caractere.
    @rtype: str

    @raises ValueError: O parametro não foi enviado
    @raises Exception: Erro ao processar o parametro 
    """
    try:
        if not cityCode:
            logger.info(f"O código não foi enviado: {e}")
            raise ValueError(f"O código não foi enviado: {e}")
        
        return cityCode[:-1]
    except Exception as e:
        logger.info(f"Erro ao processar o código da cidade: {str(e)}")
        raise Exception(f"Erro ao processar o código da cidade: {str(e)}")
    

def filterIbgeCodeInResponse(dict: dict, key: str) -> str:
    """
    O método verifica se a chave 'ibge' está presente no dicionário e retorna
    o valor associado a essa chave, caso a chave não exista ou ocorra algum erro,
    uma exceção é levantada.

    @param dict: Dicionário contendo os dados retornados do ViaCep.
    @type dict: dict

    @return: Valor correspondente à chave 'ibge'.
    @rtype: str

    @raises KeyError: Se a chave 'ibge' não estiver presente no dicionário.
    @raises Exception: Se ocorrer um erro inesperado durante a execução do método.
    """
    try:
        if key in dict: return dict[key]            
        logger.info("A chave 'ibge' não foi encontrada no dicionário.")
        raise KeyError("A chave 'ibge' não foi encontrada no dicionário.")
    
    except Exception as e:
        logger.info(f"Erro ao filtrar a ibge: {e}")
        raise Exception(f"Erro ao filtrar a ibge: {e}")
    

def requestGetToIbge(code: str) -> dict:
    """
    Método que faz uma requisição à API do IBGE usando o código IBGE.

    @param code: Código IBGE da localidade.
    @type code: str

    @return: Dicionário com os dados retornados pela API do IBGE.
    @rtype: dict

    @raises Exception: Se ocorrer um erro durante a requisição ou processamento.
    """
    try:
        response = requests.get(f'https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/28122/resultados/0%7C{code}')
        
        if response.status_code != 200:
            logger.info(f"Erro ao fazer a requisição à API do IBGE: {e}")
            raise ValueError(f"Erro ao fazer a requisição à API do IBGE: {e}")
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.info(f"Erro ao fazer a requisição: {e}")
        raise Exception(f"Erro ao fazer a requisição: {e}")
    except ValueError as e:
        logger.info(f"Erro ao processar a resposta: {e}")
        raise ValueError(f"Erro ao processar a resposta: {e}")
    except Exception as e:
        logger.info(f"Erro inesperado: {e}")
        raise Exception(f"Erro inesperado: {e}")


def prepareDataFrame(responseJson: list) -> pd.DataFrame:
    """
    Método que transforma o JSON de resposta da API do IBGE em um DataFrame, ignorando a localidade '0' (Brasil).

    @param responseJson: Lista contendo o JSON de resposta da API. O JSON deve ter a estrutura esperada, com dados de localidades e anos.
    @type responseJson: list

    @return: DataFrame contendo as colunas 'Localidade', 'Ano' e 'Valor'. Apenas os dados da cidade determinada na resposta (localidade != '0') são incluídos.
    @rtype: pd.DataFrame

    @raises ValueError: Se o JSON de resposta estiver vazio ou não contiver a estrutura esperada.
    @raises KeyError: Se o JSON não tiver as chaves esperadas, como 'res' ou 'localidade'.
    @raises TypeError: Se os valores não puderem ser convertidos para inteiros.
    """
    try:
        if not responseJson:
            logger.info("O JSON de resposta está vazio.")
            raise ValueError("O JSON de resposta está vazio.")

        localidades = []
        anos = []
        valores = []

        for entry in responseJson[0]['res']:
            localidade = entry['localidade']

            if localidade == '0':
                continue
            res_data = entry['res']

            for ano, valor in res_data.items():
                localidades.append(localidade)
                anos.append(int(ano))
                valores.append(int(valor))

        dataFrame = pd.DataFrame({
            'Localidade': localidades,
            'Ano': anos,
            'Valor': valores
        })

        return dataFrame
    except KeyError as e:
        logger.info(f"Erro: Chave ausente no JSON - {str(e)}")
        raise KeyError(f"Erro: Chave ausente no JSON - {str(e)}")
    except TypeError as e:
        logger.info(f"Erro: Falha ao converter valores para inteiros - {str(e)}")
        raise TypeError(f"Erro: Falha ao converter valores para inteiros - {str(e)}")
    except Exception as e:
        logger.info(f"Erro inesperado ao processar o JSON: {str(e)}")
        raise Exception(f"Erro inesperado ao processar o JSON: {str(e)}")
    

def plotGraph(df: pd.DataFrame, codeIbge: str, cityName: str):
    """
    Método que plota um gráfico usando Matplotlib, mostrando os valores de uma cidade específica ao longo dos anos.

    @param df: DataFrame contendo as colunas 'Localidade', 'Ano' e 'Valor'.
    @type df: pd.DataFrame
    @param codeIbge: Código da cidade a ser exibida no gráfico.
    @type codeIbge: str
    @param cityName: Nome da cidade a ser exibido no gráfico.
    @type cityName: str
    """
    try:
        # Filtra os dados apenas para a cidade
        df_cidade = df[df['Localidade'] == codeIbge]

        # Verifica se há dados para a cidade
        if df_cidade.empty:
            logger.info(f"Nenhum dado encontrado para {cityName}.")
            raise ValueError(f"Nenhum dado encontrado para {cityName}.")

        # Cria o gráfico
        fig, ax = plt.subplots(figsize=(12, 7))
        ax.plot(df_cidade['Ano'], df_cidade['Valor'], label=cityName, marker='o', linestyle='-', linewidth=2, color='blue')

        # Configurações do gráfico
        ax.set_title(f'Histórico da Frota de Veículos para {cityName}', fontsize=16)
        ax.set_xlabel('Ano', fontsize=14)
        ax.set_ylabel('Quantidade de Veículos', fontsize=14)

        # Desativa a notação científica no eixo y
        ax.ticklabel_format(axis='y', style='plain')

        # Formata os rótulos do eixo y com separadores de milhares
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

        # Define os rótulos do eixo x para mostrar todos os anos
        ax.set_xticks(df_cidade['Ano'])
        ax.tick_params(axis='x', rotation=45)

        # Adiciona legendas e grid
        ax.legend(fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)

        # Ajusta o layout para evitar cortes
        plt.tight_layout()

        return fig
    except ValueError as e:
        logger.info(f"Erro: {str(e)}")
        raise ValueError(f"Erro: {str(e)}")
    except KeyError as e:
        logger.info(f"Erro: Chave ausente no DataFrame - {str(e)}")
        raise KeyError(f"Erro: Chave ausente no DataFrame - {str(e)}")
    except Exception as e:
        logger.info(f"Erro inesperado ao plotar o gráfico: {str(e)}")
        raise Exception(f"Erro inesperado ao plotar o gráfico: {str(e)}")
    

def saveIbgeResponse(df: pd.DataFrame, cityName: str) -> str:
    """
    Método que salva o DataFrame em um arquivo .xlsx na pasta 'data'.

    @param df: DataFrame a ser salvo.
    @type df: pd.DataFrame
    @param cityName: Nome da localidade buscada.
    @type cityName: str

    @return: Caminho do arquivo salvo.
    @rtype: str

    @raises Exception: Se ocorrer um erro ao salvar o arquivo.
    """
    try:
        if not os.path.exists('data'):
            os.makedirs('data')

        file = os.path.join('data', f'{cityName}.xlsx')
        logger.info(f"Salvando arquivo em: {file}")
        df.to_excel(file, index=False)

        return file
    except Exception as e:
        logger.error(f"Erro ao salvar o arquivo: {str(e)}")
        raise Exception(f"Erro ao salvar o arquivo: {str(e)}")
