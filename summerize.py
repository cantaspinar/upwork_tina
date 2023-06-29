from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader

from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.callbacks import get_openai_callback

from config import model_name
from config import openai_api_key

def summerize_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    llm = ChatOpenAI(openai_api_key=openai_api_key,model=model_name, temperature=0)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    with get_openai_callback() as cb:
        result = chain.run(docs)
        return result