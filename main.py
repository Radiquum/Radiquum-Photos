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
        "WEBSITE_URL": "https://photos.radiquum.wah.su",
        "WEBSITE_IMAGE": None
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
    Image_List = sorted(image_array[2], reverse=True)
    
    #generate og:image
    
    opengraph_image = Image.open(f'{OUTPUT}/media/large/{Image_List[0]}')
    opengraph_foreground = Image.open(f"{OUTPUT}/public/favicon/android-chrome-256x256.png")
    img_w, img_h = opengraph_foreground.size
    bg_w, bg_h = opengraph_image.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    opengraph_image.paste(opengraph_foreground, offset, opengraph_foreground)
    
    opengraph_image.save(f"{OUTPUT}/public/opengraph.png")
    opengraph_foreground.close()
    opengraph_image.close()
    
    CONFIG["OPENGRAPH"]["WEBSITE_IMAGE"] = f'{CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/public/opengraph.png'
    
    prepare_website(Image_List)
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
                            
def prepare_website(images):  # sourcery skip: extract-method
    a = Airium()
    
    print('Creating website...')
    copytree('./public', f'{OUTPUT}/public', dirs_exist_ok=True)
    
    a('<!DOCTYPE html>')
    with a.html(lang="en"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(_t=CONFIG["OPENGRAPH"].get("WEBSITE_TITLE"))
            a.meta(name="description", content=CONFIG["OPENGRAPH"].get("WEBSITE_DESCRIPTION"))
            
            a.link(rel="apple-touch-icon", sizes="180x180", href="/public/favicon/apple-touch-icon.png")
            a.link(rel="icon", type="image/png", sizes="32x32", href="/public/favicon/favicon-32x32.png")
            a.link(rel="icon", type="image/png", sizes="16x16", href="/public/favicon/favicon-16x16.png")
            a.link(rel="manifest", href="/public/favicon/site.webmanifest")
            a.link(rel="mask-icon", href="/public/favicon/safari-pinned-tab.svg", color="#5bbad5")
            a.link(rel="shortcut icon", href="/public/favicon/favicon.ico")
            a.meta(name="msapplication-TileColor", content="#da532c")
            a.meta(name="msapplication-config", content="/public/favicon/browserconfig.xml")
            a.meta(name="theme-color", content="#ffffff")
            
            a.meta(property="og:title", content=CONFIG["OPENGRAPH"].get("WEBSITE_TITLE"))
            a.meta(property="twitter:title", content=CONFIG["OPENGRAPH"].get("WEBSITE_TITLE"))
            a.meta(property="og:type", content="website")
            a.meta(property="og:description", content=CONFIG["OPENGRAPH"].get("WEBSITE_DESCRIPTION"))
            a.meta(property="twitter:description", content=CONFIG["OPENGRAPH"].get("WEBSITE_DESCRIPTION"))
            a.meta(property="og:url", content=CONFIG["OPENGRAPH"].get("WEBSITE_URL"))
            a.meta(property="og:image", content=CONFIG["OPENGRAPH"].get("WEBSITE_IMAGE"))
            a.meta(property="twitter:image", content=CONFIG["OPENGRAPH"].get("WEBSITE_IMAGE"))
            a.meta(property="twitter:card", content="summary_large_image")
            
            
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