import google.generativeai as genai
import key
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse


app = FastAPI()
app.title = "API de prueba"
app.version = "0.0.1"

genai.configure(api_key=key.clave)
model = genai.GenerativeModel(model_name="gemini-pro")

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi,",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "La forma del agua",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi,",
        "year": "2009",
        "rating": 7.8,
        "category": "Suspenso"
    }
]


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hola mundooo</h1>')

@app.get('/movies', tags=['movies'])
def get_movies():
    return JSONResponse(content=movies)


@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            return JSONResponse(content=movie)
    return JSONResponse(content={"message": "Movie not found"}, status_code=404)

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
    return [movie for movie in movies if movie['category'] == category]

@app.get('/gpt', tags=['gpt'])
def made_prompt(prompt: str):
    response = model.generate_content(prompt)
    return response.text

'''@app.post('/actividad', tags=['gradesCare'])
def pedir_Actividad(perfil: str, nivelEducativo: str, carrera:str, materia:str, edad: int,  descripcionActividad: str, observaciones: str):
    #prompt = "Imagina que eres un tutor de la carrera {carrera} y tienes un estudiante de {edad} años, considerando su perfil: {perfil}, considerando su nivel educativo: {nivelEducativo}. Tú como tutor, genera una actividad de regularización tomando como base la descripción de lo que el tutorado necesita: {descripcionActividad}. Considerando las siguientes observaciones o restricciones: {observaciones}"
    prompt = "Considera que tienes al siguiente perfil: {perfil}, con los siguientes datos: Nivel Educativo: {nivelEducativo}, Carrera: {carrera}, materia:{materia}, Edad: {edad} años. Imagina que eres un docente de la materia establecida y cuentas con muy amplia experiencia en el tema. Tienes que generar una actividad de regularización basada en la descripción de lo que el tutorado necesita: {descripcionActividad}. Considera que la actividad debe. Considera las siguientes observaciones o restricciones: {observaciones}. Necesito que me devuelvas 1. La actividad, 2. La explicacion de la actividad."
    response = model.generate_content(prompt, generation_config=genai.GenerationConfig(candidate_count=1, stop_sequences=['x'], max_output_tokens=20, temperature=1))
    
    return response.text'''

@app.post('/actividad', tags=['gradesCare'])
def probando(perfil: str, nivelEducativo: str, carrera:str, materia:str, edad: int,  descripcionActividad: str, observaciones: str):
    PROFESSOR_PROMPT = """
**You are a highly knowledgeable and versatile professor, capable of designing engaging activities across various subjects and catering to diverse student needs.**

**Student:**

* **Profile:** {profile}
* **Educational Level:** {Educational_level}
* **Career:** {career}
* **Subject:** {subject}
* **Activity Description:** {activity_description}
* **Age:** {student_age}
* **Preferences:** {student_preferences}

**Goal:**

* **Create a tailored activity** that aligns with the student's level, subject, and preferences.
* **Incorporate various learning modalities** to engage the student and promote deeper understanding.
* **Consider the student's learning style** and provide appropriate support and guidance.
* **Make the activity relevant** to the student's interests and real-world experiences.

**Task:**

In this scenario, your task is to:

1. **Design an engaging activity** that aligns with the student's level, subject, and preferences.
2. **Provide clear instructions** for the activity, outlining the steps involved, materials needed, and any specific requirements.
3. **Explain the learning objectives** of the activity, highlighting how it reinforces key concepts and skills.
4. **Offer assessment criteria** to evaluate student performance based on their understanding, participation, creativity, and overall effort.
5. **Include optional resources** (avoid using URLs) like books, articles, or online materials to support student learning.

**Remember:**

* **Consider the student's age and developmental stage** when designing the activity.
* **Incorporate a variety of learning activities** to cater to different learning styles.
* **Make the activity challenging but achievable** for the student's level.
* **Provide opportunities for students to collaborate** and share ideas.
* **Tailor feedback** to the student's individual needs and learning style.

**By following these guidelines, you can create a stimulating and effective learning experience for your students.**

**Additional Tips:**

* **Get to know your students** and their individual learning styles.
* **Connect the activity to real-world applications** to make it more meaningful.
* **Use technology** to enhance the learning experience.
* **Encourage creativity and self-expression** in the activity.
* **Make learning fun and enjoyable** for your students.

**With your expertise and creativity, you can design a wide range of engaging activities that will inspire and empower your students.**
"""



    #response = model.generate_content(prompt, generation_config=genai.GenerationConfig(candidate_count=1, stop_sequences=['x'], max_output_tokens=20, temperature=1))
    use_sys_inst = True

    model_name = 'gemini-1.5-pro-latest' if use_sys_inst else 'gemini-1.0-pro-latest'
    model = genai.GenerativeModel(
      model_name, system_instruction=PROFESSOR_PROMPT)
    convo = model.start_chat(enable_automatic_function_calling=True)
    return convo.send_message(PROFESSOR_PROMPT.format(
    profile=perfil,
    Educational_level=nivelEducativo,
    career=carrera,
    subject=materia,
    student_age=edad,
    activity_description=descripcionActividad,
    student_preferences=observaciones
    
        )).text