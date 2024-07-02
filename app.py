from flask import Flask, jsonify, request

# Estatus 200, OK
# Estatus 201, Created
# Estatus 400, Bad Request
# Estatus 401, Unauthorized -> No autorizado (Sesion)
# Estatus 403, No Tienes permisos (Acceso/Rol)
# Estatus 404, Not Found
# Estatus 415, Content Type not Accepted
# Estatus 500, Servidor

# app -> es comun pero no obligacion
app = Flask(__name__)

# Encapsulacion. Todo lo relevante a manipular los datos de la clase
# Debe vivir dentro de la clase

# <Objt Estudiante#7411521>

class Estudiante:
    def __init__(self, nombre, id):
        self.name = nombre
        self.id = id

    # Metodos
    # Agregan a nivel del init

    def update(self, name):
        self.name = name

    def serialize(self):
        # Permitir que el objeto sea accesible
        # Por cosas externas a la aplicaion
        return {
            "name": self.name,
            "id": self.id
        }
    
estudiantes = []

@app.route("/", methods=["GET"])
def get_app():
    return "Soy una API de flask"

# CRUD Create Read Update Delete
# Usuario: Crear, Ver, Modificar, Borrar
# Post: Crear, Ver, Modificar y Borrar
# Comentario: Crear, ver, modificar y borrar
# Estudiantes:
# Metodo Get -> Ver todos los estudiantes
# Metodo Post -> Para crear un nuevo estudiante
# Modo Get -> Para ver un estudiante

@app.route("/estudiantes", methods=["GET"])
def get_estudiantes():
    estudiantes_serializados = list(map(lambda estudiante: estudiante.serialize(), estudiantes))
    return jsonify({    
        "estudiantes": estudiantes_serializados,
        "cantidad": len(estudiantes)
    })

# Metodo methods=["GET"] -> GET
@app.route("/estudiante/<int:id>")
def get_estudiante_by_id(id):
    for estudiante in estudiantes:
        if estudiante.id == id:
            return jsonify(estudiante.serialize())
        
    # Retornamos un error 404 por defecto
    return jsonify({
        "error": "Estudiante no encontrado :("
    }), 404

@app.route("/estudiante", methods=["POST"])
def crear_estudiante():
    body = request.get_json()
    name = body.get("name", None) # body["name"]
    id = body.get("id", None) 

    if id is None:
        # BE -> FE
        return jsonify({"error": "El id es requerido"}), 400
    if name is None:
        return jsonify({"error": "El name es requerido"}), 400

    # Creamos una instancia de la clase
    estudiante = Estudiante(name, id)

    # Agregamos un estudiante a la lista de estudiantes
    estudiantes.append(estudiante)

    # Es que cuando creemos siempre retornemos estatus 201
    return jsonify(estudiante.serialize()), 201

@app.route("/estudiante/<int:id>", methods=["DELETE"])
def delete_estudent(id):
    for estudiante in estudiantes:
        if estudiante.id == id:
            estudiantes.remove(estudiante)
            return jsonify({"msg": "Estudiante eliminado"}), 200
    # Significa que no lo encontro
    return jsonify({"error": "Estudiante not found"}), 404

@app.route("/estudiante/<int:id>", methods=["PUT"])
def update_estudent(id):
    body = request.get_json()
    name = body.get("name", None)

    if name is None or name == "":
        return jsonify({"error": "El name es requerido"}), 400
    
    # Encontrar al estudiante que quiero actualizar
    # ejecutar el metodo update de ese estudiante
    # Y retornarlo

    for estudiante in estudiantes:
        if estudiante.id == id:
            estudiante.update(name)
            return jsonify(estudiante.serialize()), 200
        
    return jsonify({"error": "Estudiante no encontrado"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')
