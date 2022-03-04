## Создаем офлайн библиотеку

Данный скрипт позволит скачать книги и обложки к ним с сайта [БОЛЬШАЯ БЕСПЛАТНАЯ БИБЛИОТЕКА](http://tululu.org)

## Как установить

- Скачай программу себе на компьютер.
- Создай файл .env и укажи название папок для скачивание книг и обложек к ним.
```buildoutcfg
BOOK_FOLDER='Тут название папки'
```
```buildoutcfg
IMAGE_FOLDER='Тут название папки'
```
- Создай [виртуальное окружение](https://python-scripts.com/virtualenv) для проекта.
- Установи зависимости.
```bash
pip install -r requirements.txt
```
- Запусти скрипт указанием начальной страницы для скачивания. Указание конечной страница не является обязательным.
```bash
python offline_library.py --start_page (тут номер страницы)
```
- Также можно указать необязательные аргументы:
```buildoutcfg
python offline_library.py --start_page (тут номер страницы) --dest_folder (тут название папки куда будут скачаны все данные)
```
```buildoutcfg
python offline_library.py --start_page (тут номер страницы) --json_path (тут название папки куда будет скачан файл *.json с информацией обо всех книгах)
```
- Если скачивание картинок не требуется, то введите аргумент:
```bash
python offline_library.py --start_page (тут номер страницы) --skip_imgs 
```
- Если скачивание книг не требуется, то введите аргумент:
```bash
python offline_library.py --start_page (тут номер страницы) --skip_txt 
```
## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](https://dvmn.org).
