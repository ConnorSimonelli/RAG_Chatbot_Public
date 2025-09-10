import validators
import crawler
import defineModel
import glob
import os

def main():
    """

    Main function of the program, hands user input for queries and also user input for setting up the RAG chat.

    """
    run = "temp" #Used to control user input loop 

    setUp() #Setup the env

    #Loops until "run" is updated by user input to finished
    while(run != "finished"): 
        sight = setSight() #gets the sight to be scraped
        pages = setPages() #gets the number of pages to scrape form that sight
        crawler.crawl(sight, pages)
        run = input("would you like to add another sight if yes enter 'yes' if no enter 'finished':\n") #Ask user if they want to do another sight
    
    qaChain = defineModel.generateQaChain()#Set up model and loads documents vector DB
    
    #Caches embedding error and cleans up program
    if qaChain is None:
        print("No documents were embedded. Exiting.")
        cleanUp()
        return


    query = input("\nEnter a query about the documents\nEnter exit to exit\n")#Being the chat process with the user by asking for a query

    #Loops until user wants to exit conversation
    while(query != "exit"):
        response = qaChain.invoke(query) #Sends query to model
        print("\n"+response['result']) #Prints models response 
        query = input("\nEnter a query about the documents\nEnter 'exit' to exit\n") #Checks if user wants to keep chatting

    #Check if user want to keep the data in RAGData or Delete it
    while(True):
        clean = input("Do you want to clean RAGData or keep it, enter 'Yes' to clean and 'No' to keep\n") #Ask for user input
        
        if(clean == "Yes"):
            cleanUp() #Cleans up RAGData
        if(clean == "No"):
            return #Return with out cleaning RAGData
        
        print("Please enter valid input 'Yes' or 'No'") #Ask for user to enter a valid input
        

    


def setUp():
    """

    Check if RAGData dir exists if so ask user if it should be cleaned up or reused

    """
    #Checks to see if dir RAGData exists
    if os.path.isdir("RAGData"):
        cleanRAGData = input("RAGData already exits, do you want to start fresh or reuse the data in RAGData. Enter 'Yes' or 'No'\n") #Ask user if they want to reuse RAGData or remove it
        if(cleanRAGData == "Yes"):
            cleanUp() #Delete the data stored in RAGData
            os.mkdir("RAGData") #Create a new RAGData folder
    else:
        os.mkdir("RAGData") #Create a new RAGData folder
    return



def cleanUp():
    """
    Cleans up any folders or docs created when program was running

    #BUG: Possible error if more then 1024 pages files or if other dir are stored inside
    """
    #Check to see if dir RAGData exists
    if os.path.isdir("RAGData"): 
        files = glob.glob('RAGData/*') #create a list of all files in RAGData
        for f in files: 
            os.remove(f) #Loops through all files in RAGData and remove
        os.rmdir("RAGData") #Remove RAGData
    else:
        print("Did not find dir 'RAGData'") #RAGData dose not exist
    return

def setPages():
    """
    
    Gets the number of pages the user would like the crawler to crawl and check its a valid input

    Returns:
        int: number of pages to crawl

    """
    #Loop until the user enters a valid number between 1-50
    while True:
        try:
            pages = int(input("How many pages would you like to crawl (1–50)?\n")) #Ask user to enter a number between 1-50 and save number as pages
            if 1 <= pages <= 50: #check if pages is between 1-50
                return pages #return the pages
            else:
                print("Invalid number of pages. Enter a number between 1 and 50.") #Ask the user to enter try to enter a valid number again
        except ValueError:
            print("Please enter a valid integer.") #Ask the user to enter try to enter a valid number again


def setSight():
    """
    
    Gets the url of the sight the user want to crawl and checks if its valid if not ask for another one

    Returns:
        string: url of the sight to be crawled

    """
    #Loop until the user enters a valid web sight address
    while True:
        sight = input("What sight would you like to use as your rag docs:\n") #Ask user to enter a valid web sight
        if validators.url(sight): #Check to see of the sight is valid
            return sight #IF sight is valid return sight 
        else:
            print("Please enter a valid URL") #Ask user to enter a valid sight


main()