# LigaMagic Price Tracker

Este projeto automatiza a extração de preços de cartas do site LigaMagic e os organiza em uma planilha Excel para acompanhamento.

## Requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Microsoft Excel instalado
- Conta no site LigaMagic
- Conexão com a internet

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/ligamagic-price-tracker.git
cd ligamagic-price-tracker
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```


## Como Usar

### Preparação

1. Certifique-se de que o Google Chrome está instalado
2. Faça login manualmente no site LigaMagic usando o Chrome
3. Mantenha a sessão ativa

Importante que o deck comece com **"Pool"**, senão o bot vai ignorar.
### Execução

O processo é dividido em duas etapas:

1. **Executar o Scraping**:
```bash
python 1-run-scrapping.py
```
Este comando irá:
- Acessar o site LigaMagic
- Extrair os dados das cartas
- Salvar os dados em um arquivo JSON na pasta `output`

2. **Atualizar o Excel**:
```bash
python 2-run-excel.py
```
Este comando irá:
- Ler o arquivo JSON gerado
- Atualizar a planilha Excel com os novos dados
- Aplicar formatação e cores

### Estrutura do Excel

A planilha gerada terá:
- Coluna "Nome da Carta" 
- Coluna "Quantidade"
- Colunas de datas com preços
- Cores:
  - Verde: preço aumentou
  - Vermelho: preço diminuiu
  - Branco: preço manteve

### Observações Importantes

1. **Login no LigaMagic**:
   - É necessário estar logado manualmente no Chrome
   - A sessão deve estar ativa durante a execução
   - O bot usa a sessão existente, não faz login automaticamente

2. **Excel**:
   - Deve estar instalado na máquina
   - A planilha é salva em `output/pool.xlsx`
   - Os dados são organizados por data

3. **Segurança**:
   - Mantenha suas credenciais seguras no arquivo `.env`
   - Não compartilhe o arquivo `.env`
   - O arquivo `.env` está no `.gitignore` por padrão

## Estrutura do Projeto

```
ligamagic-price-tracker/
├── src/
│   ├── core/
│   │   ├── scraper.py      # Lógica de scraping
│   │   ├── portal.py       # Interação com o site
│   │   └── excel_handler.py # Manipulação do Excel
│   └── main.py             # Script principal
├── output/
│   ├── cards.json          # Dados extraídos
│   └── pool.xlsx           # Planilha de preços
├── .env                    # Configurações (não versionado)
├── requirements.txt        # Dependências
└── README.md              # Este arquivo
```

## Solução de Problemas


1. **Erro no Excel**:
   - Verifique se o Excel está instalado
   - Confirme se o arquivo não está aberto durante a execução

2. **Erro de Conexão**:
   - Verifique sua conexão com a internet
   - Confirme se o site LigaMagic está acessível

