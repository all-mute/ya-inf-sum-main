import streamlit as st
from utils import sum_mapReduce, sum_1rank
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain_core.documents import Document
    
# это основная функция, которая запускает приложение streamlit
def main():
    # Загрузка логотипа компании
    logo_image = './images/logo.png'  # Путь к изображению логотипа

    # # Отображение логотипа в основной части приложения
    from PIL import Image
    # Загрузка логотипа
    logo = Image.open(logo_image)
    # Изменение размера логотипа
    resized_logo = logo.resize((100, 100))
    st.set_page_config(page_title="YaGPT чатбот", page_icon="📖")
    # Отображаем лого измененного небольшого размера
    st.image(resized_logo)
    st.title('📖 Yandex GPT суммаризатор')
    """
    Суммаризатор бесконечного текста на базе Yandex GPT.\n
    Вы можете выбрать, ккакой алгоритм использовать для суммаризации и ширину окна суммаризации в токенах (см. окно слева).
    [Исходный код приложения](ПОЗЖЕ)
    """

    # вводить все credentials в графическом интерфейсе слева
    # Sidebar contents
    with st.sidebar:
        st.title('\U0001F917\U0001F4ACYandex GPT суммаризатор бесконечного текста')
        st.markdown('''
        ## О программе
        Данный Yandex GPT суммаризатор использует следующие компоненты:
        - [Yandex GPT](https://cloud.yandex.ru/services/yandexgpt)
        - [Yandex GPT for Langchain](https://python.langchain.com/docs/integrations/chat/yandex)
        - [Streamlit](https://streamlit.io/)
        - [LangChain](https://python.langchain.com/)
        ''')
        
    yagpt_folder_id = st.sidebar.text_input("YC folder ID", type="password")
    if not yagpt_folder_id:
        st.info("Укажите [YC folder ID](https://cloud.yandex.ru/ru/docs/yandexgpt/quickstart#yandex-account_1) для запуска чатбота")
        st.stop()
        
    yagpt_api_key = st.sidebar.text_input("Service account API Key", type="password")
    if not yagpt_api_key:
        st.info("Укажите [YaGPT статичный API ключ](https://cloud.yandex.ru/ru/docs/iam/operations/api-key/create#console_1) для запуска чатбота")
        st.stop()
        
    yagpt_window_size = st.sidebar.slider("Ширина окна для суммаризации (токены)", 100, 4000, 4000)
    yagpt_overlap_size = st.sidebar.slider("Ширина пересечения окна (токены)", 0, 2000, 0)
    
    methods = ["mapReduce", "1rank"][::-1]
    selected_method = st.sidebar.radio("Выберите метод бесконечной суммаризации:", methods)  
        
    # text window for input
    input_text = st.text_area("Ваш текст:", value="", height=100)
    
    if st.button("Суммаризируй!"):
        # Вызов функции суммаризации
        input_docs = [Document(page_content=input_text)]
        
        # кружок загрузки
        with st.spinner('Суммаризация...'):
            if selected_method == "mapReduce":
                summary = sum_mapReduce(input_docs, folder_id=yagpt_folder_id, token=yagpt_api_key, window_size=yagpt_window_size, overlap_size=yagpt_overlap_size)
            elif selected_method == "mapReduce-0":
                summary = sum_1rank(input_docs, folder_id=yagpt_folder_id, token=yagpt_api_key, window_size=yagpt_window_size, overlap_size=yagpt_overlap_size)
            
        # Отображение результата
        st.write("Результат:")
        st.write(summary)
    
if __name__ == "__main__":

    try:
        main()
    except Exception as e:
        st.write(f"Что-то пошло не так. Возможно, не хватает входных данных для работы. {str(e)}")