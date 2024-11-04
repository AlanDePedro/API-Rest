


from typing import Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#se inicia la variable que tendra las caracteristicas de la apirest
app = FastAPI()

#defino el modelo
class Curso(BaseModel):
    id: Optional [str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

    #simulo una base de datos
cursos_db = []

    #CRUD: Read (lectura) GET ALL: se lee todos los cursos que haya en la db
@app.get("/cursos/", response_model=list[Curso])
def obtener_cursos():
        return cursos_db
    
#CRUD: Create (escribir) POST: se agrega un nuevo recurso a nuestra base de datos
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) #UUID me sirve para generar un ID unico e irrepetible
    cursos_db.append(curso)
    return curso

#CRUD: Read (lectura) GET (individual): se va a leer el curso que coincida con el ID que se pida
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id: str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

#CRUD: Update (Actualizar/Modificar) PUT: se modifca un recurso que coincida con el ID que mandamos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id: str, curso_actualizado: Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso)  # buscar el índice exacto del curso en la lista
    cursos_db[index] = curso_actualizado
    return curso_actualizado

#CRUD: Delete (borrado/baja) DELETE : se elimina un recurso que coincida con el ID que mandemos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) #con next se toma la primera coincicendia del array del curso
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso