const copy_over = document.querySelectorAll('#copy-overlay')
copy_over.forEach((item) => {
    let url = website_url + item.getAttribute("url");
    item.addEventListener('click', () => {
        copy_link(url)
        open_popup()
        setTimeout(close_popup, 1000)
    });
});

const share = document.getElementById("share");
share.onclick = function() { 
    let url = website_url
    copy_link(url)
    open_popup()
    setTimeout(close_popup, 1000)
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
    navigator.permissions.query({name: "clipboard-write"}).then((result) => {
        if (result.state === "granted" || result.state === "prompt") {
            navigator.clipboard.writeText(url);
        }
      });
}
