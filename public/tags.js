const exif_info = document.getElementById("info");
exif_info.onclick = function() { 
    getExif()
}

function getExif() {
    let img = document.getElementById('modal-image').src.split('large')[0] + "original" + document.getElementById('modal-image').src.split('large')[1];

    var http = new XMLHttpRequest();
    http.open("GET", img, true);
    http.responseType = "blob";
    http.onload = function(e) {
        if (this.status === 200) {
            EXIF.getData(http.response, function() {
                alert(EXIF.pretty(this));
            });
        }
    };
    http.send();
}