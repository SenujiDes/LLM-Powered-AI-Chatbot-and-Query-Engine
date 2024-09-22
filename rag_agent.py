from llama_index.llms.groq import Groq
from llama_index.core.agent import ReActAgent #cabalbe of building aqn basic agent application
from llama_index.core.tools import FunctionTool
from llama_index.core.tools import QueryEngineTool
from llama_index.core import Settings;
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


MODEL_NAME = "llama-3.1-70b-versatile"
API_KEY = "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"
EMBEDDING_MODEL ="BAAI/bge-small-en-v1.5"
KNOWLEDGE_SOURCE_PATH= "./mydata/"
CHUNK_SIZE=512
CHUNK_OVERLAP=20
OUPUT_TOKENS=512

def get_llm(model_name, api_key):
    return Groq(model= model_name, api_key=api_key)

def initialize_settings():
    Settings.llm =get_llm( MODEL_NAME, API_KEY)
    Settings.embed_model =HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    Settings.num_output=OUPUT_TOKENS
    Settings.node_parser=SentenceSplitter(chunk_size=CHUNK_SIZE , chunk_overlap=CHUNK_OVERLAP)

def multiply(a: float, b:float):
    return a*b

def add(a: float, b:float):
    return a+b

multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)

def load_index(folder_path):
    documents= SimpleDirectoryReader(folder_path).load_data()
    initialize_settings()
    index = VectorStoreIndex(documents, embed_model=Settings.embed_model, llm= Settings.llm)
    index.storage_context.persist()
    return index.as_query_engine()

query_engine = load_index(KNOWLEDGE_SOURCE_PATH)

budget_tool = QueryEngineTool.from_defaults(query_engine,name="Canadian_Budget_2023", description="A RAG engine with some basic facts about the 2023 Canadian fedral budget  " )
response = query_engine.query("What was the total amount of the 2023 Canadian fedaral budget?")

agent= ReActAgent.from_tools([multiply_tool,add_tool,budget_tool], llm=Settings.llm , verbose=True)

response = agent.chat("What is the total amount of the 2023 Canadian fedral budget multiplied by 3?Step by step using a tool to do math ")

print(response)



#agent =ReActAgent.from_tools([multiply_tool, add_tool], llm=Settings.llm , verbose=True)

#response = agent.chat("What is 20+(2*4)? Use a tool to calculate every step")

#print(response)