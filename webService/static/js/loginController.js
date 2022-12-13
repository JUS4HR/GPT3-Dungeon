function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}

function getIn(uid, token)
{
    setCookie("login-uid", uid, 7);
    setCookie("login-token", token, 7);
    window.location.href = "/?play=True&uid=" + uid + "&token=" + token;
}

function checkToken() {
    var uid = getCookie("login-uid");
    var token = getCookie("login-token");
    if (token != "") {
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
                    getIn(uid, token);
                }
                else {
                    $.cookie("uid", null, { path: '/' });
                    $.cookie("token", null, { path: '/' });
                }
            }
        });
    }
}

// on load:
checkToken()

// on login:
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
            if (data["success"] == "True") {
                getIn(data["uid"], data["token"]);
            }
            else {
                $("#login-password").attr("class", "login-failed-input");
            }
        }
    });
});