from llama_index.llms.groq import Groq


def chat_qa():

    #way1
    #llm = Groq(model= "Llama3-8b-8192" , api_key= "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" )
    #response = llm.complete("What is Generative AI?")
    #print(response)

    llm = Groq(model= "Llama3-8b-8192" , api_key= "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", temperature=0.7 )
    promt= "who are you"
    response = llm.complete(promt)
    print(response) #print the output





chat_qa()