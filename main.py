# Imports

from PIL import Image, ImageOps
import os
from shutil import copy, copytree
from airium import Airium
import json


# Default config

CONFIG = {
    "INPUT": 'gallery',
    "OUTPUT": 'web',
    "LARGE_SIZE": [1000, 1000],
    "SMALL_SIZE": [500, 500],
    "OPENGRAPH": {
        "WEBSITE_TITLE": "Radiquum Photos",
        "WEBSITE_DESCRIPTION": "Public gallery of https://bento.me/radiquum",
        "WEBSITE_URL": "https://photos.radiquum.wah.su"
    }
}


# Config loading

config_file = 'config.json'

try:
    if os.path.isfile('config_test.json'):
        config_file = 'config_test.json'
    
    with open(config_file, encoding='utf-8') as config:
        CONFIG = json.load(config)
except FileNotFoundError:
    with open(config_file, 'w', encoding='utf-8') as config:
        config.write(json.dumps(CONFIG, indent=3))
        
INPUT = CONFIG.get('INPUT')
OUTPUT = CONFIG.get('OUTPUT')

# Image resizing

def prepare_images():
    print('Finding images...')
    image_array = next(os.walk(INPUT))
    print(f'Found: {len(image_array[2])}')

    os.makedirs(f'{OUTPUT}/media/original', exist_ok=True)
    os.makedirs(f'{OUTPUT}/media/large', exist_ok=True)
    os.makedirs(f'{OUTPUT}/media/small', exist_ok=True)
    os.makedirs(f'{OUTPUT}/media/exif', exist_ok=True)
    os.makedirs(f'{OUTPUT}/public', exist_ok=True)

    print('Updating images...')
    image_array_check = ['something', 'something', []]
    image_array_check = next(os.walk(f'{OUTPUT}/media/original'))
    print(f'Found New: {len(image_array[2]) - len(image_array_check[2])}')

    for count, image in enumerate(image_array[2], start=1):
        
        if image in image_array_check[2] or image == 'gitkeep':
            continue
        
        print('Processing {0:50} {1}/{2}'.format(image, count, len(image_array[2]) - len(image_array_check[2])))
        copy(f'{INPUT}/{image}', f'{OUTPUT}/media/original/{image}')

        with Image.open(f'{INPUT}/{image}') as im:
            EXIF = im.getexif()
            im = ImageOps.exif_transpose(im)
            
            im.thumbnail(CONFIG.get('LARGE_SIZE'), Image.LANCZOS)
            im.save(f'{OUTPUT}/media/large/{image}')

            im.thumbnail(CONFIG.get('SMALL_SIZE'), Image.LANCZOS)
            im.save(f'{OUTPUT}/media/small/{image}', optimize=True)
            
            im.thumbnail([1, 1], Image.LANCZOS)
            im.save(f'{OUTPUT}/media/exif/{image}', optimize=True, exif=EXIF)
            
    prepare_website(sorted(image_array[2], reverse=True))
    return True

# Website generation

def image_add(a, image, orint):
    with a.div(klass=f"img {orint}", tabindex=0):
        a.img(klass="img clickable", src=f"media/small/{image}", alt=image, loading="lazy", tabindex=-1)
        with a.div(klass="image-overlay {orint}", id="image-overlay"):
            with a.span(id="copy-overlay", klass="material-icons", url=f'media/original/{image}', tabindex=-1):
                a('share')
            with a.a('download', id="download-overlay", klass="material-icons", href=f"media/original/{image}", tabindex=-1):
                a("download")
                            
def prepare_website(images):
    a = Airium()
    
    print('Creating website...')
    copytree('./public', f'{OUTPUT}/public', dirs_exist_ok=True)
    
    a('<!DOCTYPE html>')
    with a.html(lang="en"):
        with a.head():
            a.meta(charset="utf-8")
            a.meta(property="og:title", content=CONFIG["OPENGRAPH"].get("WEBSITE_TITLE"))
            a.meta(property="og:type", content="website")
            a.meta(property="og:description", content=CONFIG["OPENGRAPH"].get("WEBSITE_DESCRIPTION"))
            a.meta(property="og:url", content=CONFIG["OPENGRAPH"].get("WEBSITE_URL"))

            a.title(_t=CONFIG["OPENGRAPH"].get("WEBSITE_TITLE"))
            a.link(rel="stylesheet", href="public/index.css")
            a.link(rel="stylesheet", href="https://fonts.googleapis.com/icon?family=Material+Icons")

        with a.body():
            with a.div(klass="header"):
                with a.h1(style="font-weight: 600;"):
                    a('Radiquum')
                with a.p():
                    a('Photos')
                with a.a(href="https://bento.me/radiquum", klass="bento"):
                    a.img(src="public/Bento-Logo.svg", klass="bento", alt="")
                        
        with a.div(klass="modal", id="modal"):
            a.img(klass="modal-image modal-content", id="modal-image", src="", alt="")
            a.div(klass="modal-background", id="modal-background")
            with a.div(klass="modal-navigation", id="modal-navigation"):
                with a.span(id="copy", klass="material-icons"):
                    a('share')
                with a.a('download', id="download", klass="material-icons", href=""):
                    a('download')
                with a.span(id="info", klass="material-icons"):
                    a("info") 
                with a.span(id="close", klass="material-icons"):
                    a("close") 
                        
        with a.images():
            for image in images:
                if image == 'gitkeep':
                    continue
                
                with Image.open(f'{OUTPUT}/media/small/{image}') as im:
                    if im.width > im.height:
                        image_add(a, image, 'horizontal')
                    elif im.width == im.height :
                        image_add(a, image, 'square')
                    else:
                        image_add(a, image, 'vertical')
                    
        a.script(type='text/javascript', src='public/preview.js')
        a.script(type='text/javascript', src='public/tags.js')
        a.script(type='text/javascript', src='https://cdn.jsdelivr.net/npm/exif-js')
                    

    html = str(a)
    with open(f'{OUTPUT}/index.html', 'w', encoding='utf-8') as index:
        index.write(html)
        
        
if __name__ == "__main__":
    prepare_images()