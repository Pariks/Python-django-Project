
var chat = angular.module('chat', ['ngtimeago']);

chat.controller('ChatController', function($scope, $filter, $http, $rootScope, $timeout) {
        $scope.messages = [];
        $scope.users = [];
        $scope.csrfToken = csrfToken;
        $scope.message = "";
        $scope.username = username;
        $scope.newMessage = 0;
        
        var soundOn = 'True';
        
        if (userAuthenticated == 'False'){
            $scope.userAuthenticated = false;
        } else {
            $scope.userAuthenticated = true;
        }
        
        if(soundOn == 'True'){
            $scope.soundOn = true;
        } else {
            $scope.soundOn = false;
        }
        
        $scope.showHideChatWidget = function(){
            $scope.showChatWidget = !$scope.showChatWidget;
            
            if($scope.showChatWidget){
                $timeout(function(){
                     $("#messages-container").animate({ scrollTop: $("#messages-container")[0].scrollHeight}, 100);
                }, 1);
            }
            
            $scope.newMessage = 0;
        }
        
        var offset = new Date().getTimezoneOffset();
        
        $scope.getTimestamp = function(timestamp){
            var date = new Date(timestamp);
            date = new Date(date.getTime() + offset * 60 * 1000);
            return $filter('timeago')(date);
        }
        
        
        $scope.submitMessage = function(){
            
            var message = {};
            message.type = "message";
            message.body = $scope.message;
            message.csrfmiddlewaretoken = $scope.csrfToken;
            
            if ($scope.message == "") {
                return;
            }
            updater.socket.send(JSON.stringify(message));
            
            //Clear message
            $scope.message = "";
            
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
            
        };
        
        $scope.toggleSound = function(){
            $scope.soundOn = !$scope.soundOn;
            /*
            $.ajax({
                  method: "POST",
                  url: "/chat/sound/",
                  data: {csrfmiddlewaretoken: $scope.csrfToken }
                })
              .done(function( msg ) {
                  
              });
              */
        }
        
        
        var url = "ws://" + window.location.hostname +  ":3000/chatsocket";
        var audioElement = document.createElement('audio');
        audioElement.setAttribute('src', '/static/sounds/sound.mp3');
        
        var updater = {
            socket: null,
        
            start: function() {
                
                updater.socket = new WebSocket(url);
                
                updater.socket.onopen = function() {
                        console.log("connected");
                        if($scope.userAuthenticated){
                            var json = {};
                            json.type = "auth";
                            json.user = user;
                            updater.socket.send(JSON.stringify(json));
                        }
                    };
                    
                updater.socket.onclose = function() {
                    //Hide widget if websocket is closed
                    
                    var json = {};
                    json.type = "remove suer";
                    json.user = user;
                    updater.socket.send(JSON.stringify(json));
                    $('#chat-button').hide();
                };
                
                updater.socket.onmessage = function(event) {
                    data = JSON.parse(event.data);
                    switch(data.type){
                        case 'auth':
                            updater.showMessage(data);
                            break;
                        case 'message':
                            updater.showMessage(data);
                            if(data.messages[0].username != $scope.username && $scope.soundOn){
                                audioElement.play();
                            }
                            break;
                        case 'users':
                            updater.updateUsers(data);
                            break;
                    }
                };
            },
            
            showMessage : function(data) {
                if (data.messages.length === 0){
                    return;
                }
                
                //Check if any messages already in  message window
                var existing = $filter('filter')($scope.messages, {id: data.messages[0].id})
                if (existing.length > 0){
                    return;
                }
                
                //Add messages to window
                for(var i=0 ;i<data.messages.length; i++){
                    $scope.messages.push(data.messages[i]);
                }
                
                if(data.type === 'message'){
                    if(!$scope.showChatWidget){
                        $scope.newMessage++;
                        console.log($scope.newMessage);
                    }
                }



                $rootScope.$apply(function() {
                });
                
                $("#messages-container").animate({ scrollTop: $("#messages-container")[0].scrollHeight}, 1000);
            },
            
            updateUsers : function(data){
                $scope.users = data.users;
                $rootScope.$apply(function() {
                });
                
            }
        };
        
        
    updater.start();

});

