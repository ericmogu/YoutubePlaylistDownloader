# Instalar librerias no nativas en caso de no exisitir

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('yt_dlp')

 
# Importar librerias


import os
import subprocess
import urllib.request
import zipfile
import shutil
import yt_dlp
import re


# Funcion para descargar la aplicacion ffmpeg 


def download_ffmpeg(download_url, extract_to):
    ffmpeg_zip = os.path.join(extract_to, 'ffmpeg.zip')
    urllib.request.urlretrieve(download_url, ffmpeg_zip)
    with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_to) 
    os.remove(ffmpeg_zip)
    for folder_name in os.listdir(extract_to):
        if 'ffmpeg' in folder_name:
            return os.path.join(extract_to, folder_name, 'bin')
    return None


# Agregar ffmpeg al PATH de entorno local


def add_to_path(ffmpeg_bin_path):
    current_path = os.environ['PATH']
    if ffmpeg_bin_path not in current_path:
        os.environ['PATH'] = current_path + os.pathsep + ffmpeg_bin_path
        subprocess.run(['setx', 'PATH', f'{current_path}{os.pathsep}{ffmpeg_bin_path}'], shell=True)


# Llamado a las funciones para descargar e instalar, valida si existe el archivo y omite el proceso en caso de que ya exista 


extract = os.path.join('C:', 'ffmpeg-7.0.1')
if  os.path.exists(extract):
        print('El archivo existe en el directorio') 
else:    
    def main():
        download_url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
        if  os.path.exists(extract):
            print('El archivo existe en el directorio')
        else:
            os.makedirs(extract)
        ffmpeg_bin_path = download_ffmpeg(download_url, extract)
        if ffmpeg_bin_path:
            add_to_path(ffmpeg_bin_path)
            print('ffmpeg instalado y agregado al PATH con éxito.')
        else:
            print('Error al instalar ffmpeg.')
    if __name__ == "__main__":
        main()


# # Inicio del proceso de descarga en YouTube
# 
# 
# ### por favor agrega aqui la direccion de la playlist


playlist_url = "https://www.youtube.com/playlist?list=PLkVpKYNT_U9cDvqUqVVyI_Qo2OHRr9NPs"


# Se define una función para crear una carpeta en base al nombre de la playlist, sin caracteres especiales


def clean_name(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)


# Se crea el directorio Mis Videos en la ruta Documentos


save_path = os.path.join(os.path.expanduser("~/Documents"), "Mis Videos")


# Parametros de configuracion de la liberia yt_ltp


ydl_opts = {
    'outtmpl': os.path.join(save_path, '%(playlist_title)s', '%(title)s.%(ext)s'),
    'format': 'bestvideo+bestaudio/best',
    'noplaylist': False,
    'merge_output_format': 'mp4'
}


# Analiza el Json de la playlist y extrae enlaces y nombres, crea la carpeta con base al nombre de la playlist


with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(playlist_url, download=False)
     
    if 'title' in info_dict:
        playlist_title = clean_name(info_dict['title'])
        playlist_folder = os.path.join(save_path, playlist_title)
        if not os.path.exists(playlist_folder):
            os.makedirs(playlist_folder)
        ydl_opts['outtmpl'] = os.path.join(playlist_folder, '%(title)s.%(ext)s')
    else:
        print("No se pudo obtener el título de la playlist.")
        exit(1)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

print('¡Descarga de la playlist completada!')


