from data.news import news_crawler
from data.calender import quickstart as calender
from data.mail import quickstart as mail
from data.weather import weather as weather_info

def main():
	news = news_crawler.get_news('https://www.eventrakete.de/offenburg/blackforest-hackathon/')
	events = calender.get_events()
	emails = mail.get_mails()
	weather = weather_info.get_temperature()

if __name__ == '__main__':
    main()