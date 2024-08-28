# Desafio Cogni

## Descrição

O desafio da Cogni consiste em criar uma solução para baixar segunda via de faturas de energia (boleto pdf/xml) do portal da sua concessionária local. No meu caso, a concessionária é a [Neoenergia Pernambuco](https://servicos.neoenergiapernambuco.com.br/Pages/todos-os-servicos.aspx).

## Solução

Para resolver o desafio, criei um script em Python que acessa o portal da Neoenergia Pernambuco, preenche o formulário de segunda via de fatura com os dados do cliente e baixa o boleto em formato PDF.

Para isso, utilizei a biblioteca [Selenium](https://selenium-python.readthedocs.io/) para automatizar o navegador

## Como usar

1. Instale o [Python](https://www.python.org/downloads/) e o [Google Chrome](https://www.google.com/intl/pt-BR/chrome/).

2. Clone o repositório:

```bash
git clone https://github.com/LucasGdBS/desafio-Cogni.git
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie o arquivo .env com os dados do cliente de acordo com o arquivo .env.example:

5. Execute o script:

```bash
python main.py
```

A 2ª Via do boleto irá para a pasta "downloads" na raiz do projeto

## Observações

- Para o script funcionar corretamente, é necessário ter na sua maquina o Chrome WebDriver
