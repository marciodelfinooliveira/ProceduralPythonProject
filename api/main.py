from library import (
    inputCep,
    requestGetToViaCep,
    filterIbgeCodeInResponse,
    requestGetToIbge
)

def main():
    """
    Função principal que executa o fluxo do programa.
    """
    while True:
        try:
            responseIbge = requestGetToIbge(filterIbgeCodeInResponse(requestGetToViaCep(inputCep())))
            break
        
        except ValueError as e:
            print(e)
        
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()