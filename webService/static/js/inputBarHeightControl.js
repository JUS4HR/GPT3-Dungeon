// using jQuery

// padding-bottom of element named content-list is always equal to height of hud-bottom-section
function updateBottomClearance() {
    $('#content-list-end').css('height', $(document).height() - $('#hud-bottom-section').position().top);
}
updateBottomClearance();

const resize_ob1 = new ResizeObserver(updateBottomClearance);
resize_ob1.observe(document.querySelector('.hud-bottom-section'));

// pressing button to switch visibility of the menu
var menuVisible = true;
if ($('#bottom-menu').height() == 0) {
    menuVisible = false;
}
async function toggleMenu() {
    if (menuVisible) {
        $('#bottom-menu').css('max-height', '0rem');
        $('#bottom-menu').css('opacity', 0);
        $('#show-menu-button').css('transform', 'rotate(0deg)');
        menuVisible = false;
    } else {
        $('#bottom-menu').css('max-height', '10rem');
        $('#bottom-menu').css('opacity', 1);
        $('#show-menu-button').css('transform', 'rotate(180deg)');
        menuVisible = true;
    }
}

// scrolling position keeper
function stickToBottom() {
    if($('#content-list').scrollTop() + 0.5 /* rem */ * 16 + $('#content-list').height() >= $('#content-list')[0].scrollHeight) {
        $('#content-list').scrollTop($('#content-list')[0].scrollHeight);
    }
}
const resize_ob2 = new ResizeObserver(stickToBottom);
resize_ob2.observe(document.querySelector('.hud-bottom-menu'));