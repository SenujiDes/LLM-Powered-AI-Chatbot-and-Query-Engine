from llama_index.llms.groq import Groq
import streamlit as st

def chat_qa():

    llm = Groq(model= "Llama3-8b-8192" , api_key= "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", temperature=0.7 )
    promt= "What is Generative AI? give one sentence"
    response = llm.complete(promt)
    st.title(f"**My AI :green[Chatbot]** :sparkles:")  # Add emojis and colors to the title

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # React to user input
    if prompt := st.chat_input("Ask any question here !"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display assistant response in chat message container

        response = llm.complete(promt)
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        #print(response)
        #return response



chat_qa()



