# tools.py corregido

# 1. Importaciones: Usaremos el decorador @tool para simplificar la definición.
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime

# --- 1. Herramienta de Guardado (save_tool) ---
# Usamos el decorador @tool, que es el método preferido en LangChain
@tool
def save_to_txt(data: str, filename: str = "research_output.txt") -> str:
    """
    Guarda la información de una investigación o resumen estructurado en un archivo de texto.
    Usa esta herramienta al final, solo si el usuario pide guardar o archivar la información.

    Args:
        data (str): La información o texto que deseas guardar.
        filename (str, opcional): El nombre del archivo. Por defecto es 'research_output.txt'.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    # Nota: Usar 'a' para 'append' (añadir), esto es correcto.
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Información guardada correctamente en el archivo: {filename}"


# --- 2. Herramienta de Búsqueda Web (search_tool) ---
# Usamos el decorador @tool para envolver el DuckDuckGoSearchRun
search = DuckDuckGoSearchRun()

@tool
def search_tool(query: str) -> str:
    """
    Busca en la Web por información actualizada o detalles específicos.
    Ideal para baleros, refacciones, o noticias recientes.
    """
    return search.run(query)


# --- 3. Herramienta de Wikipedia (wiki_tool) ---
# Esta es la corrección clave. Necesitamos envolver WikipediaQueryRun como una Tool
# para que el Agente Gemini pueda entender su firma.

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000) # Aumenté los caracteres para mejor resumen

@tool
def wiki_tool(query: str) -> str:
    """
    Busca información detallada y de alta calidad sobre temas científicos,
    genómicos, bioinformáticos o históricos en Wikipedia.
    """
    # WikipediaQueryRun.run espera el 'query' para buscar
    return api_wrapper.run(query)


# Renombramos las herramientas para usarlas en main.py
save_tool = save_to_txt
# search_tool ya tiene el nombre correcto
# wiki_tool ya tiene el nombre correcto
