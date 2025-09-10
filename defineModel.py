from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import embedding


def generateQaChain():
    """

        Creates a qaChain

        Returns:
            qaChain which answers questions against a index

    """
    
    #Tries to embed documents if error is thrown catch and return None and print error message
    try:
        retriever = embedding.embed()
    except ValueError as e:
        print(e)
        return None

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) #Get access to an llm form openAI
    qaChain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff") #Build qaChain
    return qaChain