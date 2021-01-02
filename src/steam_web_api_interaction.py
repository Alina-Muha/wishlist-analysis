from steamwebapi.api import ISteamUser
from requests import get
import json
from bs4 import BeautifulSoup as BS

STEAM_API_KEY = "C66900DC016ACA765416952C6514E546"  # if empty get it here https://steamcommunity.com/dev/apikey

steam_user_info = ISteamUser(steam_api_key=STEAM_API_KEY)


# ЛЮБОЙ парсинг может вдруг не заработать
# https://store.steampowered.com/api/appdetails?appids=967390

def represent_Int(a):
    try:
        int(a)
        return True
    except ValueError:
        return False


def get_steam_id_from_url(profile_url=str):
    steam_id = ''
    url_components = profile_url.split('/')
    for i in range(len(url_components)):
        if url_components[i] == 'profiles' or url_components[i] == 'id':
            steam_id = str(url_components[i + 1])
    if represent_Int(steam_id):  # if custom id int: id = int(id)  else: id = resolve(custom id)
        return int(steam_id)
    else:
        return steam_user_info.resolve_vanity_url(vanityURL=steam_id,
                                                  url_type=1)['response']['steamid']


def str_to_list_of_dicts(text=str):
    index_l = text.find('[')
    index_r = text.rfind(']')
    text = text[index_l:index_r + 1:]
    answer = json.loads(text)
    return answer
    # answer is [{'appid', 'priority', 'added'},{},...]


def get_data_about_game(app_id):
    try:
        raw_game_details = BS(get(f'https://store.steampowered.com/api/appdetails?appids={app_id}').text, 'html.parser')
        if not raw_game_details:
            return {}
        if raw_game_details.text == 'null':
            return {}
        game_details = json.loads(raw_game_details.text)
        if not game_details[str(app_id)]['success']:
            return {}
        game_data = game_details[str(app_id)]['data']
        try:
            if not game_data['is_free']:
                if game_data['price_overview']['discount_percent'] == 0:
                    return {}
                return {"Name": game_data['name'],
                        "price": game_data['price_overview']['final_formatted'],
                        "discount": game_data['price_overview']['discount_percent'],
                        "link": f'https://store.steampowered.com/app/{app_id}'}
            else:
                return {}
        except KeyError:
            return {}
    except ValueError:
        return {}


def check_if_game_on_sale(game_url):  # not used
    game_data = BS(get(game_url).text, 'html.parser')
    summaries = {}
    try:
        summaries.update(
            {'discount': game_data.select('div[class="discount_pct"]')[0].text})  # может работать неисправно
        summaries.update(
            {'price': game_data.select('div[class="discount_final_price"]')[0].text})  # может работать неисправно
        summaries.update({'name': game_data.select('h1')[0].text[4:]})  # может работать неисправно
    except IndexError:
        return "No sale"
    return summaries
    

def obtain_sales_data(url):
    '''
    returns:
            [True, [{'Name', 'price', 'discount', 'link'},{}
            ...]]
        or
            [False, <link to privacy settings>]
    '''
    steam_id = get_steam_id_from_url(url)
    wishlist_link = f'https://store.steampowered.com/wishlist/profiles/{steam_id}/#sort=discount&discount_any=1'
    raw_wl_data = BS(get(wishlist_link).text, 'html.parser')
    wishlist_games_raw = [elem for elem in raw_wl_data.select('body > div > div > div > script')][0].contents[0]
    wishlist_games = str_to_list_of_dicts(wishlist_games_raw.split('var')[1])  # [{'appid', 'priority', 'added'},...]
    list_games_on_sale = []
    for game in wishlist_games:
        game_data = get_data_about_game(game['appid'])
        if game_data:  # not empty
            list_games_on_sale.append(game_data)
    if len(list_games_on_sale) == 0:
        return [False, f'https://steamcommunity.com/profiles/{steam_id}/edit/settings']
    return [True, list_games_on_sale]
