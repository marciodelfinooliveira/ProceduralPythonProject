from library import (
    inputCep,
    requestGetToViaCep,
    filterIbgeCodeInResponse,
    requestGetToIbge,
    prepareDataFrame
)

def main():
    """
    Função principal que executa o fluxo do programa.
    """
    while True:
        try:
            responseViaCep = requestGetToViaCep(inputCep())
            
            localidade = filterIbgeCodeInResponse(responseViaCep, 'localidade')
            ibge = filterIbgeCodeInResponse(responseViaCep, 'ibge')
            
            responseIbge = requestGetToIbge(ibge)

            dataFrame = prepareDataFrame(responseIbge)

            print(dataFrame)
            break
        
        except ValueError as e:
            print(e)
        
        except Exception as e:
            print(e)

main() if (__name__ == "__main__") else exit