#  CP-Admin
admin app for Coupons-Providing

## Инструкция
* Установить CP-admin
* Установить [Coupons-Providing](https://github.com/Ruslan-Bosin/Coupons-Providing) _(доступ для infGAI)_ **НЕ ЗАПУСКАТЬ**
* Открыть python консоль и прописать следующие команды:
```py
from app.models import create_tables, add_admin
create_tables() # создание базы данных
add_admin() # добавление админа (введите данные запрошенные после запуска)
```
* Запустить run из проекта Coupons-Providing
* можно запускать)


В папке проекта находится следующее:
* Папка database, где реализуется в файле Storage.py реализуется взаимодействие с базой данных основного проекта
* Папка screens где находятся py файлы, в которых описываются классы окон приложения:
LoadingScreen - окно загрузки, проверяющее состояния сервера основного проекта
LoginScreen - окно входа для админа, если его сессия закончилась
MainScreen - основное окно приложения
* Папка static где хранятся статические файлы, к которым обращается наше приложение. Здесь в папке icons хранятся svg файлы иконок, а в utils хранятся py файлы(check_server и exeption_hook) первый из которых для проверки доступности сервера основного проекта, а второй для перевода qt ошибок
* __init__.py - файл инициализации приложения
* config.py - файл, с объявленными константами
* run.py - основной файл для запуска нашего проекта

Технологи:
1. Библиотека PyQt6 - для реализации всех окон и их стилизации
2. Github - для контроля версия
3. Json - как тип репрезентация данных, полученных с сервера
4. Pillow для визуализации картинок
5. Datetime - для валидации токенов
6. Sqlite3 - для взаимодействия с базами данных
7. Requests - для отправки запросов
8. Csv - как возможный формат для экспорта
