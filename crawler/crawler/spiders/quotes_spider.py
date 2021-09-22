import scrapy


class QuoteSpider(scrapy.Spider):
    """
    Spiders sao classes que o Scrapy usa para fazer scrape das informacoes de um
    website (ou um grupo de websites). Subclass de scrapy.Spider. Define a requisicao inicial,
    e opcionalmente como seguir os links nas paginas e como fazer analisar o conteudo 
    baixado da pagina para extrair as informacoes.
    """
    # Identifica o Spider, deve ser único dentro do projeto
    name = 'quotes'
    # Substitui o metodo start_requests()
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/'
    ]
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/3/',
    #         'http://quotes.toscrape.com/page/4/'

    #     ]

    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Lida com a resposta para cada uma das requisicoes feitas.
        O parametro de resposta eh uma instância de TextResponse que
        detem o conteudo da pagina e tem metodos que ajudam na manipulacao
        desses conteudos. O metodo parse() extrai os dados como dicts e encontra novas
        URLs para seguir e criar novas requisicoes a partir delas.
        """
        # page = response.url.split('/')[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')

        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # O scrapy programa a requisição para ser para ser mandada e
            # registra um metodo callback para ser executada quando a requisicao
            # acabar.
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)
