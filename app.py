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

class CustomError(Exception):
    def __init__(self, status, msg):
        super().__init__(self)
        self.status = status
        self.msg = msg

class User:
    # metodo constructor
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        
    # Para enviar la informacion a un cliente 
    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
        }
    
usuarios = []

@app.route("/", methods=["GET"])
def get_app():
    # JSON: JavaScript Object Notation
    return jsonify("El servidor esta corriendo")

# ENDPOINTS
"""
GET = Obtener datos
POST = Crear algo nuevo / Para enviar informacion
PUT = Editar algo que ya existe
DELETE = Eliminar algo que ya existe

Crear una cuenta/Registro de usuario - POST
Iniciar sesion - GET
Obtener sus datos - GET

Si un endpoint requiere mas de una palabra en su ruta:
separamos-con-guiones
"""
# localhost:8000/ register / signup
@app.route("/signup", methods=["POST"])
def signup():
    """
    Creates an user account with email, username, password
    """
    request_body = request.get_json(force=True)
    # Uno siempre deberia validar esa data
    username = request_body.get("username", None)
    email = request_body.get("email", None)
    password = request_body.get("password", None)
    
    # Es validacion de inputs
    if username is None or username.strip() == "":
        return jsonify({"error": "El username es requerido"}), 400
    if email is None or email.strip() == "":
        return jsonify({"error": "El email es requerido"}), 400
    if password is None or password.strip() == "":
        return jsonify({"error": "El password es requerido"}), 400

    # Validamos que son unicos
    for usuario in usuarios:
        if username == usuario.username:
            return jsonify({"error": "El usuario ya esta uso"}), 400
        if email == usuario.email:
            return jsonify({"error": "El correo ya esta en uso"}), 400
    
    invalid_characters = ["%", ",", "<", ">"]
    for character in invalid_characters:
        if character in username:
            return jsonify({"error": "Caracter invalido", "no_permitidos": invalid_characters}), 400

    new_user = User(username, email, password)
    usuarios.append(new_user)
    return jsonify({"msg": "Se ha creado con exito"}), 201

@app.route("/signin", methods=["POST"])
def signin():
    # Que creen que deberiamos hacer para recibir password y correo?
    # intenta y atrapa / try and catch
    try:
        body_request = request.get_json(force=True)
        email = body_request["email"]
        password = body_request["password"]

        for usuario in usuarios:
            if usuario.email == email:
                if usuario.password == password:
                    return jsonify({"msg": "Bienvenido de vuelta"}), 200
                else:
                    raise CustomError(400, "Contrasenas deben ser iguales")
        
        # throw new Error()
        raise CustomError(404, "Usuario no encontrado")
        
    # Es sintaxis bastante comun en Python cuando se trata un error/excepcion
    except Exception as error:
        if isinstance(error, KeyError):
            return jsonify({"error": f"{error.__str__()}: es requerido"}), 400
        
        # Rabbit hole
        if isinstance(error, CustomError):
            return jsonify({"error": error.msg}), error.status
        
        # 500 Internal server error
        return jsonify({"error": error.__str__()}), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0')
