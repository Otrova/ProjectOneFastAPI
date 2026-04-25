
def userSchema(user) -> dict:
    return {
            "id": str(user["_id"]),
            "userName": user["userName"],
            "age": user["age"],
            "email": user["email"],
            "isActive": user["isActive"],
            "password": user["password"]
            }

def usersSchema(users) -> list:
    return [userSchema(user) for user in users]