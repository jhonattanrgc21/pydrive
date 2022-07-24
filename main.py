import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

CREDENTIALS = 'config/credentials.json'

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
        gauth.Refresh()
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
    
# BUSCAR ARCHIVOS EN GOOGLE DRIVE
def search(query):
    '''
    Retorna una lista de archivos correspondientes a la query de entrada.
    La query puede ser: title, id, embedLink, downloadUrl, mimeType, createdDate', modifiedDate', fileSize
    Si no se envia una query, se puede obtener la lista de todos los archivos que esten en Google Drive
    '''
    
    response = []
    credentials = login()
    
    '''
    Se pueden utilizar parametros adicionales como filtros de busqueda
    para la operacion ListFile
    
    Los parametros adicionales se pueden consultar aqui: https://developers.google.com/drive/api/v3/reference/files/list
    '''
    #list_file = credentials.ListFile().GetList()
    list_file = credentials.ListFile({'q': query}).GetList()

    # Recorre la lista de archivos encontrados
    i = 1
    for f in list_file:
        print('\nItem: ', i)
        
        # ID Drive
        print('ID Drive:',f['id'])
        # Link de visualizacion embebido
        print('Link de visualizacion embebido:',f['embedLink'])
        # Nombre del archivo
        print('Nombre del archivo:',f['title'])
        # Tipo de archivo
        print('Tipo de archivo:',f['mimeType'])
        # Esta en el basurero
        print('Esta en el basurero:',f['labels']['trashed'])
        # Fecha de creacion
        print('Fecha de creacion:',f['createdDate'])
        # Fecha de ultima modificacion
        print('Fecha de ultima modificacion:',f['modifiedDate'])
        # Version
        print('Version:',f['version'])
        
        try:
            # Link de descarga
            print('Link de descarga:',f['downloadUrl'])
        except:
            pass

        try:
            # Tamanio
            print('Tamanio:',f['fileSize'])
        except:
            pass
            
        response.append(f)
        i += 1
    
    return response

# BORRAR/RECUPERAR ARCHIVOS EN GOOGLE DRIVE
def delete_recuperate(id_file):
    '''
    Recibe el id de un archivo que este en Google Drive.
    Sobre el se pueden aplicar operaciones de eliminar o restaurar.
    '''
    
    credenciales = login()
    file = credenciales.CreateFile({'id': id_file})
    
    try:
        '''
        Se pueden utilizar 3 metodos
        
        - Mover al basurero: file.Trash()
        - Recuperar del basurero: file.Trash()
        - Eliminar permanentemente: file.Delete()
        
        Para este ejemplo se usara la operacion de mover al basurero
        '''
        file.Trash()
    except:
        print('Error, el archivo con ese id no existe')
    
# CREAR CARPETA
def create_folder(name_folder, id_folder):
    '''
    Recibe el nombre de la carpeta  el id para la ubicacion
    '''
    
    credenciales = login()
    
    folder = credenciales.CreateFile({
        'title': name_folder, 
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{
            "kind": "drive#fileLink",
            "id": id_folder
            }]
    })
    
    folder.Upload()

# CUERPO PRINCIPAL
def main():
    file_name = 'test2.txt'
    folder_name = 'Prueba3'
    file_content = 'Esto es una prueba usando PyDrive2!'
    id_file = '1nIv16WMCWFFTimEE8A1jPrmvouLqs9H2'
    id_folder = '13HgFJ0NJyaEUk82pQ9HVKQ8Z0W9NYMzB'
    file_path = '/home/jhonattanrgc21/Documentos/meme.png'
    download_path = '/home/jhonattanrgc21/Descargas/'
    
    
    #create_file(file_name, file_content, id_folder)
    #upload_file(file_path, id_folder)
    #download_file(id_file , download_path)
    search("title = 'meme.png'")
    #delete_recuperate(id_file)
    #create_folder(folder_name, id_folder)
    pass

if __name__ == '__main__':
    if not (os.path.exists('config/credentials.json')):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth() 
        
    main()