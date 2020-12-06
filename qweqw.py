from bs4 import BeautifulSoup as BS
from requests import get
'''
sale_list = BS(get('https://store.playstation.com/ru-ru/category/5dc2862d-c810-4105-86de-e51c693987d4/1').text,
               'html.parser')
# print(sale_list.prettify())
game_list = [x for x in sale_list.select('#main > section > div > div > ul > li')]
'''
# сверху пример Толика, я не понимаю как выбирать эти  #main > section > div > div > ul > li

steam_sale_list = BS(get('https://store.steampowered.com/wishlist/profiles/76561198049638242/#sort=order').text,
                'html.parser')      #ссылка, с которой нужно уметь доставать значение g_rgWishlistDa - нужно только оно,
                                    # как это сделать?

steam_game_list = [x for x in steam_sale_list.select('html class="responsive" lang="en"> body > div > div > scripts')]
# пробный вариант, который пока не работает

print(steam_game_list) # выводит весь файл, легче в блокнот скопировать и там искать
