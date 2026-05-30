# OrganizationWorkFlowBackend
Бэкенд приложения учета работ организации 


## _Установка на Linux/Ubuntu_:

1. Ставим питон версии 3.12 Для этого открываем консоль и вводим следующие команды:
    ```sh
    sudo apt update
    sudo apt upgrade -y
    sudo add-apt-repository ppa:deadsnakes/ppa, здесь далее нажимаем enter
    sudo apt install python3.12
    sudo apt install python3-pip
    sudo apt install python3-devel
   
2. Запускаем postgresql в отдельном Docker-контейнере на локальной машине:
    ```sh
    docker run -d \
      --name postgres-work-flow \
      -e POSTGRES_DB=work_flow \
      -e POSTGRES_USER=work_flow \
      -e POSTGRES_PASSWORD=work_flow \
      -p 15432:5432 \
      -v postgres_work_flow_data:/var/lib/postgresql/data \
      postgres:15
    ```
   Если необходимо полностью пересоздать контейнер с БД:
   ```sh
   docker rm -f postgres-work-flow
   ```
   Если при этом так-же необходимо дропнуть данные в БД:
   ```sh
   docker volume rm postgres_work_flow_data
   ```
3. Устанавливаем redis на операционную систему:
    ```sh
    sudo apt install redis-server 
    sudo nano /etc/redis/redis.conf
    находим строку supervised, заменяем на supervised systemd
    sudo systemctl restart redis-server
4. В любом месте на жестком диске создать папку для проекта, далее зайти в нее. \
    Открыть в папке консоль и склонировать репозиторий локально
    ```sh
    git clone https://github.com/Ensin1031/OrganizationWorkFlowBackend.git
    ```
    После этого в консоли прописать команды:
    ```shell
    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
   ```
   Либо на свой вкус клонировать проект, активировать виртуальное окружение, установить зависимости командой:
   ```shell
   pip install -r requirements.txt
   ```
5. Открыть среду Pycharm, занести в параметр запуска проекта настройки work_flow.local_settings:
в Environment variables прописываем:
   ```sh
   PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=work_flow.local_settings
   ```
   В дальнейшем, для запуска команд для локального приложения из консоли необходимо явно прописывать локальные настройки, добавляем к каждой команде:
   ```shell
   --settings=work_flow.local_settings
   # Например
   ./manage.py createsuperuser --settings=work_flow.local_settings
   ./manage.py runserver --settings=work_flow.local_settings
   ./manage.py migrate --settings=work_flow.local_settings
   ./manage.py makemigrations --settings=work_flow.local_settings
   ```
6. Запускаем celery в командной строке:
     ```shell
     celery -A celery_management worker --loglevel=info
     ```
