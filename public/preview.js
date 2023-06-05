const img = document.querySelectorAll('.clickable')
const modal = document.getElementById('modal');
const modal_image = document.getElementById('modal-image');
const modal_background = document.getElementById('modal-background');
const website_url = window.location.origin + window.location.pathname.split('index.html')[0]

const modal_nav = document.getElementById("modal-navigation");
const nav_close = document.getElementById("close");
const modal_close = document.getElementById("modal-background");
nav_close.onclick = function() { 
    close()
};
modal_close.onclick = function() { 
    close()
};

function close() {
    modal_image.classList.remove('opacity');
    modal_nav.classList.remove('opacity')    
    setTimeout(function() {
        modal_background.classList.remove('opacity');}, 300);
        setTimeout(function() {
            modal.classList.remove('flex');
            modal.classList.remove('opacity')
        }, 600);
};

img.forEach((item) => {
    let image = item.getAttribute("alt");

    item.addEventListener('click', function () {
        modal.classList.add('flex');
        setTimeout(function() {
            modal.classList.add('opacity')
            modal_image.classList.add('opacity')
            modal_nav.classList.add('opacity')    
            modal_background.classList.add('opacity')    
        }, 10);
    
        document.getElementById('modal-image').src = website_url + "media/large/" + image;
        document.getElementById('download').href = website_url + "media/original/" + image;
        globalThis.url = website_url + "media/original/" + image;
    });
});

const copy = document.getElementById("copy");
copy.onclick = function() { 
    navigator.clipboard.writeText(url);
};

const copy_over = document.querySelectorAll('#copy-overlay')
copy_over.forEach((item) => {
    let url = website_url + item.getAttribute("url");
    item.addEventListener('click', () => {
        navigator.clipboard.writeText(url);
    });
});
