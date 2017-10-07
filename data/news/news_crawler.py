from newspaper import Article

def get_news(url):
	a = Article(url, language='de')
	a.download()
	a.parse()
	return a.text