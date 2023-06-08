const copy_over = document.querySelectorAll('#copy-overlay')
copy_over.forEach((item) => {
    let url = website_url + item.getAttribute("url");
    item.addEventListener('click', () => {
        copy_link(url)
        
    });
});

const share = document.getElementById("share");
share.onclick = function() { 
    let url = website_url
    copy_link(url)

};

const copy_popup = document.getElementById('copy-popup');

function close_popup() {
    copy_popup.classList.remove('opacity')    
    setTimeout(function() {
        copy_popup.classList.remove('flex');}, 310);
};

function open_popup() {
    copy_popup.classList.add('flex');
    setTimeout(function() {copy_popup.classList.add('opacity');}, 10);
}

function copy_link(url) {
        navigator.clipboard.writeText(url);
        open_popup()
        setTimeout(close_popup, 1000)
}
