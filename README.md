Бот для игры в крестики нолики.

https://seahorse-tender-ladybird.ngrok-free.app/docs

По этой ссылке доступен просмотр доступных ручек

В проекте используется Redis для хранения пользователей. Для просмотра авторизованных пользователей в консоль потребуется ввести:

docker exec -it src-redis-1 redis-cli -a 1



ngrok http --domain=seahorse-tender-ladybird.ngrok-free.app 8000
бэк


ngrok http --domain=seahorse-tender-ladybird.ngrok-free.app 8888
бот