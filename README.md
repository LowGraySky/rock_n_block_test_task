Выполненное тестовое задание в компанию Rock'N'Block:

Ссылка на задание: https://manzoni.atlassian.net/wiki/external/814448649/Zjk5OTI0YTUxMWNhNDgxNjk3NmQzY2I4MmJmNDNhM2U

Для запуска использовать команду: python manage.py runserver

- Конифг в формате .yaml расположен в папке RockNBlock и имеет название service_config: "RockNBlockTestTask/RockNBlockTestTask/service_config.yaml"
 - Через конфиг задаются параметры конфигурации базы данных (PostgreSQL)
 - Данный для взаимодействия с блокчейном Эфириума (адрес контракта, abi, величина gas'a, адрес ноды, приватный ключ*)

Комментарии:
 - Немного изменил порядок логики выполнения функции 'mint' - объект модели Token создается после отправки транзации, со всеми заполнеными полями.

*
 - приватный ключ от адреса, указанного в конфиге
