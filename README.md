## Yandex GPT суммаризатор бесконечного текста

### Краткая информация
Данный Yandex GPT-суммаризатор использует следующие компоненты:
- [Yandex GPT](https://cloud.yandex.ru/services/yandexgpt)
- [Yandex GPT for Langchain](https://python.langchain.com/docs/integrations/chat/yandex)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)

### Структура репозитория и порядок работы с ботом
- файл `requirements.txt` традиционно содержит в себе список необходимых для работы программы модулей, которые устанавливаются командой 
```pip install -r requirements.txt ```
- в папке `images` хранится логотип компании, который можно использовать в графическом интерфейсе streamlit
- `utils.py` содержит две функции sum_mapReduce, sum_1rank. Первая рекурсивно суммаризирует текст до тех пор, пока финальный результат не будет длинной меньше 4000 токенов. Второй разбивает текст на кусочки длинной 4000 токенов, суммаризирует каждый кусочек последовательно, скливает итоговые суммаризации в одно целое.
- `app1.py` содержит streamlit приложение

### Запуск в Streamlit Community Cloud
Вы можете развернуть данное приложение через Streamlit Community Cloud, следуя [инструкциям](https://docs.streamlit.io/streamlit-community-cloud/get-started)

