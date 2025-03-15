import streamlit as st
import logging
import os
from library import (
    inputCep,
    requestGetToViaCep,
    filterIbgeCodeInResponse,
    requestGetToIbge,
    prepareDataFrame,
    setString,
    plotGraph,
    saveIbgeResponse
)

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/app.log',
    level=logging.DEBUG,
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
        Esta aplicação permite visualizar o crescimento da frota de veículos em uma cidade específica, 
        com base no código do IBGE obtido a partir de um CEP da localidade.
    """)

    cep = st.text_input("Digite o CEP:", placeholder="Ex: 99999-999")

    if st.button("Buscar Dados"):
        if not cep:
            st.error("Por favor, insira um CEP válido.")
            logger.warning("CEP não foi inserido.")
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
        
main() if (__name__ == "__main__") else exit