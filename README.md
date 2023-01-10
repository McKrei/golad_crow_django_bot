## О приложении
Приложение для мониторинга цены на валюту Золотая корона
Страна отправления всегда Россия
### Возможности:
- Поддержка множества пользователей
- мониторинг цены
- сообщать о цене каждый день
- сохранение и мониторинг необходимой цены
- все это настраивается

## Как устанавливать
1) git clone
в файл env.py
и указываем токе SECRET_KEY (django), TOKEN (telegram) и DATABASE
2) docker-compose build
3) docker-compose up -d
4) docker-compose run --rm web-app sh -c "python manage.py makemigrations"
5) docker-compose run --rm web-app sh -c "python manage.py migrate"
6) docker-compose run --rm web-app sh -c "python manage.py runapp"

* Можно изменить параметры ДБ в docker-compose

## Что улучшить / в разработке:
