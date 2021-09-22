# py-web-crawler

- Scrapy

# XPath

Scrapy selectors tem suporte para expressões XPath
Ex:

```python
response.xpath('//title/text()').get()
>> 'Quotes to Scrape'
```

Expressões XPath são a base dos Scrapy Selectors.
Usando XPath você consegue selecionar coisas como: Selecionar o link que contém o texto _'Next Page'_

```
quote1 = response.css('div.quote')[0]
text = quote.css('span.text::text').get()
author = quote1.css('small.author::text').get()
tags = quote1.css("div.tags a.tag::text").getall()
```

Iterando pelos elementos das quotes e adicionando num dicionário

```python
for quote in response.css('div.quote'):
    text = quote.css('span.text::text').get()
    author = quote.css('small.author::text').get()
    tags = quote.css('div.tags a.tag::text').getall()
    print(dict(text=text, author=author, tags=tags))
```

# Guardando os dados

`scrapy crawl quotes -O quotes.json`

Gera um arquivo `quotes.json` contendo todos os items serializados em JSON.

`-O` sobrescreve qualquer arquivo existente. `-o` acrescenta novo conteúdo. Porém acrescentar a um arquivo JSON torna o arquivo JSON inválido. Quando acrescentando dados a um arquivo, considere usar um formato de serialização diferente, como JSON lines:

`scrapy crawl quotes -o quotes.jl`

# Links seguintes

Ao invés de fazer scrape das duas primeiras páginas do site salvar todas as páginas do website.
Primeiro é necessário extrair o link da página seguinte. Examinando a página, nos podemos ver que há um link para a próxima página.
Podemos extrair no shell

```python
response.css('li.next a').get()
response.css('li.next a::attr(href)').get()
# ou
response.css('li.next a').attrib['href']
```

O scrapy programa a requisição para ser para ser mandada e registra um metodo callback para ser executada quando a requisicao acabar.

```python
next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
```

# Atalho para criação de Requests

Como atalho para criar onjetos Request você pode usar `response.follow`

```python
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
```

O `response.follow` tem suporte para URLs relativas, não é necessário chamar `urljoin`. Esse método só retorna uma instância Request ainda é necessário `yield`
também é possível passar um _selector_ em `response.follow` ao invés de uma _string_.

```python
for href in response.css('ul.pager a::attr(href)'):
    yield response.follow(href, callback=self.parse)

```

para tags **a** existe um atalho: `response.follow` usa seu atributo `href` automaticamente

```python
for a in response.css('ul.pager a'):
    yield response.follows(a, callback=self.parse)
```

Para criar multiplas requisições de um _iterable_:
`response.follow_all`:

```python
anchors = response.css('ul.pager a')
yield from response.follow_all(anchors, callback=self.parse)
```

ou

```python
anchors = response.css('ul.pager a')
yield from response.follow_all(css='ul.pager a', callback=self.parse)
```

# Spider arguments

`scrapy craw quotes -O quotes-humor.json -a tag=humor`

Esses argumentos são passados no método `__init__`
