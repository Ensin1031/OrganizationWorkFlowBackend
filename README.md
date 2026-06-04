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

7. Запуск тестов
   ```shell
   ./manage.py test  --settings=work_flow.local_settings
   # либо, с проверкой покрытия, через coverage
   coverage run manage.py test --settings=work_flow.local_settings
   # получить данные покрытию тестами через coverage
   coverage report
   # или все вместе, с coverage
   coverage run manage.py test --settings=work_flow.local_settings && coverage report -m
   # выгрузить результаты покрытия тестами в файл:
   coverage report > coverage_report.txt
   ```
      
   <details>
   <summary><strong>Результаты покрытия тестами</strong></summary>
   
   ```text
   Name                                                                          Stmts   Miss  Cover
   -------------------------------------------------------------------------------------------------
   comments/__init__.py                                                              0      0   100%
   comments/admin.py                                                                 9      0   100%
   comments/api/__init__.py                                                          0      0   100%
   comments/api/filters.py                                                           9      0   100%
   comments/api/rest_view.py                                                        19      0   100%
   comments/api/serializers.py                                                      26      0   100%
   comments/apps.py                                                                  5      0   100%
   comments/factories.py                                                            12      0   100%
   comments/migrations/0001_initial.py                                               9      0   100%
   comments/migrations/__init__.py                                                   0      0   100%
   comments/models.py                                                               19      0   100%
   comments/tests.py                                                               122      0   100%
   comments/urls.py                                                                  6      0   100%
   manage.py                                                                        11      2    82%
   notifications/__init__.py                                                         0      0   100%
   notifications/admin.py                                                           13      0   100%
   notifications/api/__init__.py                                                     0      0   100%
   notifications/api/rest_view.py                                                   59      4    93%
   notifications/api/serializers.py                                                  8      0   100%
   notifications/apps.py                                                             7      0   100%
   notifications/migrations/0001_initial.py                                          8      0   100%
   notifications/migrations/__init__.py                                              0      0   100%
   notifications/models.py                                                          26      2    92%
   notifications/services/__init__.py                                                0      0   100%
   notifications/services/notification_service.py                                   19      0   100%
   notifications/signals.py                                                          0      0   100%
   notifications/tests.py                                                           85      0   100%
   notifications/urls.py                                                             6      0   100%
   permissions/__init__.py                                                           0      0   100%
   permissions/admin.py                                                              0      0   100%
   permissions/api/__init__.py                                                       0      0   100%
   permissions/api/mixins.py                                                        70      4    94%
   permissions/apps.py                                                               5      0   100%
   permissions/migrations/__init__.py                                                0      0   100%
   permissions/models.py                                                            34      7    79%
   project/__init__.py                                                               0      0   100%
   project/admin.py                                                                 44      0   100%
   project/api/__init__.py                                                           0      0   100%
   project/api/rest_view.py                                                         51      8    84%
   project/api/serializers.py                                                      134     19    86%
   project/apps.py                                                                   5      0   100%
   project/factories.py                                                             34      0   100%
   project/migrations/0001_initial.py                                                9      0   100%
   project/migrations/__init__.py                                                    0      0   100%
   project/models.py                                                                88      9    90%
   project/tests.py                                                                115      0   100%
   project/urls.py                                                                  10      0   100%
   references/__init__.py                                                            0      0   100%
   references/admin.py                                                              26      0   100%
   references/api/__init__.py                                                        0      0   100%
   references/api/filters.py                                                         9      0   100%
   references/api/rest_view.py                                                      59     10    83%
   references/api/serializers.py                                                    65      0   100%
   references/apps.py                                                                5      0   100%
   references/factories.py                                                          33      0   100%
   references/migrations/0001_initial.py                                            14      0   100%
   references/migrations/__init__.py                                                 0      0   100%
   references/models/__init__.py                                                     0      0   100%
   references/models/status.py                                                       5      0   100%
   references/models/work_difficulty.py                                              5      0   100%
   references/models/work_priority.py                                                5      0   100%
   references/models/work_tag.py                                                     5      0   100%
   references/models/work_technology.py                                              5      0   100%
   references/models/work_type.py                                                    5      0   100%
   references/tests.py                                                              39      0   100%
   references/urls.py                                                               11      0   100%
   sprint/__init__.py                                                                0      0   100%
   sprint/admin.py                                                                  10      0   100%
   sprint/api/__init__.py                                                            0      0   100%
   sprint/api/rest_view.py                                                          36      0   100%
   sprint/api/serializers.py                                                        45      5    89%
   sprint/apps.py                                                                    5      0   100%
   sprint/factories.py                                                              13      0   100%
   sprint/migrations/0001_initial.py                                                 7      0   100%
   sprint/migrations/__init__.py                                                     0      0   100%
   sprint/models.py                                                                 13      0   100%
   sprint/tests.py                                                                 101      0   100%
   sprint/urls.py                                                                    6      0   100%
   users/__init__.py                                                                 0      0   100%
   users/admin.py                                                                    9      0   100%
   users/api/__init__.py                                                             0      0   100%
   users/api/rest_view.py                                                           80     26    68%
   users/api/serializers.py                                                         66     20    70%
   users/apps.py                                                                    10      1    90%
   users/factories.py                                                               25      1    96%
   users/migrations/0001_initial.py                                                  8      0   100%
   users/migrations/0002_userextended_slug_alter_userextended_is_active.py           4      0   100%
   users/migrations/0003_userextended_birth_date_userextended_profile_photo.py       5      0   100%
   users/migrations/0004_userextended_need_send_email_notification_and_more.py       4      0   100%
   users/migrations/__init__.py                                                      0      0   100%
   users/models.py                                                                  39      1    97%
   users/tests.py                                                                   60      0   100%
   users/urls.py                                                                     8      0   100%
   utils/choices/default_work_types_choices.py                                      15      0   100%
   utils/choices/work_connection_choices.py                                         18      0   100%
   utils/choices/work_notification_types_choices.py                                  6      0   100%
   utils/custom_slugify.py                                                           9      1    89%
   utils/default_paginator.py                                                        5      0   100%
   utils/django_validate.py                                                         29     22    24%
   utils/drf_query_params_filter.py                                                 13      4    69%
   utils/model_admin_mixins.py                                                      16      7    56%
   utils/model_mixins.py                                                            90     10    89%
   utils/test_admin.py                                                              30      1    97%
   work/__init__.py                                                                  0      0   100%
   work/admin.py                                                                    17      0   100%
   work/api/__init__.py                                                              0      0   100%
   work/api/filters.py                                                              47     12    74%
   work/api/rest_view.py                                                            61      2    97%
   work/api/serializers.py                                                          76      0   100%
   work/apps.py                                                                      7      0   100%
   work/factories.py                                                                53      2    96%
   work/migrations/0001_initial.py                                                   9      0   100%
   work/migrations/__init__.py                                                       0      0   100%
   work/models/__init__.py                                                           0      0   100%
   work/models/work.py                                                              45      0   100%
   work/models/work_connection.py                                                   13      0   100%
   work/signals.py                                                                  28      4    86%
   work/tests.py                                                                   128      0   100%
   work/urls.py                                                                      7      0   100%
   work_flow/__init__.py                                                             0      0   100%
   work_flow/local_settings.py                                                      23      0   100%
   work_flow/settings.py                                                            79      1    99%
   work_flow/urls.py                                                                 6      0   100%
   -------------------------------------------------------------------------------------------------
   TOTAL                                                                          2752    185    93%
   ```
   
   </details>
   
## Схема БД серверной части
![Диаграмма_моделей_бэк.svg](%D0%94%D0%B8%D0%B0%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0_%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B5%D0%B9_%D0%B1%D1%8D%D0%BA.svg)
