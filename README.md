## API correspondente a nota final da disciplina Programação de Computadores - Centro Universitário de João Pessoa(Unipê)

##### Esta aplicação permite visualizar o crescimento da frota de veículos em uma cidade específica, com base no código do IBGE obtido a partir de um CEP da localidade. Ela faz isso obtendo dados da API ViaCep(https://viacep.com.br/), passando um CEP como argumento, em seguida os dados são separados, pois apenas o código do ibge da cidade e seu nome nos interessam, com esses parâmetros, fazemos uma requisição a API do IBGE(https://servicodados.ibge.gov.br/api/docs/pesquisas). Com os dados obtidos, criamos um DataFrame(https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) para este ser consumido pela library do Matplotlib(https://matplotlib.org/stable/index.html) e plotar um gráfico para que possamos observar o crescimento ou decaimento da frota de veículos da cidade que se deseja analisar.

### Estrutura do projeto
```
/projeto
│-- /api
│   │-- library.py
│   │-- main.py
│-- /data
│-- requirements.txt
│-- .gitignore
```

### Procedimentos Para Execução do Projeto

##### Clone o Projeto
```git clone https://github.com/marciodelfinooliveira/ProceduralPythonProject.git
```

##### Crie uma Virtual Environment
```python3 -m venv venv -- Para sistemas UNIX
```

##### Ative a VENV
```source venv/bin/activate -- Para sistemas UNIX
```

##### Instale as libs necessárias
```pip install -r requirements.txt
```

##### Execute o sistema via Streamlit
```streamlit run ./api/main.py
```



