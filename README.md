# Телеграм бот для публикаций фото/видео контента
Бот делался для быстрой и комфортной работы. На момент написания бота не было сервиса, готовых разработок, необходимого функционала(реакции к публикации)
## Текущий функционал
1. Система лайков через инлайн кнопки
2. Наложение водного знака поверх контента
3. Разграничение доступа
4. Модерация (бан, анбан)
5. Предложка для контента от пользователей с последующей публикацией
6. Публикация рекламы с инлайн ссылкой
7. github actions CI/CD сборка/деплой

## Планирую сделать(как будет время)
1. Логирование
2. Управление модераторами
3. Генерация мемов
4. Парсинг популярных реусрсов и автопостинг
5. Рейтинг постов на основе лайков (отдельный сервис на go)
6. ...

#### Стэк: python, aiogram, mongodb, redis, ansible, github actions, ffmpeg
