# Importamos Langchain y LangGraph desde su documentación (Quickstart)

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, MessageGraph

# Importamos el LLM (Ollama)

from langchain_community.llms.ollama import Ollama

# Para conectarnos con base de datos
from pymongo import MongoClient


# Conexión con base de datos
client = MongoClient('localhost', 27017)
database = client['Ungga-Challenge']
collection = database['citas']

# Generamos un llm
llm = Ollama(model="llama3")

# creamos un historial de chat vacío
chat_history = []

# PromptTemplate para el agente de citas #2

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Eres un AI que agenda citas, me debes ir preguntando mi información hasta obtener lo siguiente:
            - nombre
            - email
            - horario de cita (día de la semana, día del mes, mes y hora), haz esto mensaje tras mensaje.
            
            Solamente cuando hayas obtenido todo, retornarás los datos en forma de diccionario: 
            'nombre': <nombre>, 'email': <email>, 'cita': <horario de la cita en MM/DD/2024 HH:MM>
            No retornes nada extra más que eso, solamente el diccionario, ninguna palabra más.""",
        ),

        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

chain = prompt_template | llm

# Función de Agente de citas #2

def chat(user_input):
    response = chain.invoke({"input": user_input, "chat_history": chat_history})
    print(response)
    chat_history.append(HumanMessage(content=response))
    while True:
        pregunta = input("You: ")
        if pregunta == "bye":
            return
        # response = llm.invoke(question
        response = chain.invoke({"input": pregunta, "chat_history": chat_history})
        chat_history.append(HumanMessage(content=pregunta))
        chat_history.append(SystemMessage(content=response))
        print("-"*50)
        print("AI: " + response)

        #datos_iniciales = response[-1].content
        datos_iniciales = response
        if datos_iniciales.startswith("{"):
            print("---------------out--------------")
            datos_diccionario = eval(datos_iniciales)
            print(type(datos_diccionario))
            print(datos_diccionario)
            user_nombre = datos_diccionario['nombre']
            print(user_nombre)
            user_email = datos_diccionario['email']
            print(user_email)
            user_cita = datos_diccionario['cita']
            print(user_cita)
            print("---------------out--------------")

            confirmacion = "Pregunta si quiero confirmar la cita. Si te digo que no, pregúntame qué quiero modificar, lo modificas y vuelves a retornar el diccionario. Si te respondo afirmativamente, retorna True, nada más que eso"
            response = chain.invoke({"input": confirmacion, "chat_history": chat_history}) #aqui el chat nos pregunta si confirmamos
            chat_history.append(HumanMessage(content=confirmacion)) #guardar confirmacion
            chat_history.append(SystemMessage(content=response)) # guardar accion IA
            print("AI: " + response)   
            
            pregunta = input("You: ") #aquí respondemos a si confirmamos o no
            response = chain.invoke({"input": pregunta, "chat_history": chat_history}) #aqui imprime True
            chat_history.append(HumanMessage(content=pregunta)) # guardar nuestra confirmacion
            chat_history.append(SystemMessage(content=response)) # guardar True
            
            if str(response) == "True":
                print("---------------out--------------")
                collection.insert_one({"name":user_nombre, "email": user_email, "cita": user_cita})
                print("cita agendada")
                print("---------------out--------------")
                return
            


# Generamos un Grafo, que contiene un Node(Agente #3 - Conversacional) y un Edge
graph = MessageGraph()

graph.add_node("oracle", llm1)
graph.add_edge("oracle", END)

# Definimos punto de entrada
graph.set_entry_point("oracle")

# Compilamos el grafo junto con nuestro llm
runnable = graph.compile()


# Función para intercambiar entre agentes
def encontrar_palabras_clave(string, palabras):
    encontrar_palabras = []
    for palabra in palabras:
        if palabra in string:
            encontrar_palabras.append(palabra)
    return encontrar_palabras





# Definimos el chat principal con el agente #3 Conversacional
def chat_main(user_input):
    
    terminar = "bye"
    
    store1 = []
    user_input = user_input
    
    system_input = "Eres un chatbot que puede traducir lo que sea. También puedes agendar citas. Comienza dándome la bienvenida."
    store1.append("System: " + system_input)
    primer_mensaje = runnable.invoke(HumanMessage(system_input))
    store1.append("AI: " + primer_mensaje[-1].content)
    print(primer_mensaje[-1].content)
    
    while user_input != "terminar":
        user_input = input("Ingrese mensaje: ")
        store1.append("Human: " + user_input)
        palabras_clave_cita = ["cita", "citas", "appointment", "appointments"]
        iniciar_cita = encontrar_palabras_clave(user_input, palabras_clave_cita)
        if len(iniciar_cita)>0:
            chat(user_input)
        respuesta = runnable.invoke(HumanMessage(user_input))
        store1.append("AI: " + primer_mensaje[-1].content)
        print(respuesta[-1].content)

