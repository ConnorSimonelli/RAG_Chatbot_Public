
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def embed():
    """
        
        Embeds saved txt files from webpage and saves in vector db to be used by llm

        Return:
            returns a retriever of easy integration into qaChain
    
    """

    print("Embedding web pages")
    load_dotenv()

    path = './RAGData' 
    loader = DirectoryLoader(path, glob = "**/*.txt",loader_cls=TextLoader) #create a doc loader, pointed to ./RAGData and .txt files
    docs = loader.load() #Load files into docs

    #Check if data has been loaded form ./RAGData, if not throw error
    if len(docs) == 0:
        raise ValueError("Failed to load any docs to embed")

    textSplitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 100) #Define a chunk size and chunk over lap for a textSplitter
    splits = textSplitter.split_documents(docs) #Split docs

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large") #Define a model to use for embedding for docs
    vectorstore = FAISS.from_documents(splits, embeddings) #Embed split docs using the embedding model store in vector db
    vectorstore.save_local("faissIndex") #Save vector DB 


    retriever = FAISS.load_local("faissIndex", embeddings, allow_dangerous_deserialization = True).as_retriever() #Define a retriever pointed to VB that the llm can use later

    return retriever








