import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL


server = Flask(__name__)


# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))
mysql = MySQL(server)




@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    cursor = mysql.connection.cursor()
    result_set = cursor.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if result_set > 0:
        user_row = cursor.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401


def createJWT(username:str, secret, isAdmin:bool):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(tz=datetime.timezone.utc),
            "admin": isAdmin
        },
        secret,
        algorithm="HS256"
    )

@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    parsed_token = encoded_jwt.split(" ")
    if parsed_token[0] != 'Bearer' :
        return "Method not allowed", 405

    try:
        decoded_token = jwt.decode(
            parsed_token[1], os.environ.get("JWT_SECRET"), algorithms=['HS256']
        )
    except:
        return "Unauthorized", 403

    return decoded_token, 200

if __name__=='__main__':
    server.run(host='0.0.0.0', port=5000)


