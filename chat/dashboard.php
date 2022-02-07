<!DOCTYPE html>
<html>
<head>

  <meta charset="utf-8">
  <title>Chat</title>
  <link rel="stylesheet" href="index.css">

</head>

<body>
  <div id="main_text">
    <h1>Simple Chat</h1>
  </div>

  <div id="dasboard">
    <?php
      require("conn.php");

      $login = $_POST["login"];
      $pwd = $_POST["pwd"];

      $query = "SELECT * FROM users WHERE login = '$login' && pwd = '$pwd'";
      $res = $conn->query($query);

      if ($res->num_rows != 1) {
        ?>
        <div id="invalid_logon">
          <form action="index.html">
            <label class="lc">Błędny login lub hasło</label><br/><br/>
            <button type="subbmit">ok</button>
          </form>
        </div>
        <?php
      }

      else {
        ?>
        <h3>Dashboard</h3>
        <div id="user_info">
          <p>Zalogowano jako: <?php echo $login ?></p><br/>
  
          <form action="index.html">
            <button type="subbmit">wyloguj</button>
          </form>
        </div>
  
        <div id="connect">
          <form action="chat.php" method="post">
            <h4>Połącz z czatem</h4>
  
            <label class="lc">IP: </label>
            <input class="ic" type="text" name="ip"><br/><br/>
            
            <label class="lc">port: </label>
            <input class="ic" type="test" name="port"><br/><br/>
            
            <label class="lc">Nazwa użytkownika: </label>
            <input class="ic" type="test" name="login" value="<?php echo $login ?>" readonly><br/><br/>
  
            <button type="subbmit">Połącz</button>
          </form>
        </div>
        <?php
      }

    ?>
  </div>

  <!--<div id="register">
    <form action="register.php" method="post">
      <h4>Zarejestruj się</h4>

      <label class="lc">Nazwa użytkownika: </label>
      <input class="ic" type="text" name="username"><br/><br/>
      
      <label class="lc">Hasło: </label>
      <input class="ic" type="password" name="pwd"><br/><br/>
      
      <label class="lc">Potwierdź hasło: </label>
      <input class="ic" type="password" name="conf_pwd"><br/><br/>

      <button type="subbmit">Zarejestruj!</button>

    </form>
  </div> -->



</body>
</html>