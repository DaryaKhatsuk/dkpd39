# Динамическая форма на Flask

Это простое приложение Flask с динамической формой, которая сохраняет введенные данные в поле PostgreSQL JSONB.

### Для работы необходимы
- Python
- Virtualenv
- PostgreSQL
- Nginx
- Gunicorn

## Установка и настройка проекта

### Настройка
1. Клонируйте репозиторий:
   
         git clone https://github.com/DaryaKhatsuk/dkpd39.git
2. Создайте виртуальную среду:
  
         python -m venv venv
3. Активируйте виртуальную среду:
  
         source venv/bin/activate
4. Установите зависимости:
    
          pip3 install -r requirements.txt

### Конфигурация базы данных
1. Создайте базу данных PostgreSQL:
      1. Убедитесь, что PostgreSQL установлен, иначе выполните следующие команды:
         
               sudo apt-get update
               sudo apt-get install postgresql
      2. Войдите в систему в режиме суперпользователя:
         
               sudo -i -u postgres
      3. Создайте пользователя с паролем:
         
               createuser --interactive
      4. Создайте базу данных:
         
               createdb название_вашей_базы
      5. Отредактируйте файл настроек PostgreSQL:
         
               sudo nano /etc/postgresql/{версия}/main/postgresql.conf
      6. Найдите параметр listen_addresses и укажите '*' для разрешения всех IP-адресов:
          
                listen_addresses = '*'
      7. Отредактируйте файл pg_hba.conf:
          
               sudo nano /etc/postgresql/{версия}/main/pg_hba.conf
      8. Добавьте строку для разрешения подключения по паролю:
        
               host    all             all             0.0.0.0/0               md5
      9. Перезапустите PostgreSQL:

               sudo service postgresql restart
      10. Чтобы установить пароль для пользователя в PostgreSQL, вы можете воспользоваться командой ALTER USER. Вот пример того, как установить или изменить пароль для пользователя:

                sudo -u postgres psql
      11. Внутри командной строки PostgreSQL выполните следующую команду, чтобы установить пароль для пользователя:
         
                ALTER USER имя_пользователя WITH PASSWORD 'новый_пароль';

2. Обновите `SQLALCHEMY_DATABASE_URI` в `app.py`, указав сведения о вашей базе данных.
3. Примените миграции:
   
         python -m flask db init
         python -m flask dbmigrate
         python -m flask db update

## Развертывание на Nginx + Gunicorn

### Конфигурация Nginx
1. Установите Nginx:

         sudo apt-get install nginx
2. Создайте файл конфигурации Nginx для вашего приложения (например, `sudo nano /etc/nginx/sites-available/your-app`) с 
   соответствующими настройками server_name, location и proxy_pass.
       
   Пример настроек:

           server {
                listen 80;
                server_name localhost;
            
                location / {
                    proxy_pass http://127.0.0.1:8000;  # Change this if your Gunicorn is running on a different address or port
                    include /etc/nginx/proxy_params;
                    proxy_redirect off;
                }
            
                location /static {
                    alias /path/to/your-flask-app/static;
                }
            
                location /favicon.ico {
                    alias /path/to/your-flask-app/static/favicon.ico;
                }
            }

3. Создайте символическую ссылку на каталог с поддержкой сайтов:
  
         sudo ln -s /etc/nginx/sites-available/your-app/etc/nginx/sites-enabled
4. Проверьте конфигурацию Nginx:
   
         sudo nginx -t
5. Перезапустите Nginx:
    
         sudo service nginx restart

### Конфигурация Gunicorn
1. Установите Gunicorn:
   
         pip install Gunicorn
2. Запустите Gunicorn:
  
         gunicorn -w 4 -b 127.0.0.1:8000 app:app
   При необходимости отрегулируйте количество рабочих процессов и привяжите адрес.
