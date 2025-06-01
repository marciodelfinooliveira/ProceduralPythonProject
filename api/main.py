import streamlit as st
import logging
import os
import sys
from library import (
    checkCep,
    requestGetToViaCep,
    filterIbgeCodeInResponse,
    requestGetToIbge,
    prepareDataFrame,
    setString,
    plotGraph,
    saveIbgeResponse
)

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

def main():
    """
    Função principal que executa o fluxo do programa com interface Streamlit.
    """
    st.title("Análise de Frota de Veículos por Cidade")
    st.markdown("""
        Esta aplicação permite visualizar o crescimento da frota de veículos de uma cidade específica, 
        com base no código IBGE obtido a partir de um CEP da localidade.
    """)

    cepInput = st.text_input("Digite o CEP:", placeholder="Digite o CEP no Formato Padrão 99999-999 ou Numérico 99999999")
    cep = checkCep(cepInput) if cepInput else None

    if st.button("Buscar Dados"):

        if not cep:
            st.error("Por favor, insira um CEP válido.")
            logger.warning("O CEP inserido não é válido.")
        else:
            try:
                logger.info(f"Iniciando busca para o CEP: {cep}")

                responseViaCep = requestGetToViaCep(cep)
                logger.debug(f"Resposta da API ViaCEP: {responseViaCep}") 
                
                localidade = filterIbgeCodeInResponse(responseViaCep, 'localidade')
                codeIbge = setString(filterIbgeCodeInResponse(responseViaCep, 'ibge'))
                logger.info(f"Localidade encontrada: {localidade}, Código IBGE: {codeIbge}") 
                
                dataFrame = prepareDataFrame(requestGetToIbge(codeIbge))
                logger.debug(f"DataFrame gerado: {dataFrame.head()}")

                try:
                    file_path = saveIbgeResponse(dataFrame, localidade)
                    st.success(f"Dados salvos com sucesso em: {file_path}")
                    logger.info(f"Arquivo salvo em: {file_path}")
                except Exception as e:
                    st.error(f"Erro ao salvar os dados: {str(e)}")
                    logger.error(f"Erro ao salvar os dados: {str(e)}")

                st.success(f"Dados encontrados para a cidade: {localidade}")

                fig = plotGraph(dataFrame, codeIbge, localidade)
                st.pyplot(fig)

            except ValueError as e:
                st.error(f"Erro: {str(e)}")
                logger.error(f"Erro de valor: {str(e)}")
            except Exception as e:
                st.error(f"Erro inesperado ao executar o sistema: {str(e)}")
                logger.error(f"Erro inesperado: {str(e)}")

# Chamada da função 'main' via condição ternária, 
# garantindo a execução apenas quando (__name__ == "__main__") 
# ou seja, este script deve ser chamado diretamente, de outra forma
# será ignorado.
main() if (__name__ == "__main__") else sys.exit()