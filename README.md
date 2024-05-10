# Ungga Challenge

[![PR's Welcomes](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)]()
[![GitHub pull requests](https://img.shields.io/github/issues-pr/cdnjs/cdnjs.svg?style=flat)]()

**Objective**: The challenge entails developing a multi-agent LLM (using langraph) to operate as an interactive bot communicating with users via a web interface. It's designed for two primary purposes: scheduling appointments and serving as a translator. Note that appointments could need to be conducted in multiple languages.

**Language and Technology**: You must utilize [LangGraph](https://python.langchain.com/v0.1/docs/langgraph/) and you're free to choose the interface (frontend) technology; for example [Gradio](https://www.gradio.app/) though any alternative is acceptable.

Hint: If this is your first time using LangGraph, it might be a good idea to review [LangChain](https://python.langchain.com/v0.1/docs/get_started/introduction) and its ecosystem. The documentation and the community are quite good, and there are plenty of tutorials available on the internet.

**Assistant Capabilities**:

- The graph must consist of **at least** three nodes (agents).

1. Agent 1: Classificator
- The assistant is tasked with determining the most suitable agent to execute the action.
2. Agent 2: Schedule Appoitment
- The assistant should be able to schedule appointments.
- It should extract and store information such as name, email, and phone number.
- If the assistant already has this information, it should use it for scheduling another appointment without prompting for the data again.
3. Agent 3: Translator
- It's able to translate to any language and interpret the information provided by Agent 2.


**Data Storage**: All messages and relevant information exchanged with the assistant should be saved in a database of your choice.

**Project Run Instructions**:

Provide precise instructions for setting up and running your project, including any dependencies that need to be installed.

**Demo Video**:

Include a Loom video demonstrating the functionality of your project. Clearly show how the assistant interacts with the interface.


## Technologies Used

- [Lang Graph](https://python.langchain.com/v0.1/docs/langgraph/)
- TODO (add here everything else you use for example: python, supabase, etc.)

## Contribution 👨🏻👧🏻🌍

If you want to contribute to this project, follow the steps below:

- Fork this repository
- Clone the repository
- Create a new branch: `git checkout -b <name>`
- Create your commit: `git commit -m 'Add new functionality'`
- Push your changes: `git push origin <branch>`
- Open a pull request


## Example

This example is the chat with the user. Behind the scenes langgraph and the agents would have many more interactions

```txt
user: Hola
bot: Hola ¿cómo puedo ayudarte hoy?
user: quiero una cita
bot: claro que puedo ayudarte, necesito saber tu nombre
user: juan
bot: gracias Juan, ahora ¿me puedes dar tu correo?
user: juan@gmail.com
bot: perfecto, ¿qué dia quieres la cita?
user: tomorrow 10 am please
bot: So, would it be for Saturday, May 11th, at 10:00 AM?
user: yes
bot: the appointment has been scheduled successfully

user: I want another appointment
bot: sure, when would you like the appointment?
user: martes porfavor
bot: ¿te refieres al martes 14 de mayo?
user: no, para el martes 21
bot: de acuerdo ¿a qué hora?
user: 4pm
bot: la cita quedaria para el martes 21 de mayo a las 4 pm ¿es correcto?
user: correcto
bot: la cita se agendo de forma correcta

user: como se dice ¿Dónde está el baño? en francés
bot: Où est la salle de bain ?

user: ¿cuantos planetas hay en el sistema solar?
bot: esa función esta fuera de mis capacidades
```

The examples are demonstrative; the tone and format of the messages may vary. It is important to save the data for appointments in the database
