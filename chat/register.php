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

  <?php
    require("conn.php");

    function inString($str, $pwd) {
      foreach ($pwd as $c) {
        if (strpos($str, $c)) {
          return true;
        }
      }

      return false;
    }
  
    $login = $_POST["login"];
    $pwd = $_POST["pwd"];
    $conf_pwd = $_POST["conf_pwd"];
  
    $date_fmt = "Y-m-d H:i:s";
    $reg_date = date($date_fmt);
  
    // password length check 
    $pwd_len_valid = false;
    if (strlen($pwd) >= 8) {
      $pwd_len_valid = true;
    }
    
    // special characters in password
    $special_fmt = array('!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', 
     ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', 
     '`', '{', '|', '}', '~', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9');
    $pwd_special_valid = inString($pwd, $special_fmt);

    // upper case in password
    $upper_fmt = array('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
        'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z');
    $pwd_upper_valid = inString($pwd, $upper_fmt);

    $pwd_conf_valid = (strcmp($pwd, $conf_pwd) == 0);

    if ($pwd_len_valid && ($pwd_special_valid || $pwd_upper_valid)) {
      if ($pwd_conf_valid) {
        // login check
        $query = "SELECT id FROM users WHERE login = '$login'";
        $res = $conn->query($query);
        if (($res->num_rows) == 0 && $login !== "") {
          $query = "INSERT INTO users (login, pwd, reg_date)".
                   "VALUES ('$login', '$pwd', '$reg_date')";
          $conn->query($query);

          ?>
          <div id="reg_correct">
            <form action="dashboard.php" method="post">
              <h4>Zarejestrowano</h4>
        
              <label class="lc">Nazwa użytkownika: </label>
              <input class="ic" type="text" name="login" value="<?php echo $login ?>" maxlength=64><br/><br/>
              
              <label class="lc">Hasło: </label>
              <input class="ic" type="password" name="pwd" value="<?php echo $pwd ?>" maxlength=64><br/><br/>
        
              <button type="subbmit">Zaloguj!</button>
        
            </form>
          </div>
          <?php
        }

        else {
          ?>
          <div id="invalid_login">
            <form action="index.html">
              <label class="lc">Taki użytkownik już istnieje</label><br/><br/>
              <button type="subbmit">ok</button>
            </form>
          </div>
          <?php 
        }
      }

      else {
        ?>
        <div id="invalid_conf_pwd">
          <form action="index.html">
            <label class="lc">Hasła nie są zgodne</label><br/><br/>
            <button type="subbmit">ok</button>
          </form>
        </div>
        <?php 
      }
    }

    else {
      ?>
      <div id="invalid_pwd">
        <form action="index.html">
          <label class="lc">Hasło musi mieć przynajmniej 8 znaków, w tym znak specialny oraz wielkie i małe litery</label><br/><br/>
          <button type="subbmit">ok</button>
        </form>
      </div>
      <?php      
    }
  
  ?>

</body>
</html>