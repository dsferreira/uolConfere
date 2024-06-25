from typing import Iterable
from uolConfere_scraper.items import UolconfereItem
from scrapy_playwright.page import PageMethod
import scrapy
import asyncio
import re

class UolSpider(scrapy.Spider):
    name = "uolSpider"
    allowed_domains = ["noticias.uol.com.br"]
    start_urls = ["https://noticias.uol.com.br/confere/"]

    def start_requests(self): 
        url = "https://noticias.uol.com.br/confere/"
        yield scrapy.Request(
            url, 
            meta={
                'playwright': True,
                'playwright_include_page': True,
                'playwright_page_methods': [
                    PageMethod('wait_for_load_state', 'load')
                ]
            }
        )

    async def parse(self, response):
        page = response.meta.get("playwright_page")
        if not page:
            self.logger.error("Página não encontrada")
            return

        try:
            # Loop para clicar no botão até que uma condição seja atendida
            while True:
                try:
                    await page.click('.btn-search')
                    await asyncio.sleep(1.5)
                except Exception as e:
                    self.logger.error(f"Erro ao clicar no botão: {e}")
                    break

            # Obtém o HTML atualizado da página
            html = await page.content()
            response = scrapy.http.HtmlResponse(url=page.url, body=html, encoding='utf-8')

            # Coleta dos links de notícias
            news = response.css("div.thumbnails-item > div > a::attr(href)").getall()
            self.logger.info(f"Total de notícias encontradas: {len(news)}")
            teste = [new for new in news if "noticias.uol.com.br" in new]

            for news_url in teste:
                yield response.follow(news_url, callback=self.parse_newspage)
        
        finally:
            await page.close()

    def parse_newspage(self, response):
        newspage_item = UolconfereItem()

        textoBruto = response.css("p.bullet").getall()
        titulo = response.css("h1::text").get()
        data = response.css(".date::text").get()
        if not textoBruto:
            textoBruto = response.css("p").getall()
            del textoBruto[:4]
            del textoBruto[-11:]
            titulo = response.css('.col-sm-22::text').get()
            data = response.css('p.p-author.time::text').get()
            

        textoFinal = re.sub(r'<[^>]+>', ' ', ' '.join(textoBruto))

        checkTag = response.css('h2.bullet::text').getall()
        if not checkTag:
            self.logger.warning("Nenhum texto encontrado em 'h2.bullet'")

        newspage_item['url'] = response.url
        newspage_item['text'] = textoFinal
        newspage_item['date'] = data
        newspage_item['checkTag'] = checkTag[-2] if len(checkTag) > 1 else None
        newspage_item['title'] = titulo

        self.logger.info(f"Item extraído: {newspage_item}")
        yield newspage_item
