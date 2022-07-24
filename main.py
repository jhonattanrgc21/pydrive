from logging import exception
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

CREDENTIALS = 'credentials.json'

# INICIO DE SESION 
def login():
    ''' 
    Valida las credenciales del usuario.
    Si expiraron, genera nuevas credenciales y actualiza el archivo credentials.json
    En caso contrario, se le otorga el acceso al usuario 
    '''
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(CREDENTIALS)
    
    if gauth.access_token_expired:
        gauth.refresh()
        gauth.SaveCredentialsFile(CREDENTIALS)
    else:
        gauth.Authorize()
    
    return GoogleDrive(gauth)

# CREAR UN NUEVO ARCHIVO EN GOOGLE DRIVE
def create_file(name, content, id_folder):
    '''
    Obtiene los datos del inicio de sesion
    Crea un archivo con el titulo y el id del folder para la ubicacion
    Agrega el contenido al archivo y lo sube a Google Drive
    '''
    credentials = login()
    
    # Creando el archivo mediante su nombre y id del directorio
    new_file = credentials.CreateFile({
        'title': name,
        'parents': [{
            "kind": "drive#fileLink",
            "id": id_folder,
        }],
    })
    
    # Agregando contenido y subieron el archivo
    new_file.SetContentString(content)
    new_file.Upload()

# CARGAR UN ARCHIVO DESDE EL ORDENADOR A GOOGLE DRIVE
def upload_file(path, id_folder):
    credentials = login()
    
    # Creando el archivo mediante su nombre y id del directorio
    file = credentials.CreateFile({
        'title': path.split('/')[-1],
        'parents': [{
            "kind": "drive#fileLink",
            "id": id_folder,
        }],
    })
    
     # Agregando contenido y subieron el archivo
    file.SetContentFile(path)
    file.Upload()

# DESCARGAR ARCHIVO DE GOOGLE DRIVE AL ORDENADOR        
def download_file(id_file, download_path):
    credentials = login()
    
    # Creando el archivo mediante su nombre y id del directorio
    file = credentials.CreateFile({ 'id': id_file })
    file_name = file['title']
    file.GetContentFile(download_path + file_name)
    
# CUERPO PRINCIPAL
def main():
    #create_file('test.txt', 'Esto es una prueba usando PyDrive2!', "13HgFJ0NJyaEUk82pQ9HVKQ8Z0W9NYMzB")
    #upload_file('/home/jhonattanrgc21/Documentos/meme.png', "13HgFJ0NJyaEUk82pQ9HVKQ8Z0W9NYMzB")
    download_file("16fzu5zcfFDy5BOFpGtbT6Z4EczqcUreJ", '/home/jhonattanrgc21/Descargas/')
if __name__ == '__main__':
    main()