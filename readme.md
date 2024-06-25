# Uol Confere Spider

Este projeto contém um spider Scrapy chamado `UolSpider`, desenvolvido para rastrear e extrair informações do site "UOL Confere". O objetivo principal é analisar o impacto da desinformação nos direitos difusos como parte de um estudo preliminar financiado pelo Fundo de Direitos Difusos (FDD).

## O que é o Fundo de Direitos Difusos (FDD)?

O Fundo de Direitos Difusos (FDD) é um fundo administrado pelo Ministério da Justiça e Segurança Pública do Brasil. Ele visa financiar projetos que promovam a reparação de danos causados ao meio ambiente, ao consumidor, a bens e direitos de valor artístico, estético, histórico, turístico e paisagístico, entre outros direitos difusos.

## Objetivo do Projeto

Este projeto faz parte de um processo de análise dos impactos da desinformação nos direitos difusos. A coleta e análise de dados de checagem de fatos são etapas preliminares para entender como a desinformação pode afetar esses direitos.

## Dependências

Para executar este projeto, as seguintes bibliotecas são necessárias:

- `scrapy`: Framework de scraping usado para construir o spider.
- `scrapy_playwright`: Integração do Scrapy com o Playwright para renderização de páginas JavaScript.
- `scrapy-xlsx`: Extensão do Scrapy para exportar dados em formato XLSX.
- `typing`: Biblioteca para suporte de tipagem.
- `asyncio`: Biblioteca para programação assíncrona.
- `re`: Biblioteca para operações com expressões regulares.

## Métodos

### start_requests

Inicia as requisições para a URL inicial, configurando o uso do Playwright para renderizar a página.

### parse

Responsável por clicar nos botões da página até que uma condição seja atendida, obter o HTML atualizado e extrair os links das notícias.

### parse_newspage

Responsável por extrair os dados da página de notícias, como título, data, texto e tags de checagem.

## Execução

Copie o código, inicie o ambiente virtual, instale as dependências, e execute:

**scrapy crawl uolSpider -o nome_do_arquivo.xlsx**
