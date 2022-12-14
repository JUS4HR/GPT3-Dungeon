// on innerHeight change, change html height to that value.
function updatePageHeight() {
    $('html').css('height', window.innerHeight);
}

const resize_ob3 = new ResizeObserver(updatePageHeight);
resize_ob3.observe(document.querySelector('html'));
