import streamlit as st
from library import (
    inputCep,
    requestGetToViaCep,
    filterIbgeCodeInResponse,
    requestGetToIbge,
    prepareDataFrame,
    setString,
    plotGraph
)

def main():
    """
    Função principal que executa o fluxo do programa com interface Streamlit.
    """
    st.title("Análise de Frota de Veículos por Cidade")
    st.markdown("""
        Esta aplicação permite visualizar o crescimento da frota de veículos em uma cidade específica, 
        com base no código do IBGE obtido a partir de um CEP da localidade.
    """)

    cep = st.text_input("Digite o CEP:", placeholder="Ex: 58052-310")

    if st.button("Buscar Dados"):
        if not cep:
            st.error("Por favor, insira um CEP válido.")
        else:
            try:
                responseViaCep = requestGetToViaCep(cep)
                
                localidade = filterIbgeCodeInResponse(responseViaCep, 'localidade')
                codeIbge = setString(filterIbgeCodeInResponse(responseViaCep, 'ibge'))
                
                dataFrame = prepareDataFrame(requestGetToIbge(codeIbge))

                st.success(f"Dados encontrados para a cidade: {localidade}")

                st.pyplot(plotGraph(dataFrame, codeIbge, localidade))

            except ValueError as e:
                st.error(f"Erro: {str(e)}")
            except Exception as e:
                st.error(f"Erro inesperado ao executar o sistema: {str(e)}")
        
main() if (__name__ == "__main__") else exit