from bs4 import BeautifulSoup as BS
from requests import get
from json import loads
from steam_web_api_interaction import main

'''
sale_list = BS(get('https://store.playstation.com/ru-ru/category/5dc2862d-c810-4105-86de-e51c693987d4/1').text,
               'html.parser')
# print(sale_list.prettify())
game_list = [x for x in sale_list.select('#main > section > div > div > ul > li')]
'''
# сверху пример Толика, я не понимаю как выбирать эти  #main > section > div > div > ul > li

'''steam_sale_list = BS(get('https://store.steampowered.com/wishlist/profiles/76561198049638242/#sort=order').text,
                'html.parser')      #ссылка, с которой нужно уметь доставать значение g_rgWishlistData - нужно только оно,
                                    # как это сделать?

steam_game_list = [x for x in steam_sale_list.select('html class="responsive" lang="en"> body > div > div > scripts')]
# пробный вариант, который пока не работает

print(steam_game_list) # выводит весь файл, легче в блокнот скопировать и там искать
'''


def get_data_about_game(app_id):
    raw_game_details = BS(get(f'https://store.steampowered.com/api/appdetails?appids={app_id}').text, 'html.parser')
    game_details = loads(raw_game_details.text)
    game_data = game_details[str(app_id)]['data']
    if not game_data['is_free']:
        return {"Name": game_details[str(app_id)]['data']['name'],
                "price": game_details[str(app_id)]['data']['price_overview']['final_formatted'],
                "discount": game_details[str(app_id)]['data']['price_overview']['discount_percent']}
    else:
        return {}

next_app_id = 359550
l = get_data_about_game(next_app_id)
for i in l:
    print(i)
