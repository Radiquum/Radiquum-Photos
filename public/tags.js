const exif_info = document.getElementById("info");
exif_info.onclick = function() { 
    getExif()
}

function getExif() {
    let img = document.getElementById("modal-image");
    EXIF.getData(img, function() {
        alert(EXIF.pretty(this));
    });
}