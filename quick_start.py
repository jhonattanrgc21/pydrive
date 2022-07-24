'''
Genera el archivo credentials.json
almacenando todas las credenciales del usuario
para un inicio de sesion rapido
'''
from pydrive2.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth() 