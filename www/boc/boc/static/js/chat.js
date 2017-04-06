
$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#message-form").on("submit", function(e) {
        e.preventDefault();
        newMessage($(this));
        
    });
    $("#message-form").on("keypress", function(e) {
        if (e.keyCode == 13) {
             e.preventDefault();
             newMessage($(this));
        }
    });
    $("#message").select();
    updater.start();
    
    
    //Open close chat window
    $("#chat-button, #chat-footer").on("click", function(){
        $("#chat-window").toggle();
        $("#messages-container").animate({ scrollTop: $("#messages-container")[0].scrollHeight}, 0);

    });
    
});

function newMessage(form) {
    var message = form.formToDict();
    message.type = "message";
    if (message.body == "") {
        return;
    }
    updater.socket.send(JSON.stringify(message));
    form.find("input[id=message]").val("").select();
    //Scroll to bottom chat
    $("#messages-container").animate({ scrollTop: $("#messages-container")[0].scrollHeight}, 1000);
    //save message to database
    $.ajax({
          method: "POST",
          url: "/chat/message/",
          data: { text: message.body, csrfmiddlewaretoken: message.csrfmiddlewaretoken }
        })
      .done(function( msg ) {
      });
}



jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

var updater = {
    socket: null,

    start: function() {
        var url = "ws://" + window.location.hostname +  ":3000/chatsocket";
        var audioElement = document.createElement('audio');
        audioElement.setAttribute('src', '/static/sounds/sound.mp3');
        
        updater.socket = new WebSocket(url);
        
        updater.socket.onopen = function() {
                console.log("connected");
                
                //send authenication to websocket
                var json = {};
                json.type = "auth";
                json.user = user;
                updater.socket.send(JSON.stringify(json));
            };
            
        updater.socket.onclose = function() {
            //Hide widget if websocket is closed
            json.type = "remove user";
            json.user = user;
            updater.socket.send(JSON.stringify(json));
            $('#chat-button').hide();
        };
        
        updater.socket.onmessage = function(event) {
            json = JSON.parse(event.data);
            switch(json.type){
                case 'auth':
                    updater.showMessage(json);
                    break;
                case 'message':
                    updater.showMessage(json);
                    audioElement.play();
                    break;
                case 'users':
                    updater.updateUsers(json.html_users);
                    break;
            }
        };
    },
    
    showMessage : function(message) {
        //check if message already in window, if so than return
        var existing = $(message.id);
        if (existing.length > 0)
            return;
            
        if (typeof message.id === "undefined" && !$("#messages-container").is(':empty'))
            return;
             
        var node = $(message.html_messages);
        node.hide();
        $("#messages-container").append(node);
        node.slideDown();
    },
    
    updateUsers : function(users){
        var node = $(users);
        $("#online-users-container").html(node);
        
    }
};

