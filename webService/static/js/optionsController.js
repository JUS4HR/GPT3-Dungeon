const urlPlay = "/?play=True"

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

$("#btn-back").click(function () {
    window.location.href = urlPlay;
});

$("#sel-save").change(function () {
    setCookie("active-save-name", $("#sel-save").val(), 365);
});

$("#btn-new-save").click(function () {
    var name = prompt("Enter save name");
    if (name != null && name != "") {
        $.ajax({
            url: "/handle-save",
            contentType: "application/json",
            type: "POST",
            data: JSON.stringify({
                "save-name": name,
                "uid": getCookie("uid"),
                "operation": "create"
            }),
            success: function (data) {
                if (data["success"] == "True") {
                    setCookie("active-save-name", name, 365);
                    $("#sel-save").append("<option value='" + name + "'>" + name + "</option>");
                    $("#sel-save").val(name);
                }
            }
        });
    }
});

$("#btn-delete-save").click(function () {
    if (window.confirm("Are you sure you want to delete this save?")) {
        if (window.confirm("Are you really sure?")) {
            var name = $("#sel-save").val();
            if (name != null && name != "") {
                $.ajax({
                    url: "/handle-save",
                    contentType: "application/json",
                    type: "POST",
                    data: JSON.stringify({
                        "save-name": name,
                        "uid": getCookie("uid"),
                        "operation": "delete"
                    }),
                    success: function (data) {
                        if (data["success"] == "True") {
                            $("#sel-save option[value='" + name + "']").remove();
                            setCookie("active-save-name", "", 365);
                            $("#sel-save").val("");
                        }
                    }
                });
            }
        }
    }
});

$("#btn-account-logout").click(function () {
    delCookie("uid");
    delCookie("active-save-name");
    delCookie("token");
    window.location.href = "/";
});


// load settings on start
$.ajax({
    url: "/get-settings",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ "uid": getCookie("uid") }),
    success: function (data) {
        console.log(data);
        if (data["save-names"].length > 0) {
            data["save-names"].forEach(function (save) {
                $("#sel-save").append(`<option value="${save}">${save}</option>`);
            });
            if (getCookie("active-save-name") != "") {
                $("#sel-save").val(getCookie("active-save-name"));
            }
        }
        if (data["engine-list"].length > 0) {
            data["engine-list"].forEach(function (engine) {
                $("#sel-generator-ai-engine").append(`<option value="${engine}">${engine}</option>`);
            });
            $("#sel-generator-ai-engine").val(data["settings"]["aiSettings"]["engine"]);
        }
        $("#int-generator-wct").val(data["settings"]["wordCountThreshold"]);
        $("#int-generator-ptkws").val(data["settings"]["promptsToKeepWhenSummarizing"]);
        $("#txt-generator-shp").val(data["settings"]["styleHintPrompt"]);
        $("#int-generator-scs").val(data["settings"]["summarizingSentenceCount"]);
        $("#int-generator-ai-temp").val(data["settings"]["aiSettings"]["temperature"]);
        $("#int-generator-ai-maxtok").val(data["settings"]["aiSettings"]["max_tokens"]);
        $("#int-generator-ai-maxtoksum").val(data["settings"]["aiSettings"]["max_tokens_summary"]);
        $("#int-generator-ai-top-p").val(data["settings"]["aiSettings"]["top_p"]);
        $("#int-generator-ai-freq-pen").val(data["settings"]["aiSettings"]["frequency_penalty"]);
        $("#int-generator-ai-pres-pen").val(data["settings"]["aiSettings"]["presence_penalty"]);
        $("#txt-account-api-key").val(data["settings"]["key"]);
    }
});

$("#btn-generator-submit").click(function (e) {
    e.preventDefault();
    var data = {
        "uid": getCookie("uid"),
        "wordCountThreshold": $("#int-generator-wct").val(),
        "promptsToKeepWhenSummarizing": $("#int-generator-ptkws").val(),
        "styleHintPrompt": $("#txt-generator-shp").val(),
        "summarizingSentenceCount": $("#int-generator-scs").val(),
        "aiSettings": {
            "engine": $("#sel-generator-ai-engine").val(),
            "temperature": $("#int-generator-ai-temp").val(),
            "max_tokens": $("#int-generator-ai-maxtok").val(),
            "max_tokens_summary": $("#int-generator-ai-maxtoksum").val(),
            "top_p": $("#int-generator-ai-top-p").val(),
            "frequency_penalty": $("#int-generator-ai-freq-pen").val(),
            "presence_penalty": $("#int-generator-ai-pres-pen").val()
        }
    };
    $.ajax({
        url: "/handle-options",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (data) {
            // TODO: show success message
        }
    });
});

$("#btn-account-submit").click(function (e) {
    e.preventDefault();
    var data = {
        "uid": getCookie("uid"),
        "key": $("#txt-account-api-key").val()
    };
    $.ajax({
        url: "/handle-options",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (data) {
            // TODO: show success message
        }
    });
});
