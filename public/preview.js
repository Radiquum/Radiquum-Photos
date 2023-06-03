const img = document.querySelectorAll('.img')
const modal = document.getElementById('modal');
const modal_image = document.getElementById('modal-image');
const modal_background = document.getElementById('modal-background');

const nav_close = document.getElementById("close");
const modal_close = document.getElementById("modal-background");
nav_close.onclick = function() { 
        close()
    }
modal_close.onclick = function() { 
        close()
    }

function close() {
    modal_image.classList.remove('opacity');
        setTimeout(function() {
            modal_background.classList.remove('opacity');}, 300);
            setTimeout(function() {
                modal.classList.remove('flex');
                modal.classList.remove('opacity')
           }, 600);
}

img.forEach((item) => {
    let image = item.getAttribute("large");
    item.addEventListener('click', () => {
        modal.classList.add('flex');

        setTimeout(function() {
                modal.classList.add('opacity')
                modal_image.classList.add('opacity')
                modal_background.classList.add('opacity')    
           }, 10);

        document.getElementById('modal-image').src = image;
        document.getElementById('download').href = "media/original" + image.split('large')[1];
        globalThis.url = document.getElementById('modal-image').src.split('large')[0] + "original" + image.split('large')[1]
    });
});

const copy = document.getElementById("copy");
copy.onclick = function() { 
    navigator.clipboard.writeText(url);
    }

