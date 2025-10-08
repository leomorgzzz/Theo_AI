
# Theo: Agente de IA Personalizado y Persistente 

Theo es un asistente de Inteligencia Artificial especializado, diseñado para ser un experto en mi contexto: Ciencias Genómicas/Bioinformática y la Refaccionaria (Donde trabajo).

Construido con LangChain y potenciado por la API de Gemini, Theo no solo responde preguntas, sino que recuerda conversaciones y utiliza herramientas para obtener información.

## Características Principales

- Memoria a Largo Plazo Persistente (RAG): Utiliza ChromaDB y embeddings de Gemini para almacenar y recuperar hechos relevantes de sesiones pasadas.

- Memoria Conversacional: Recuerda el contexto de la sesión actual (session_history) para mantener conversaciones coherentes.

- Agente con Herramientas: Puede razonar sobre qué herramienta utilizar para responder mejor a una consulta.

- Herramientas de Búsqueda y Archivo: Acceso directo a la web, Wikipedia y una herramienta para guardar datos.

## Herramientas Disponibles (Tools)

Tiene acceso a las siguientes herramientas para responder a tus preguntas:

    Herramienta       |                     Función

    search_tool       |     Busca información actualizada en la Web.

    wiki_tool         |     Busca información detallada en Wikipedia.

    save_tool         |     Guarda el texto de una investigación o resumen en un archivo local (.txt).
    
## Configuración e Instalación

Los siguientes pasos son para ejecutar Theo en cualquier sistema operativo Linux, se ha probado de manera exitosa tanto en Ubuntu como en Debian, otras distribuciones deberian de funcionar igual, pero no es 100% seguro.

Sigue estos pasos para poner a Theo en funcionamiento.

1. Clonar el Repositorio

Abre tu terminal y descarga el código:

```

git clone https://github.com/leomorgzzz/Theo_AI.git

cd Theo_AI

```
2. Configurar el Entorno Virtual

Crea el entorno virtual y actívalo:

```

python3 -m venv venv

source venv/bin/activate

```
3. Instalar Dependencias

Asegúrate de tener un archivo requirements.txt y luego instala:
```

pip install -r requirements.txt

```
4. Configurar la Clave de API

Crea un archivo llamado .env en la carpeta raíz del proyecto y pega tu clave de Gemini API dentro.
```

# .env
GEMINI_API_KEY="sk-proj-TU_CLAVE_SECRETA_AQUÍ"

```
5. Ejecutar archivo main.py

Ejecuta el comando de la siguiente manera para empezar a interactuar con Theo.
```

python3 main.py

```
## Alias para Zsh (.zshrc) y Bash (.bashrc)

Recuerda que debes reemplazar la ruta /home/USER/proyectos/Theo_AI con la ruta exacta de tu directorio de proyecto, si cambiaste el nombre de usuario o la ubicación.

1. Para Zsh (Z Shell) y Para Bash (Bourne Again Shell)

Abre ~/.zshrc o ~/.bashrc y pega esta línea:
```

# ALIAS PARA INICIAR EL ASISTENTE THEO
alias theo='cd /home/leonardo/proyectos/Theo_AI/ && source venv/bin/activate && python3 main.py && deactivate'

```
2. Recarga el shell ejecutando:

```

source ~/.zshrc   # Si estás usando Zsh
# O
source ~/.bashrc  # Si estás usando Bash

```
3. Ya puedes ejecutar el comando theo desde tu terminal y ejecutar al asistente.

```

theo

```
