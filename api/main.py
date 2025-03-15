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
    Função principal que executa o fluxo do programa.
    """
    while True:
        try:
            responseViaCep = requestGetToViaCep(inputCep())
            
            localidade = filterIbgeCodeInResponse(responseViaCep, 'localidade')
            codeIbge = setString(filterIbgeCodeInResponse(responseViaCep, 'ibge'))
            
            dataFrame = prepareDataFrame(requestGetToIbge(codeIbge))

            plotGraph(dataFrame, codeIbge, localidade)
            break
        
        except ValueError as e:
            raise ValueError(f"Erro: {str(e)}")
        
        except Exception as e:
            raise Exception(f"Erro inesperado ao executar o sistema: {str(e)}")
        
main() if (__name__ == "__main__") else exit