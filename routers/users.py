from fastapi import APIRouter, HTTPException, status
from db.models.userModel import User
from db.client import dbClient
from db.schemas.user import userSchema, usersSchema

from bson import ObjectId



routerUsers = APIRouter(prefix = "/users", responses = {"404": {"ERROR": "Ruta no encontrada"}}, tags = ["PRODUCTS"])

##---METODO GET TODOS LOS USERS
@routerUsers.get("/", response_model = list[User])
async def users():
    return usersSchema(dbClient.local.users.find())
    # En este caso usaremos userSchema que recibe un objeto y lo retorna como un diccionario
    # despues le pasaremos como parametro lo que encuentre la funcion find en nuestra base
    # de datos, asi esta le pasara un usuario en formato json a nuestro. userschema y este
    # lo transformata en un diccionario, cada uno de los usuario, sera esto lo que retornemos
    # como una lista de usuarios


#---METODO GET USER POR ID
routerUsers.get("/{id}")
async def user(id: str):
    return searchUser("_id", ObjectId(id))

##---METODO POST
@routerUsers.post("/", response_model = User, status_code = status.HTTP_201_CREATED)
async def createUser(user: User):

    # Primero validaremos que no exita un usuario con nombre de usuario o email iguales
    # a los que le estamos pasando
    if type(searchUser("userName", user.userName)) == User:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Ya existe un usuario con este nombre de usuario")
    
    if type(searchUser("email", user.email)) == User:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Ya existe un usuario con este email")
    
    userDict = dict(user)
    del userDict["id"]

    idUser = dbClient.local.users.insert_one(userDict).inserted_id
    # Aca vamos a capturar el id con el que creo a nuestro usuario para verificar que el usuario fue
    # insertado correctamente

    newUser = userSchema(dbClient.local.users.find_one({"_id": idUser}))
    return User(**newUser)




#----------------------------------------------------------------------------------------
##---FUNCIONES
def searchUser(key: str, value) -> User:
    try:
        user = dbClient.local.users.find_one({key: value})
        if not user:
            raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail = f"Usuario no encontrado con {key} = {value}" )
            # Aca validaremos que la busqueda en la base de datos me haya retornado
            # algo, de lo contrario retornaremos que el usuario no ha sido encontrado 
        
        # user["_id"] = str(user["_id"])
        # # Aca estamos convirtiendo el campo de objectId y lo convetimos a string
        # # para poder hacer la contruccion del objeto User
        
        return User(**user)
    except:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail = "Usuario no encontrado" )
