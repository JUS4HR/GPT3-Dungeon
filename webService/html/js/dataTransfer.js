var userMode = {
    say: "Say",
    do: "Do",
    story: "Story",
}

var nextUserMode = {
    say: "do",
    do: "story",
    story: "say",
}

var activeUserMode = "say";
$("#mode-button").html(userMode[activeUserMode]);

$("#user-input-form").submit(function (e) {
    e.preventDefault();
    var userInput = $("#user-input").val();
    var json_data = JSON.stringify({
        "user-input": userInput,
        "user-mode": activeUserMode
    });
    $("#submit-button").css("opacity", "0");
    $("#submit-button").prop('disabled', true);
    $("#submit-button-disabled").css("opacity", "1");
    $.ajax({
        url: '/process',
        contentType: 'application/json',
        type: 'POST',
        data: json_data,
        success: function (data) {
            // $("div[name='target']").html(data.result);
            $("#user-input").val("");
            $("#submit-button").css("opacity", "1");
            $("#submit-button").prop('disabled', false);
            $("#submit-button-disabled").css("opacity", "0");

            var atBottom = isAtBottom();
            // start of content processing
            if (data["mode"] == "add") {
                $("#content-list-content").append('<li>' + data["new-content"] + '</li>');
            }
            // end of content processing
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