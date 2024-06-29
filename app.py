# Aqui vamos a importar flask
from flask import Flask, jsonify, request

# Esta linea instancia nuestra app de flask
app = Flask(__name__)

class Estudiante:
    def __init__(self, nombre, id):
        self.name = nombre
        self.id = id

    def serialize(self):
        return {
            "name": self.name,
            "id": self.id
        }
    
estudiantes = []
# URLs dentro de nuestra API que se encargan de distribuir informacion en concreto
# Un endpoint con el metodo get
# localhost:8000/
@app.route("/", methods=["GET"])
def get_app():
    return "Soy una API de flask"

# Un decorador es una funcion que se ejecuta antes de otra funcion
# localhost:8000/saluda
@app.route("/saluda", methods=["GET"])
def saluda(): # El nombre de la funcion me lo invento
    return "Hola que tal?"

@app.route("/estudiantes", methods=["GET"])
def get_estudiantes():
    # Usando un bucle comun
    # estudiantes_serializados = []
    # for estudiante in estudiantes:
    #     estudiantes_serializados.append(estudiante.serialize())

    # Usando comprehensive list:
    # estudiantes_serializados = [estudiante.serialize for estudiante in estudiantes]

    # Usando el map()
    estudiantes_serializados = list(map(lambda estudiante: estudiante.serialize(), estudiantes))
    return jsonify({    
        "estudiantes": estudiantes_serializados,
        "cantidad": len(estudiantes)
    })

@app.route("/estudiante", methods=["POST"])
def crear_estudiante():
    body = request.get_json() # {}
    # Tenemos que recibir el nombre y el id
    name = body.get("name", None) # diccionario["key"]
    id = body.get("id", None) # No es OPCIONAl

    if id is None:
        return jsonify({"error": "El id es requerido"}), 400
    if name is None:
        return jsonify({"error": "El name es requerido"}), 400

    # crear una nueva instancia de la clase
    estudiante = Estudiante(name, id)

    # agregarlo a la list estudiantes
    estudiantes.append(estudiante)
    # retornar correctamente la data <Object Estudiante at #1230981230192>
    return jsonify(estudiante.serialize())

# Parametro para hacer la ruta dinamica
# @app.route("<tipo_dato:nombre_variable>")
# def nombre_generico(nombre_variable)
@app.route("/estudiante/<int:id>")
def get_estudiante_by_id(id):
    for estudiante in estudiantes:
        if estudiante.id == id:
            return jsonify(estudiante.serialize())
    return jsonify({
        "error": "Estudiante no encontrado :("
    }), 404


# Hot reload: Cuando haces un cambio se actualiza la app
# Esto es lo que inicia la aplicacion como tal
if __name__ == "__main__":
    app.run(host='0.0.0.0')
