from llama_index.llms.groq import Groq
from llama_index.core.agent import ReActAgent #cabalbe of building aqn basic agent application
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings;

MODEL_NAME = "llama-3.1-70b-versatile"
API_KEY = "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"

def get_llm(model_name, api_key):
    return Groq(model= model_name, api_key=api_key)

def initialize_settings():
    Settings.llm =get_llm( MODEL_NAME, API_KEY)

def multiply(a: float, b:float):
    return a*b

def add(a: float, b:float):
    return a+b

multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)

initialize_settings()

agent =ReActAgent.from_tools([multiply_tool, add_tool], llm=Settings.llm , verbose=True)

response = agent.chat("What is 20+(2*4)? Use a tool to calculate every step")

print(response)