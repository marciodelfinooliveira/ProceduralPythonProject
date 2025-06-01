import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
import logging
import re

# Cria diretório de logs, caso não já exista
if not os.path.exists('logs'):
    os.makedirs('logs')

# Chamada da instância da lib referente aos logs.
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def checkCep(cep: str = None) -> str | None:
    """
    Valida um CEP fornecido como argumento. Aceita apenas valores numéricos de 8 dígitos 
    como '99999999' ou no formato '99999-999'. Retorna sempre o CEP apenas com números.
    
    @param cep: O CEP fornecido pelo usuário.
    @type cep: str
    
    @return: O CEP válido com apenas números ou None se for inválido.
    @rtype: str | None

    @raises Exception: Se ocorrer um erro inesperado durante a execução do método.
    """
    try:
        if not cep:
            return None

        cep_match = re.fullmatch(r"(\d{5})-?(\d{3})", cep)
        
        if cep_match:
            return f"{cep_match.group(1)}{cep_match.group(2)}"

        logger.info("CEP inválido. Deve conter 8 dígitos numéricos ou estar no formato 99999-999.")
        return None
    except Exception as e:
        logger.error(f"Erro ao processar o CEP: {str(e)}")
        raise Exception(f"Erro ao processar o CEP: {str(e)}")


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
        logger.info(f"Erro ao fazer a requisição: {str(e)}")
        raise Exception(f"Erro ao fazer a requisição: {str(e)}")
    except ValueError as e:
        logger.info(f"Erro ao processar a resposta: {str(e)}")
        raise ValueError(f"Erro ao processar a resposta: {str(e)}")
    except Exception as e:
        logger.info(f"Erro inesperado: {str(e)}")
        raise Exception(f"Erro inesperado: {str(e)}")
    

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
            logger.info(f"O código não foi enviado: {str(e)}")
            raise ValueError(f"O código não foi enviado: {str(e)}")
        
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
                    
        logger.info("A chave 'ibge' não foi encontrada na response.")
        raise KeyError("A chave 'ibge' não foi encontrada na response.")
    
    except Exception as e:
        logger.info(f"O CEP Não existe: {str(e)}")
        raise Exception(f"O CEP Não existe: {str(e)}")
    

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
            logger.info(f"Erro ao fazer a requisição à API do IBGE: {str(e)}")
            raise ValueError(f"Erro ao fazer a requisição à API do IBGE: {str(e)}")
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.info(f"Erro ao fazer a requisição: {str(e)}")
        raise Exception(f"Erro ao fazer a requisição: {str(e)}")
    except ValueError as e:
        logger.info(f"Erro ao processar a resposta: {str(e)}")
        raise ValueError(f"Erro ao processar a resposta: {str(e)}")
    except Exception as e:
        logger.info(f"Erro inesperado: {str(e)}")
        raise Exception(f"Erro inesperado: {str(e)}")


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
