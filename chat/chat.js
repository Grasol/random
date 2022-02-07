
var addr = document.getElementById("chat_ip").innerHTML
var user = document.getElementById("user").innerHTML;
var fault_num = 0;
var chat_len = 0;


var outbox = document.getElementById("chat_outbox");
var inbox = document.getElementById("inbox");


const errorHandling = (jqXHR, textStatus, errorThrown) => {
  outbox.innerHTML += ("<span> error: " + errorThrown + "<br/></span>");
  fault_num += 1;
  if (fault_num >= 3) {
    window.clearInterval(intv);
  }
}

const sendMsg = () => {
  var data_json = JSON.stringify({
    "user": user.substring(0, user.length - 2),
    "text": inbox.value
  });


  $.ajax({
    method: "POST",
    url: "http://" + addr + "/msg",
    data: data_json,
    dataType: "json",

    statusCode: {
      200: function () {
        inbox.value = "";
      }
    }
  });
}

const reqLen = () => {
  $.ajax({
    method: "POST",
    url: "http://" + addr + "/len",

    statusCode: {
      200: function (len) {
        var new_len = parseInt(len);
        if (new_len != chat_len) {
          getChat();
          chat_len = new_len;
        }
      }
    },

    error: function (jqXHR, textStatus, errorThrown) {
      errorHandling(jqXHR, textStatus, errorThrown);
    }
  })
}


const getChat = () => {
  $.ajax({
    method: "POST",
    url: "http://" + addr + "/chat",

    success: function (chat) {
        outbox.innerHTML = chat;
    },

    error: function (jqXHR, textStatus, errorThrown) {
      errorHandling(jqXHR, textStatus, errorThrown)
    }
  });
}

var req_time = 1000;
var intv = window.setInterval(reqLen, req_time);

