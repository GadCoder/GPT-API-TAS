import os


from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_objectbox.vectorstores import ObjectBox
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain import hub

from app.core.config import settings


# Initialize and configure the retrieval chain
def initialize_qa_chain():
    # Valida that ./data/context.txt exists\
    context_file = "data/context.txt"
    if not os.path.exists(context_file):
        raise FileNotFoundError("File ./data/context.txt not found")

    loader = TextLoader(context_file)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(data)
    vector = ObjectBox.from_documents(documents, OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY),
                                      embedding_dimensions=768)
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=settings.OPENAI_API_KEY)
    prompt = hub.pull("rlm/rag-prompt")

    # Create RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vector.as_retriever(),
        chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain


# Initialize chain once to avoid reloading on every request
qa_chain = initialize_qa_chain()