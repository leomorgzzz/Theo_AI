import os
from dotenv import load_dotenv


load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


CHROMA_DB_DIR = "./theo_memory_db"
EMBEDDINGS_MODEL = "models/text-embedding-004"
embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDINGS_MODEL)

def indexar_documentos(pdf_path):
    """Carga, divide y almacena un PDF en la base de datos vectorial."""
    print(f"Iniciando indexación del archivo: {pdf_path}")


    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        print(f"Documento cargado. Total de páginas: {len(documents)}")
    except Exception as e:
        print(f"Error al cargar el PDF: {e}")
        return


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Documento dividido en {len(chunks)} fragmentos (chunks).")


    Chroma.from_documents(
        chunks,
        embeddings,
        collection_name="theo_long_term_memory",
        persist_directory=CHROMA_DB_DIR
    )

    print("\n✅ Indexación completada. La información ha sido añadida a la memoria de Theo.")



if __name__ == "__main__":

    ruta_pdf = input("Por favor, ingresa la ruta del archivo PDF a indexar (ej. ./catalog.pdf): ")
    if os.path.exists(ruta_pdf):
        indexar_documentos(ruta_pdf)
    else:
        print(f"Error: No se encontró el archivo en la ruta '{ruta_pdf}'")
