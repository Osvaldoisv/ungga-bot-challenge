# Importamos LangGraph desde su documentación (Quickstart)

from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph

# Importamos el LLM (Ollama)

from langchain_community.llms import Ollama

# Herramientas para Cadenas Condicionales
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

# Para conectarnos con base de datos
from pymongo import MongoClient


# Conexión con base de datos
client = MongoClient('localhost', 27017)
database = client['LangChain_Intento4']
collection = database['lenguajes']

# Generamos un llm
llm1 = Ollama(model='llama3', temperature=0.1)

# Generamos un Grafo, que contiene un Node(Agent) y un Edge
graph = MessageGraph()

graph.add_node("oracle", llm1)
graph.add_edge("oracle", END)

# Definimos punto de entrada
graph.set_entry_point("oracle")

# Compilamos el grafo junto con nuestro llm
runnable = graph.compile()


# Para generar una conversación
terminar = "bye"
user_input = ""

while user_input != terminar:
    user_input = input("Ingrese mensaje: ")
    respuesta = runnable.invoke(HumanMessage(user_input))
    print(respuesta[-1])