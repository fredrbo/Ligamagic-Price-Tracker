# RPA - Raspagem de Dados e Exportação para Excel

Este projeto é um RPA (Robotic Process Automation) desenvolvido em Python para realizar raspagem de dados e exportação para Excel.

## Estrutura do Projeto

```
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── scraper.py
│   │   └── excel_handler.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── data/
│   ├── input/
│   └── output/
├── logs/
├── tests/
├── .env
├── requirements.txt
└── main.py
```

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Configure as variáveis de ambiente no arquivo `.env`
2. Execute o script principal:
```bash
python main.py
```

## Funcionalidades

- Raspagem de dados de sites
- Exportação para Excel
- Logging de operações
- Configuração via variáveis de ambiente 