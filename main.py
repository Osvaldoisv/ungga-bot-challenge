# Importamos Langchain y LangGraph desde su documentación (Quickstart)
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, MessageGraph
from langchain_community.llms.ollama import Ollama   # Importamos el LLM (Ollama)
from pymongo import MongoClient                      # Para conectarnos con base de datos

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

# Función de Agente de citas #2 ------------------- Nos agendará una cita en la base de datos
def chat(user_input):

    # Inicializamos "quiero agendar una cita"
    response = chain.invoke({"input": user_input, "chat_history": chat_history})
    print(response)
    chat_history.append(HumanMessage(content=response))


    while True:
        pregunta = input("You: ")

        if pregunta == "bye":
            return

        response = chain.invoke({"input": pregunta, "chat_history": chat_history})
        chat_history.append(HumanMessage(content=pregunta))
        chat_history.append(SystemMessage(content=response))
        print("-"*50)
        print("AI: " + response)
        print("-"*50)

        datos_iniciales = response

        # Al recolectar todos los datos, devolverá un diccionario
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

            # Pregunta si queremos confirmar la cita
            confirmacion = "Pregunta si quiero confirmar la cita. Si te digo que no, pregúntame qué quiero modificar, lo modificas y vuelves a retornar el diccionario. Si te respondo afirmativamente, retorna True, nada más que eso"
            response = chain.invoke({"input": confirmacion, "chat_history": chat_history}) 
            chat_history.append(HumanMessage(content=confirmacion)) 
            chat_history.append(SystemMessage(content=response))
            print("AI: " + response)   
            

            pregunta = input("You: ") #aquí respondemos a si confirmamos o no
            response = chain.invoke({"input": pregunta, "chat_history": chat_history}) 
            chat_history.append(HumanMessage(content=pregunta)) 
            chat_history.append(SystemMessage(content=response))
            
            # Si confirmamos, se guardan los datos del diccionario en la base de datos
            if str(response) == "True":
                print("---------------out--------------")
                collection.insert_one({"name":user_nombre, "email": user_email, "cita": user_cita})
                print("cita agendada")
                print("---------------out--------------")
                return
            


# Generamos un Grafo, que contiene un Node(Agente Conversacional #3) y un Edge
graph = MessageGraph()

graph.add_node("oracle", llm)
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





# Definimos el chat principal con el Agente Conversacional #3
def chat_main(user_input):

    # definimos un historial de chat manual para el Agente Conversacional #3
    store1 = []
    user_input = ""
    
    # Este será la IA que reciba al usuario
    system_input = "Eres un chatbot que puede traducir lo que sea. También puedes agendar citas. Comienza dándome la bienvenida."
    store1.append("System: " + system_input)
    primer_mensaje = runnable.invoke(HumanMessage(system_input))
    store1.append("AI: " + primer_mensaje[-1].content)
    print(primer_mensaje[-1].content)
    
    # Aquí comienza el chat Loop, si el Usuario menciona "cita", se activará el agente de citas
    while user_input != "terminar":

        # user_input = input("Ingrese mensaje: ")
        user_input = user_input
        store1.append("Human: " + user_input)
        palabras_clave_cita = ["cita", "citas", "appointment", "appointments"]
        iniciar_cita = encontrar_palabras_clave(user_input, palabras_clave_cita)

        # Si está escrita la palabra "cita", se inicia el chat con el otro agente
        if len(iniciar_cita)>0:
            chat(user_input)
            
        #Al finalizar el chat de agendar citas, se puede seguir conversando con el Agente Conversacional #3
        respuesta = runnable.invoke(HumanMessage(user_input))
        store1.append("AI: " + respuesta[-1].content)
        print(respuesta[-1].content)

