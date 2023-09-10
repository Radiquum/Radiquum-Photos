# Imports

from PIL import Image, ImageOps
import os
from shutil import copy, copytree, make_archive
from airium import Airium
import json
import datetime
import os.path
import json

# Default config

CONFIG = {
    "INPUT": 'gallery',
    "OUTPUT": 'web',
    "LARGE_SIZE": [1000, 1000],
    "SMALL_SIZE": [300, 300],
    "LITE_SIZE": [100,100],
    "ZIP": False,
    "LITE": False,
    "WEB":
        {
            "TITLE": '<h1 style="font-weight: 600;">Radiquum</h1><p>Photos</p>',
            "SOCIAL_IMG": 'Bento-Logo.svg',
            "SOCIAL_URL":  'https://bento.me/radiquum',
            "USE_CDN": True,
        },
    
    "OPENGRAPH": {
        "WEBSITE_TITLE": "Radiquum Photos",
        "WEBSITE_DESCRIPTION": "Public gallery of https://bento.me/radiquum",
        "WEBSITE_URL": "https://photos.radiquum.wah.su",
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

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def prepare_images():
    print('Finding images...')
    image_array = next(os.walk(INPUT))
    print(f'Found: {len(image_array[2])}')

    os.makedirs(f'{OUTPUT}/media/original', exist_ok=True)
    os.makedirs(f'{OUTPUT}/media/large', exist_ok=True)
    if CONFIG["WEB"].get("USE_CDN") != True:
        os.makedirs(f'{OUTPUT}/media/small', exist_ok=True)
    if  CONFIG.get("LITE") == True:
        os.makedirs(f'{OUTPUT}/lite', exist_ok=True)
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
            image_orig = ImageOps.exif_transpose(im)
            EXIF = image_orig.getexif()
            
            image_orig.thumbnail(CONFIG.get('LARGE_SIZE'), Image.LANCZOS)
            image_orig.save(f'{OUTPUT}/media/large/{image}', exif=EXIF)
            
            if CONFIG["WEB"].get("USE_CDN") != True:
                image_orig.thumbnail(CONFIG.get('SMALL_SIZE'), Image.LANCZOS)
                image_orig.save(f'{OUTPUT}/media/small/{image}', optimize=True, quality=100)
                image_orig.thumbnail([25, 25], Image.LANCZOS)
                image_orig.save(f'{OUTPUT}/media/small/25-{image}', optimize=True, quality=100)
            image_orig.close()
            if CONFIG.get('LITE') == True:
                json_file = os.path.splitext(image)[0] + '.json'
                sizes = []
                im.thumbnail(CONFIG.get('LITE_SIZE'), Image.LANCZOS)
                im.save(f'{OUTPUT}/lite/{os.path.splitext(image)[0]}{im.width}x{im.height}{os.path.splitext(image)[1]}', optimize=True, quality=80)
                sizes.append(im.size)
                if im.width < 128:
                    space = int((128 - im.width)/2)
                    img = add_margin(im, 0, space, 0, space, 'black')
                    img.save(f'{OUTPUT}/lite/{os.path.splitext(image)[0]}{img.width}x{img.height}{os.path.splitext(image)[1]}', optimize=True, quality=80)
                    sizes.append(img.size)
                with open(f'{OUTPUT}/lite/{json_file}', 'w', encoding='utf-8') as file:
                    file.write(json.dumps(sizes))
    
    if CONFIG.get("ZIP") == True:
        print('Creating ZIP...')
        make_archive(f'{OUTPUT}/public/{datetime.datetime.now():%Y-%m-%d}', 'zip', INPUT)
    
    prepare_website(sorted(image_array[2], reverse=True))
    return True

# Website generation

def image_add(a, image, orint):
    if CONFIG["WEB"].get("USE_CDN") == True:
        with a.div(klass=f"img {orint} blur-img", style=f'background-image: url(//wsrv.nl/?url={CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/media/large/{image}&w=25&h=25)'):
            a.img(klass="img clickable",\
                srcset=f'//wsrv.nl/?url={CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/media/large/{image}&w=175&h=175 175w, \
                    //wsrv.nl/?url={CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/media/large/{image}&w=300&h=300 300w, \
                    //wsrv.nl/?url={CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/media/large/{image}&w=475&h=475 475w',\
                    sizes="(max-width: 700px) 175px, (max-resolution: 1dppx) and (min-width: 1400px) 475px, 300px",\
                    src=f'//wsrv.nl/?url={CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/media/large/{image}&w=475&h=475', loading="lazy", alt=image, tabindex=0)
            
            with a.div(klass="image-overlay", id="image-overlay"):
                with a.span(id="copy-overlay", klass="material-icons", url=f'media/original/{image}', tabindex=-1):
                    a('share')
                with a.a('download', id="download-overlay", klass="material-icons", href=f"media/original/{image}", tabindex=-1):
                    a("download")
    else:
        with a.div(klass=f"img {orint} blur-img", style=f'background-image: url(media/small/25-{image})'):
            a.img(klass="img clickable", src=f"media/small/{image}", alt=image, loading="lazy", tabindex=0)
            with a.div(klass="image-overlay", id="image-overlay"):
                with a.span(id="copy-overlay", klass="material-icons", url=f'media/original/{image}', tabindex=-1):
                    a('share')
                with a.a('download', id="download-overlay", klass="material-icons", href=f"media/original/{image}", tabindex=-1):
                    a("download")
                            
def prepare_website(images):  # sourcery skip: extract-method
    a = Airium()
    
    print('Creating website...')
    copytree('./public', f'{OUTPUT}/public', dirs_exist_ok=True)
    
    #generate og:image
    OPENGRAPH_IMAGE = None
    if images[0] != 'gitkeep':
        opengraph_image = Image.open(f'{OUTPUT}/media/large/{images[0]}')
        opengraph_foreground = Image.open(f"{OUTPUT}/public/favicon/android-chrome-256x256.png")
        img_w, img_h = opengraph_foreground.size
        bg_w, bg_h = opengraph_image.size
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        opengraph_image.paste(opengraph_foreground, offset, opengraph_foreground)
        
        opengraph_image.save(f"{OUTPUT}/public/opengraph.png")
        opengraph_foreground.close()
        opengraph_image.close()
    
        OPENGRAPH_IMAGE = f'{CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/public/opengraph.png'
    
    a('<!DOCTYPE html>')
    with a.html(lang="en"):
        with a.head():
            a.meta(charset="utf-8")
            a.meta(name="viewport", content="width=device-width")
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
            if OPENGRAPH_IMAGE is not None:
                a.meta(property="og:image", content=OPENGRAPH_IMAGE)
                a.meta(property="twitter:image", content=OPENGRAPH_IMAGE)
            a.meta(property="twitter:card", content="summary_large_image")
            
            
            a.link(rel="stylesheet", href="public/index.css")
            if CONFIG.get('RSS') == True:    
                a.link(rel="alternate", type="application/rss+xml", title=CONFIG["OPENGRAPH"].get("WEBSITE_TITLE"), href=f'{CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/feed.xml')

        with a.body():
            with a.div(klass="header"):
                with a.div(klass="header-title"):
                    a(CONFIG['WEB'].get('TITLE'))
                with a.div(klass="header-links"):
                    if CONFIG['WEB'].get('SOCIAL_URL') is not None and CONFIG['WEB'].get('SOCIAL_IMG') is not None:
                        with a.a(href=CONFIG['WEB'].get('SOCIAL_URL'), klass="social"):
                            a.img(src=f"public/{CONFIG['WEB'].get('SOCIAL_IMG')}", klass="social", alt="Social Link.")
                    with a.span(id="share", klass="material-icons"):
                        a('share')
                    if os.path.isfile(f"{OUTPUT}/public/{datetime.datetime.now():%Y-%m-%d}.zip"):
                        with a.a('download', href=f"public/{datetime.datetime.now():%Y-%m-%d}.zip", klass="zip material-icons"):
                            a('folder_zip')
                    if CONFIG.get('RSS') == True:    
                        with a.a(href="feed.xml", klass="material-icons"):
                            a('rss_feed')
                    if CONFIG.get('LITE') == True:
                        with a.a(href="lite/", klass="material-icons"):
                            a('data_saver_on')
                        
        with a.div(klass="modal", id="modal"):
            with a.div(klass="modal-content blur-modal", id="modal-image-background"):
                a.img(klass="modal-image", id="modal-image", src="", alt="")
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
                
                with Image.open(f'{OUTPUT}/media/large/{image}') as im:
                    if im.width > im.height:
                        image_add(a, image, 'horizontal')
                    elif im.width == im.height :
                        image_add(a, image, 'square')
                    else:
                        image_add(a, image, 'vertical')
                        
        with a.div(klass="copy-popup", id="copy-popup"):
            with a.span(klass="material-icons"):
                a('check_circle')
            with a.p():
                a('link copied!')
                    
        a.script(type='text/javascript', src='public/images.js')
        a.script(type='text/javascript', src='public/preview.js')
        a.script(type='text/javascript', src='public/copy.js')
        a.script(type='text/javascript', src='public/tags.js')
        a.script(type='text/javascript', src='https://cdn.jsdelivr.net/npm/exif-js')
                    

    html = str(a)
    with open(f'{OUTPUT}/index.html', 'w', encoding='utf-8') as index:
        index.write(html)
        
    if CONFIG.get('RSS') == True:
        prepare_rss(images)
    
    if CONFIG.get('LITE') == True:
        prepare_lite(images)

def prepare_rss(images):  # sourcery skip: extract-method
    a = Airium()
    
    print('Creating RSS...')
    
    a('<?xml version="1.0" encoding="UTF-8" ?>')
    with a.rss('xmlns:atom="http://www.w3.org/2005/Atom"', version="2.0"):
        with a.channel():
            with a.title():
                a(CONFIG["OPENGRAPH"].get("WEBSITE_TITLE"))
            with a.description():
                a(CONFIG["OPENGRAPH"].get("WEBSITE_DESCRIPTION"))
            a(f'<link>{CONFIG["OPENGRAPH"].get("WEBSITE_URL")}</link>')
            a(f'<atom:link href=\"{CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/feed.xml\" rel="self" type="application/rss+xml" />')
                
            for i in range(10):
                with a.item():
                    with a.title():
                        a(f"New Photo: {images[i]}")
                    with a.description():
                        a(f'<![CDATA[<img src=\"{CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/media/large/{images[i]}\" alt="{images[i]}"> <br> \
<a href=\"{CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/media/original/{images[i]}\">ORIGINAL IMAGE</a><span> | </span><a href=\"{CONFIG["WEB"].get("SOCIAL_URL")}\">SOCIAL</a>]]>')
                    a(f'<guid>{CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/media/original/{images[i]}</guid>')
                    a(f'<link>{CONFIG["OPENGRAPH"].get("WEBSITE_URL")}/media/original/{images[i]}</link>')

    xml = str(a)
    with open(f'{OUTPUT}/feed.xml', 'w', encoding='utf-8') as index:
        index.write(xml)


def image_add_lite(a, image, orint):
        json_file = os.path.splitext(image)[0] + '.json'
        with open(f'{OUTPUT}/lite/{json_file}') as file:
            sizes = json.load(file)

        if orint == "horizontal":
            with a.div(style="width: 256px; margin-left: 4px"):
                a.img(src=f"{os.path.splitext(image)[0]}{sizes[0][0]}x{sizes[0][1]}{os.path.splitext(image)[1]}", alt=image, style="width: 256px;")
                for size in sizes:
                    with a.a('download', href=f'{os.path.splitext(image)[0]}{size[0]}x{size[1]}{os.path.splitext(image)[1]}'):
                        a(f"download {size[0]}x{size[1]}")
        if orint == "vertical":
            with a.div(style="width: 128px; margin-left: 4px"):
                a.img(src=f"{os.path.splitext(image)[0]}{sizes[0][0]}x{sizes[0][1]}{os.path.splitext(image)[1]}", alt=image, style="width: 128px;")
                for size in sizes:
                    with a.a('download', href=f'{os.path.splitext(image)[0]}{size[0]}x{size[1]}{os.path.splitext(image)[1]}'):
                        a(f"download {size[0]}x{size[1]}")
        if orint == "square":
            with a.div(style="width: 256px; height: 256px; margin-left: 4px"):
                a.img(src=f"{os.path.splitext(image)[0]}{sizes[0][0]}x{sizes[0][1]}{os.path.splitext(image)[1]}", alt=image, style="width: 256px; height: 256px")
                for size in sizes:
                    with a.a('download', href=f'{os.path.splitext(image)[0]}{size[0]}x{size[1]}{os.path.splitext(image)[1]}'):
                        a(f"download {size[0]}x{size[1]}")

def prepare_lite(images):  # sourcery skip: extract-method
    a = Airium()
    
    print('Creating lite website...')
    a('<!DOCTYPE html>')
    with a.html(lang="en"):
        with a.head():
            a.meta(charset="utf-8")
            a.meta(name="viewport", content="width=device-width")

        with a.body():
            with a.div():
                with a.div():
                    with a.h1():
                        a(CONFIG['OPENGRAPH'].get('WEBSITE_TITLE'))
                with a.a(href="/"):
                    a("<-Back--")
                        
            with a.images(style="display:flex;flex-wrap:wrap;width: 100%;height: 100%;"):
                for image in images:
                    if image == 'gitkeep':
                        continue
                    
                    with Image.open(f'{OUTPUT}/media/large/{image}') as im:
                        if im.width > im.height:
                            image_add_lite(a, image, 'horizontal')
                        elif im.width == im.height :
                            image_add_lite(a, image, 'square')
                        else:
                            image_add_lite(a, image, 'vertical')

    html = str(a)
    with open(f'{OUTPUT}/lite/index.html', 'w', encoding='utf-8') as index:
        index.write(html)        

if __name__ == "__main__":
    prepare_images()