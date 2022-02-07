<!DOCTYPE html>
<html>

<?php header('Access-Control-Allow-Origin: *'); ?>

<head>
  <link rel="stylesheet" href="index.css">
  <meta charset="utf-8">
  <title>Chat</title>

</head>

<body>
  <?php
    $ip = $_POST["ip"];
    $port = $_POST["port"];
    $login = $_POST["login"]
  
  ?>

  <div id="main_text">
    <h1>Simple Chat</h1>
  </div>

  <div id="name_ip">
    <p>Chat: <span id="chat_ip"><?php echo $ip, ':', $port;?></span></p>
  </div>

  <div id="chat_box">
    <div id="chat_outbox"> *cisza* </div>
  </div>

  <div id="chat_inbox">
    <span id="user"><?php echo $login ?>: </span>
    <input type="text" id="inbox">
    <button id="send" onclick="sendMsg()">wyślij</button>
  </div>
  



</body>

<script src="chat.js"></script>

<script src="//code.jquery.com/jquery-1.11.3.min.js"></script>

</html>