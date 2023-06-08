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

const close = function() {
    modal_image.classList.remove('opacity');
    modal_nav.classList.remove('opacity')    
    setTimeout(function() {
        modal_background.classList.remove('opacity');}, 300);
        setTimeout(function() {
            modal.classList.remove('flex');
            modal.classList.remove('opacity')
            modal_image.src = ''
            modal_image.style = ''
        }, 600);
};

const open = function(image) {

        modal.classList.add('flex');
        setTimeout(function() {
            modal.classList.add('opacity')
            modal_image.classList.add('opacity')
            modal_nav.classList.add('opacity')    
            modal_background.classList.add('opacity')    
        }, 10);
        
        modal_image.src = website_url + "media/large/" + image;
        document.getElementById('download').href = website_url + "media/original/" + image;
        const copy = document.getElementById("copy");
        copy.onclick = function() { 
            copy_link(website_url + "media/original/" + image)
       };
};

img.forEach((item) => {
    let image = item.getAttribute("alt");

    item.addEventListener("keydown", function(event){ 
        if (event.code === "Enter") {
            open(image);
        }
        
        if (event.code === "Escape") {
            close();
        }
       }
    );

    item.addEventListener("click", function() { open(image) })

    }
);
