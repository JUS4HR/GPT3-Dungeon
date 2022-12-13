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

function solidfyTokenCookie(uid, token) {
    setCookie("uid", uid, 7);
    setCookie("token", token, 7);
}

function getIn(uid, token) {
    if (token != "" && uid != "") {
        solidfyTokenCookie(uid, token);
        window.location.href = "/?play=True";
    }
}

$("#login-form").submit(function (e) {
    e.preventDefault();
    var uname = $("#login-username").val();
    var pass = $("#login-password").val();
    $.ajax({
        url: "/auth-password",
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify({
            "uname": uname,
            "pass": pass
        }),
        success: function (data) {
            console.log(data);
            if (data["success"] == "True") {
                getIn(data["uid"], data["token"]);
            }
            else {
                $("#login-password").attr("class", "login-failed-input");
            }
        }
    });
});


var uid = getCookie("uid");
var token = getCookie("token");
getIn(uid, token);