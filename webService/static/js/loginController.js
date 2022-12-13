function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function delCookie(cname) {
    setCookie(cname, "", -1);
}

function checkToken() {
    var uid = getCookie("uid");
    var token = getCookie("token");
    $.ajax({
        url: "/auth-token",
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify({
            "uid": uid,
            "token": token
        }),
        success: function (data) {
            if (data["success"] == "True") {
                console.log("Token is valid");
            }
            else {
                delCookie("uid");
                delCookie("token");
                window.location.href = "/";
            }
        }
    });
}

// on load:
checkToken()
