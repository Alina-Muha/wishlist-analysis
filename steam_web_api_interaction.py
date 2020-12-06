import steamwebapi
from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats, _SteamWebAPI
from requests import get
import json
from bs4 import BeautifulSoup as BS

STEAM_API_KEY = "ABD6838F654CAB1520AE8729592D0A25"  # if empty get it here https://steamcommunity.com/dev/apikey

steam_user_info = ISteamUser(steam_api_key=STEAM_API_KEY)


# ЛЮБОЙ парсинг может вдруг не заработать

def represent_Int(a):
    try:
        int(a)
        return True
    except ValueError:
        return False


def str_to_list_of_dicts(text=str):
    index_l = text.find('[')
    index_r = text.rfind(']')
    text = text[index_l:index_r + 1:]
    answer = json.loads(text)
    return answer


def check_if_game_on_sale(game_url):
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
    # dlc_list = game_data.find_all('div', {'class': 'game_area_dlc_list'})


def main(url=str):
    profile_url = url
    steam_id_url = profile_url.split('/')[-1]
    if steam_id_url == '': steam_id_url = profile_url.split('/')[-2]
    url_steam_id = steam_id_url  # самый конец ссылки на профиль
    if represent_Int(url_steam_id):  # if custom id int: id = int(id)  else: id = resolve(custom id)
        steam_id = int(url_steam_id)
    else:
        steam_id = steam_user_info.resolve_vanity_url(vanityURL=url_steam_id,
                                                      url_type=1)['response']['steamid']  # получаем id через custom id
    # верхнее обернуть в функию :url -> steam_id
    user_summary = steam_user_info.get_player_summaries(steam_id)['response']['players'][0]
    link_wishlist_on_sale = f'https://store.steampowered.com/wishlist/profiles/{steam_id}/#sort=discount&discount_any=1'
    sale_list = BS(get(link_wishlist_on_sale).text, 'html.parser')
    wishlist_games_raw = [elem for elem in sale_list.select('body > div > div > div > script')][0].contents[0]
    helper = wishlist_games_raw.split('var')[1]
    wishlist_games = str_to_list_of_dicts(helper)  # !
    for game in wishlist_games:
        res = check_if_game_on_sale(f'https://store.steampowered.com/app/{game["appid"]}')
        if type(res) == dict and res['name'].count('Players Like You Love') == 0:  # second part is bugfix
            print(res['name'][:-1:], res['price'], 'discount =', res['discount'])
    print('finished')


if __name__ == '__main__':
    start_url = str(input())  # example https://steamcommunity.com/id/lElysiuMl
    main(start_url)
