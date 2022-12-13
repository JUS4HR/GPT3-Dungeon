const userMode = {
    say: "Say",
    do: "Do",
    story: "Story",
}

const nextUserMode = {
    say: "do",
    do: "story",
    story: "say",
}

const transferTemplate = {
    "modified-content-list": [
    ],
    "uid": "",
    "save": "",
    "user-mode": "",
    "user-input": "",
}

const modifiedContentTemplate = {
    "type": "",
    "id": 0,
    "content": ""
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

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

const contentUserPrefix = "⤷ "
const contentUserClass = "content-user"

var activeUserMode = "say";
var activeSave = getCookie("active-save-name");

$("#mode-button").html(userMode[activeUserMode]);

$("#btn-options").click(function () {
    window.location.href = "/?options=True";
});

$("#user-input-form").submit(function (e) {
    e.preventDefault();

    $("#submit-button").css("opacity", "0");
    $("#submit-button").prop('disabled', true);
    $("#submit-button-disabled").css("opacity", "1");

    var userInput = $("#user-input").val();
    var data = transferTemplate;
    data["uid"] = getCookie("uid");
    data["save-name"] = activeSave;
    data["user-mode"] = activeUserMode;
    data["user-input"] = userInput;
    $.ajax({
        url: '/process',
        contentType: 'application/json',
        type: 'POST',
        data: JSON.stringify(data),
        success: function (data) {
            var atBottom = isAtBottom();

            // start of content processing
            data["new-content-list"].forEach(function (content) {
                // console.log(content);
                if (content["content"] != "") {
                    if (content["type"] == "user") {
                        $("#content-list-content").append('<li id="content-' + content["id"] + '" class="' + contentUserClass + '">' + contentUserPrefix + content["content"] + '</li>');
                    }
                    else {
                        $("#content-list-content").append('<li id="content-' + content["id"] + '">' + content["content"] + '</li>');
                    }
                }
            });
            data["modified-content-list"].forEach(function (content) {
                $("#content-" + content["id"]).html(content["content"]);
            });
            // end of content processing

            $("#user-input").val("");
            $("#submit-button").css("opacity", "1");
            $("#submit-button").prop('disabled', false);
            $("#submit-button-disabled").css("opacity", "0");
            getToBottom(atBottom);
        }
    });
});

// switch between say, do, story
function switchMode() {
    activeUserMode = nextUserMode[activeUserMode];
    $("#mode-button").html(userMode[activeUserMode]);
}

// scrolling position keeper
function isAtBottom(rem = 0.5) {
    return $('#content-list').scrollTop() + 0.5 /* rem */ * 16 + $('#content-list').height() >= $('#content-list')[0].scrollHeight
}
function getToBottom(atBottom) {
    if (atBottom) $("#content-list").scrollTop($("#content-list")[0].scrollHeight);
}

function getStartingPrompt() {
    $("#submit-button").css("opacity", "0");
    $("#submit-button").prop('disabled', true);
    $("#submit-button-disabled").css("opacity", "1");
    $("#content-list-content").html("");
    $.ajax({
        url: '/start',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            "uid": getCookie("uid"),
            "save-name": activeSave,
        }),
        success: function (dataReceived) {
            // start of content processing
            dataReceived["new-content-list"].forEach(function (content) {
                if (content["content"] != "") {
                    if (content["type"] == "user") {
                        $("#content-list-content").append('<li id="content-' + content["id"] + '" class="' + contentUserClass + '">' + contentUserPrefix + content["content"] + '</li>');
                    }
                    else {
                        $("#content-list-content").append('<li id="content-' + content["id"] + '">' + content["content"] + '</li>');
                    }
                }
            });
            // end of content processing

            $("#user-input").val("");
            $("#submit-button").css("opacity", "1");
            $("#submit-button").prop('disabled', false);
            $("#submit-button-disabled").css("opacity", "0");
        }
    });
}


if (activeSave == "") {
    alert("You need to select a save file to continue.")
    window.location.href = "/?options=True";
}
else {
    getStartingPrompt();
}