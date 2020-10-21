# 7news_web_site

Для корректного создания базы данных необходимо сначала сконфигурировать миграции для приложения 'main':
    
    python manage.py makemigration main
а лишь затем запустить миграцию:

    python manage.py migrate

