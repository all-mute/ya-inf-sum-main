import time
from langchain_community.chat_models import ChatYandexGPT
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain, LLMChain, StuffDocumentsChain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain_core.documents import Document

def load_documents_from_url(url) -> list[Document]:
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs

def sum_mapReduce(docs, folder_id, token, window_size, overlap_size) -> str:
    # Устанавливаем модель для суммаризации
    model_uri = "gpt://" + str(folder_id) + "/summarization/latest"
    llm = ChatYandexGPT(api_key=token, model_uri=model_uri, temperature=0)

    # Map
    map_template = """Ниже приведен набор документов
    {docs}
    Основываясь на этом списке документов, пожалуйста, определи основные темы
    Полезный ответ:"""
    map_prompt = PromptTemplate.from_template(map_template)
    map_chain = LLMChain(llm=llm, prompt=map_prompt)

    # Reduce
    reduce_template = """Ниже приведен набор кратких выжимок из документов:
    {docs}
    Возьми их и сформируй из них окончательное, сводное резюме по основным темам.
    Полезный ответ:"""
    reduce_prompt = PromptTemplate.from_template(reduce_template)
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

    # Берет список документов, объединяет их в одну строку и передает в LLMChain
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="docs"
    )

    # Объединяет и итеративно сокращает сопоставленные документы
    reduce_documents_chain = ReduceDocumentsChain(
        combine_documents_chain=combine_documents_chain,
        collapse_documents_chain=combine_documents_chain,
        token_max=window_size,
    )

    # Объединение документов путем сопоставления цепочки над ними, а затем объединение результатов
    map_reduce_chain = MapReduceDocumentsChain(
        llm_chain=map_chain,
        reduce_documents_chain=reduce_documents_chain,
        document_variable_name="docs",
        return_intermediate_steps=False,
    )

    # Разделение текста на части
    CHUNK_SIZE = window_size
    CHUNK_OVERLAP = overlap_size
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP
    )
    split_docs = text_splitter.split_documents(docs)
    #print('SPLIT DOCS: ', split_docs)
    
    final_summary = ''
    iteration = 0

    # Пока не останется только один документ
    while len(split_docs) > 1:
        summaries = []

        # Обрабатываем каждый документ в списке
        for doc in split_docs:
            summary = map_reduce_chain.run([doc])  # Запускаем map-reduce для документа
            summaries.append(summary)
            time.sleep(1)  # Ждем 1 секунду перед обработкой следующего документа

        # Объединяем все резюме в одно
        final_summary = " ".join(summaries)
        # Разбиваем объединенное резюме на новые документы
        split_docs = text_splitter.split_documents([Document(page_content=final_summary)])
        iteration += 1  # Увеличиваем счетчик итераций

    return final_summary  # Возвращаем итоговое резюме

def sum_1rank(docs, folder_id, token, window_size, overlap_size) -> str:
    # Устанавливаем модель для суммаризации
    model_uri = "gpt://" + str(folder_id) + "/summarization/latest"
    llm = ChatYandexGPT(api_key=token, model_uri=model_uri, temperature=0)

    # Map
    map_template = """Ниже приведен набор документов
    {docs}
    Основываясь на этом списке документов, пожалуйста, определи основные темы
    Полезный ответ:"""
    map_prompt = PromptTemplate.from_template(map_template)
    map_chain = LLMChain(llm=llm, prompt=map_prompt)

    # Reduce
    reduce_template = """Ниже приведен набор кратких выжимок из документов:
    {docs}
    Возьми их и сформируй из них окончательное, сводное резюме по основным темам.
    Полезный ответ:"""
    reduce_prompt = PromptTemplate.from_template(reduce_template)
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

    # Берет список документов, объединяет их в одну строку и передает в LLMChain
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="docs"
    )

    # Объединяет и итеративно сокращает сопоставленные документы
    reduce_documents_chain = ReduceDocumentsChain(
        combine_documents_chain=combine_documents_chain,
        collapse_documents_chain=combine_documents_chain,
        token_max=window_size,
    )

    # Объединение документов путем сопоставления цепочки над ними, а затем объединение результатов
    map_reduce_chain = MapReduceDocumentsChain(
        llm_chain=map_chain,
        reduce_documents_chain=reduce_documents_chain,
        document_variable_name="docs",
        return_intermediate_steps=False,
    )

    # Разделение текста на части
    CHUNK_SIZE = window_size
    CHUNK_OVERLAP = overlap_size
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP
    )
    split_docs = text_splitter.split_documents(docs)
    #print('SPLIT DOCS: ', split_docs)

    # Запуск цепочки MapReduce с задержкой между запросами
    summaries = []
    for doc in split_docs:
        summary = map_reduce_chain.run([doc])
        summaries.append(summary)
        time.sleep(1)  # Задержка в 1 секунду между запросами

    # Объединение всех суммарий в одну
    final_summary = " ".join(summaries)
    return final_summary

if __name__ == "__main__":
    token = "_____"
    folder_id = "_____"
    
    # Выбор между суммаризацией веб-сайта или текста
    choice = 'text'
    
    if choice == 'url':
        url = 'https://ru.wikipedia.org/wiki/Куросава,_Акира'
        docs = load_documents_from_url(url)
    elif choice == 'text':
        text_file = 'text.txt'
        docs = TextLoader(text_file).load()
    
    summary = sum_mapReduce(docs, folder_id=folder_id, token=token)
    print("Суммаризация: ", summary)
