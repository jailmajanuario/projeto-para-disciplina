# Snowballing Forward

Ferramenta interativa para triagem automática e aplicação de critérios em revisões sistemáticas da literatura.

## Funcionalidades

- Importação de artigos via Semantic Scholar
- Marcação de artigos como "incluir", "excluir" ou "talvez"
- Aplicação automática de critérios com LLM (Google Gemini)
- Exportação dos resultados em CSV
- Visualizações com gráficos por ano e por venue

## Como rodar localmente

1. Clone o repositório:

```bash
git clone https://github.com/jailmajanuario/projeto-para-disciplina.git
cd projeto-para-disciplina

2. Instale as dependências:

npm install

3. Configure a chave da API Gemini:

Abra o arquivo analisa.py

Substitua "insira sua chave" pela sua chave real

4. Inicie a aplicação:

node app.js

5. Acesse no navegador:
http://localhost:3000
