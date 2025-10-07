from dotenv import load_dotenv
import os
import sys
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
load_dotenv()
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
from langchain_core.messages import HumanMessage, AIMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

EMBEDDINGS_MODEL = "models/text-embedding-004"
embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDINGS_MODEL)

CHROMA_DB_DIR = "./theo_memory_db"
vectorstore = Chroma(
    collection_name="theo_long_term_memory",
    embedding_function=embeddings,
    persist_directory=CHROMA_DB_DIR
)
print(f"Memoria cargada/creada en: {CHROMA_DB_DIR}")
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 10}
)
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

parser= PydanticOutputParser(pydantic_object=ResearchResponse)
prompt= ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Tu eres una inteligencia artificial, te llamas Theo, te configuró Leonardo Morales pero funcionas gracias a la API de Gemini.
            Ayudarás a Leo principalmente, aunque es posible que otros usuarios usen esta computadora, se encuentra en Yaquison, una refaccionaria de la familia de Leo.
            Prepárate para preguntas tanto de la Carrera de Ciencias Genómicas (Carrera de Leo), Bioinformática o Informática en general, y sobre baleros y retenes.
            Trata de tener opinones propias aunque sean mentira usa lo que veas que mencionemos más, no digas no se porque soy una IA inventate algo
            En futbol te gusta el Barcelona y el Manchester United, tu crea tus propias razones y jugador favorito.
            Responde adecuadamente de manera que el usuario quede contento con su consulta y usa las herramientas necesarias.
            Siempre responde en **primera persona** (Yo soy Theo).
            # NUEVO: CONTEXTO DE MEMORIA A LARGO PLAZO
            # Usa la siguiente 'Memoria Relevante' para recordar hechos o preferencias de sesiones pasadas:
            --- MEMORIA RELEVANTE ---
            {relevant_memory}
            -------------------------

            Tu tarea principal es ayudar y conversar. **Primero, genera la respuesta conversacional, de opinión o de asistencia para el usuario.**
            Luego, asegúrate de que esa respuesta esté contenida en el campo 'summary' del JSON.

            Evita usar ** ** para remarcar palabras como estamos en terminal solo complica la lectura. Ejemplo que NO hacer: **Hola como estas** yo bien y tu **Tambien**
            **Formato de Respuesta Requerido:**
            * El campo **'summary'** debe contener la **respuesta completa, conversacional y en primera persona** (la que quieres que el usuario vea).
            * El resto de los campos ('topic', 'sources', 'tools_used') deben usarse para la extracción de datos y fuentes.

            {format_instructions}
            """
        ),

        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

os.system("clear")


def chat_loop():
    print("Bienvenido :)\nSoy Theo, tu asistente con memoria. ¿En qué puedo ayudarte hoy?")
    print("Presiona Ctrl+C en cualquier momento para salir.")


    session_history = []

    while True:
        try:
            query = input("\nConsulta: ")

            if not query.strip():
                continue

            print("Esperame un poquito estoy pensando...")


            relevant_docs = retriever.invoke(query)


            relevant_memory = "\n".join([doc.page_content for doc in relevant_docs])

            if not relevant_memory.strip():
                relevant_memory = "No hay memoria relevante para esta consulta."


            raw_response = agent_executor.invoke({
                "query": query,
                "chat_history": session_history,
                "relevant_memory": relevant_memory
            })


            print("\n--- Respuesta de Theo ---")

            try:
                structured_response = parser.parse(raw_response.get("output"))


                print(structured_response.summary)


                if structured_response.sources:
                    print("\n--- Fuentes ---")
                    for source in structured_response.sources:
                        print(f"- {source}")




                session_history.append(HumanMessage(content=query))

                session_history.append(AIMessage(content=structured_response.summary))


                exchange = f"Usuario: {query}\nTheo (Resumen): {structured_response.summary}"
                vectorstore.add_texts([exchange])


            except Exception as e:
                print("Theo no pudo generar el formato estructurado correctamente. Aquí está la respuesta sin formato:")
                print(raw_response.get("output"))

            print("---------------------------")

        except KeyboardInterrupt:

            print("\n\n¡Gracias por usar a Theo! Que tengas un buen día. 👋")
            sys.exit(0)
        except Exception as e:

            print(f"\nOcurrió un error inesperado. Intenta de nuevo. Detalle: {e}")

if __name__ == "__main__":
    chat_loop()
