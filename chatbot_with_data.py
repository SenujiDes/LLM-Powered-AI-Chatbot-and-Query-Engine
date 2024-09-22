from llama_index.llms.groq import Groq
import streamlit as st
from llama_index.core import SimpleDirectoryReader , VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

def chat_qa_data():
    #Load the Data
    documents = SimpleDirectoryReader("./data/").load_data()
    #Initialize the LLM
    Settings.llm = Groq(model="Llama3-8b-8192", api_key="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")
    #Initialize the Embedding Model
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    #Configure the token
    Settings.num_output = 512
    #Define the chunk size , means how many small pieces you need to break the text
    #Overlap means when retrieve what is the size of overlap with other chunks
    Settings.node_parser = SentenceSplitter(chunk_size=512 , chunk_overlap=20)
    #Initialize the vector store index with docments, embeded model and LLM
    index = VectorStoreIndex.from_documents(documents,embed_model = Settings.embed_model , llm = Settings.llm)
    index.storage_context.persist()

    query_engine = index.as_query_engine()
    # = "What is the vision for national AI strategy"
    prompt =""
    #response= query_engine.query(prompt)
    #print(response)

    #___________________

    st.title(f"**My AI :green[Chatbot]** :sparkles:")  # Add emojis and colors to the title
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("Ask any question here!"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate the assistant's response using the user's prompt instead of hardcoded promt
        response = query_engine.query(prompt)  # Replacing promt with prompt
        
        # Display assistant's response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})



chat_qa_data()