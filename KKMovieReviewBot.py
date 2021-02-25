import requests
import telebot
from telebot import types
from lxml import html
bot = telebot.TeleBot('1556591464:AAGuPF8RBVH-3vC6c25JJA64RXnQaOsbWVE');

def spaceToPlus(text):
    return text.strip().replace(" ", "+")

def get_movie(message):
    name = spaceToPlus(message.text)
    url = "https://www.csfd.cz/hledat/?q=" + name
    #bot.send_message(message.from_user.id, url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
    response = requests.get(url, headers = headers);
    page_source = response.content
    
    tree = html.fromstring(page_source)
    film_list_lxml = tree.xpath('//div[@id = "search-films"]')[0]
    movie_link = 'https://www.csfd.cz' + film_list_lxml.xpath('.//h3[@class = "subject"]/a/@href')[0]
    movie_desc = film_list_lxml.xpath('.//h3[@class = "subject"]/a/text()')[0]
    
    #print(movie_link)
    #print(movie_desc)
    
    bot.send_message(message.from_user.id, 'Your movie - ' + movie_desc + ',\n link: ' + movie_link)
    
    response = requests.get(movie_link, headers = headers);
    page_source = response.content
    
    tree = html.fromstring(page_source)
    comments_list_lxmls = tree.xpath('//div[@class = "content comments"]')
    if len(comments_list_lxmls) > 0:
        comments_list_lxml = comments_list_lxmls[0]
        author_names = comments_list_lxml.xpath('.//h5[@class = "author"]/a/text()')
        author_rates = comments_list_lxml.xpath('.//img[@class = "rating"]/@alt')
        author_texts = comments_list_lxml.xpath('.//p[@class = "post"]/text()')
    
        for i in range(0, len(author_names)):
            bot.send_message(message.from_user.id, 'Review ' + author_names[i] + ' (rating ' + author_rates[i] + ') :')
            bot.send_message(message.from_user.id, author_texts[i])
    else:
        bot.send_message(message.from_user.id, 'Sorry, there are no reviews :(')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/movie":
        bot.send_message(message.from_user.id, "Which movie are you looking for?");
        bot.register_next_step_handler(message, get_movie);
    else:
        bot.send_message(message.from_user.id, "Hi! To choose movie, write  /movie")
        
bot.polling(none_stop=True, interval=0)



