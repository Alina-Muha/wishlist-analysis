# wishlist-analysis
для работы используется только файл steam_web_api_interactions, 
из него импортируется obtain_sales_data() который по url возвращает
##  [True, [{'Name', 'price', 'discount'},{}...]] если в его wishlist есть игры со скидкой
## [False, 'link to privacy settings'] если таких игр нет, либо данные об wishlist пользователя скрыты, последнее - ссылка на его настройки приватности
