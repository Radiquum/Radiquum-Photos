from PIL import Image, ExifTags
import os
from shutil import copy, copytree
from airium import Airium


INPUT = 'gallery'
OUTPUT = 'web'
LARGE_SIZE = [1000, 1000]
SMALL_SIZE = [300, 300]


def prepare_images():
    print('Finding images...')
    image_array = next(os.walk(INPUT))
    print(f'Found: {len(image_array[2])}')

    print('Creating folders...')
    os.makedirs(f'{OUTPUT}/media/original', exist_ok=True)
    os.makedirs(f'{OUTPUT}/media/large', exist_ok=True)
    os.makedirs(f'{OUTPUT}/media/small', exist_ok=True)
    
    image_array_check = ['something', 'something', []]
    image_array_check = next(os.walk(f'{OUTPUT}/media/original'))

    for count, image in enumerate(image_array[2], start=1):
        
        if image in image_array_check[2]:
            continue
        
        print(f'Processing image {count}/{len(image_array[2]) - len(image_array_check[2])}')
        copy(f'{INPUT}/{image}', f'{OUTPUT}/media/original/{image}')
        
        with Image.open(f'{INPUT}/{image}') as im:
            im.thumbnail(LARGE_SIZE, Image.LANCZOS)
            im.save(f'{OUTPUT}/media/large/{image}')

            im.thumbnail(SMALL_SIZE, Image.LANCZOS)
            im.save(f'{OUTPUT}/media/small/{image}')
            
    prepape_website(image_array[2])
    return True

def prepape_website(images):
    a = Airium()
    
    copytree('./public', f'{OUTPUT}/public', dirs_exist_ok=True)
    
    print('Creating website...')
    a('<!DOCTYPE html>')
    with a.html(lang="en"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(_t="Radiquum Photos")
            a.link(rel="stylesheet", href="public/index.css")

        with a.body(klass="adaptive"):
            with a.nav():
                with a.h1(style="font-weight: 600;"):
                    a('Radiquum')
                with a.p():
                    a('Photos')
                with a.a(href="https://bento.me/radiquum", klass="bento"):
                    a.img(src="public/Bento-Logo.svg", klass="bento")
                        
        with a.div(klass="modal", id="modal"):
            a.img(klass="modal-image modal-content", id="modal-image", src="media/large/image")
           #  a.img(klass="modal-image modal-background", id="modal-background", src="media/large/image")
            with a.div(klass="image-nav", id="image-nav"):
                with a.span(id="copy"):
                    a('📋') 
                with a.a('download', id="download", href="media/original/image"):
                    a('💾') 
                with a.span(id="close"):
                    a('❌') 
                        
        with a.images():
            for image in images:
                a.div(klass="img", style=f"background-image: url(media/small/{image})", large=f"media/large/{image}")
                    
            a.script(type='text/javascript', src='public/preview.js')
                    

    html = str(a)
    with open(f'{OUTPUT}/index.html', 'w', encoding='utf-8') as index:
        index.write(html)
        
        
if __name__ == "__main__":
    prepare_images()