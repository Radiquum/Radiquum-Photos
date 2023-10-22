const img = document.querySelectorAll('.clickable')
const modal = document.getElementById('modal');
const modal_image = document.getElementById('modal-image');
const modal_image_bg = document.getElementById('modal-image-background');
const modal_background = document.getElementById('modal-background');
const website_url = window.location.origin + window.location.pathname.split('index.html')[0]

const modal_nav = document.getElementById("modal-navigation");
const modal_next = document.getElementById("next");
const modal_prev = document.getElementById("prev");
const nav_close = document.getElementById("close");
const modal_close = document.getElementById("modal-background");

const last_image = document.querySelector('images').lastElementChild.children[0]

nav_close.onclick = function() { 
    close()
};
modal_close.onclick = function() { 
    close()
};

const close = function() {
    modal_background.classList.remove("filter");
    setTimeout(function() {modal.classList.remove('opacity')}, 205);
    setTimeout(function() {
        modal.classList.remove('flex');
        modal_image_bg.classList.remove("loaded")
        modal_image.src = '';
        modal_image_bg.style = '';}, 605);
        
    };
    
const open = function(image, source) {
        modal.id = "CUR_" + image;
        if (document.querySelector('img[alt="'+modal.id.replace("CUR_", "")+'"]').getAttribute('idx') == last_image.getAttribute('idx')) { modal_next.style = "display: none;"} else {modal_next.style = "display: block;"};
        if (document.querySelector('img[alt="'+modal.id.replace("CUR_", "")+'"]').getAttribute('idx') == '0') { modal_prev.style = "display: none;"} else {modal_prev.style = "display: block;"};

        modal.classList.add('flex');
        setTimeout(function() {modal.classList.add('opacity');}, 5);
        setTimeout(function() {modal_background.classList.add("filter");}, 300);
        modal_image_bg.style = "background-image: url("+ source +")";
        modal_image.src = website_url + "media/large/" + image;
        document.getElementById('download').href = website_url + "media/original/" + image;
        const copy = document.getElementById("copy");
        copy.onclick = function() { 
            copy_link(website_url + "media/original/" + image)
        };
        
        function loaded() {
            modal_image_bg.classList.add("loaded")
        };
        
        if (modal_image.complete) {
            loaded()
        } else {
            modal_image.addEventListener("load", loaded)
        };

};

img.forEach((item) => {
    let image = item.getAttribute("alt");
    let source = item.getAttribute("src");
    item.addEventListener("keydown", function(event){ 
        if (event.code === "Enter") {
            open(image, source);
        }
        
        if (event.code === "Escape") {
            close();
        }
       }
    );

    item.addEventListener("click", function() { open(image, source) })

    }
);

document.addEventListener("keydown", function(event){ 
    if (event.code === 'ArrowLeft') {
        show_prev();
    }
    if (event.code === 'ArrowRight') {
        show_next();
    }
   }
);

modal_next.onclick = function() {
    show_next()
}
const show_next = function() {
    let current = document.querySelector('img[alt="'+modal.id.replace("CUR_", "")+'"]')
    let next_id = parseInt(current.getAttribute('idx')) + 1
    let item = document.querySelector('img[idx="'+next_id+'"]')

    let image = item.getAttribute("alt");
    let source = item.getAttribute("src");
    
    modal.id = "CUR_" + image
    if (document.querySelector('img[alt="'+modal.id.replace("CUR_", "")+'"]').getAttribute('idx') == last_image.getAttribute('idx')) { modal_next.style = "display: none;"} else {modal_next.style = "display: block;"};
    if (document.querySelector('img[alt="'+modal.id.replace("CUR_", "")+'"]').getAttribute('idx') == '0') { modal_prev.style = "display: none;"} else {modal_prev.style = "display: block;"};

    modal_image_bg.style = "background-image: url("+ source +")";
    modal_image.src = website_url + "media/large/" + image;
    document.getElementById('download').href = website_url + "media/original/" + image;
    copy.onclick = function() { 
        copy_link(website_url + "media/original/" + image)
   };

    function loaded() {
        modal_image_bg.classList.add("loaded")
    };

    if (modal_image.complete) {
        loaded()
    } else {
        modal_image.addEventListener("load", loaded)
    };

};

modal_prev.onclick = function() {
    show_prev()
}
const show_prev = function() {
    let current = document.querySelector('img[alt="'+modal.id.replace("CUR_", "")+'"]')
    let next_id = parseInt(current.getAttribute('idx')) - 1
    let item = document.querySelector('img[idx="'+next_id+'"]')

    let image = item.getAttribute("alt");
    let source = item.getAttribute("src");
    
    modal.id = "CUR_" + image
    if (document.querySelector('img[alt="'+modal.id.replace("CUR_", "")+'"]').getAttribute('idx') == last_image.getAttribute('idx')) { modal_next.style = "display: none;"} else {modal_next.style = "display: block;"};
    if (document.querySelector('img[alt="'+modal.id.replace("CUR_", "")+'"]').getAttribute('idx') == '0') { modal_prev.style = "display: none;"} else {modal_prev.style = "display: block;"};

    modal_image_bg.style = "background-image: url("+ source +")";
    modal_image.src = website_url + "media/large/" + image;
    document.getElementById('download').href = website_url + "media/original/" + image;
    copy.onclick = function() { 
        copy_link(website_url + "media/original/" + image)
   };

    function loaded() {
        modal_image_bg.classList.add("loaded")
    };

    if (modal_image.complete) {
        loaded()
    } else {
        modal_image.addEventListener("load", loaded)
    };

};

