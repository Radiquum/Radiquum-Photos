const img = document.querySelectorAll('.img')
const modal = document.getElementById('modal');

const close = document.getElementById("close");
close.onclick = function() { 
      modal.style.display = "none";
    }

img.forEach((item) => {
    let image = item.getAttribute("large");
    item.addEventListener('click', () => {
        console.log("clicked")
        modal.style.display = 'flex'
        document.getElementById('modal-image').src = image;
        document.getElementById('download').href = "media/original" + image.split('large')[1];
        globalThis.url = document.getElementById('modal-image').src.split('large')[0] + "original" + image.split('large')[1]

        // document.getElementById('modal-background').src = image;
    });
});

const copy = document.getElementById("copy");
copy.onclick = function() { 
    navigator.clipboard.writeText(url);
    }

