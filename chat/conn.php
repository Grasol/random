
<?php
  $hostname = "localhost";
  $username = "root";
  $password = "";
  $database = "chat";

  $conn = new mysqli($hostname, $username, $password, $database);
  if (mysqli_connect_error() != 0) {
    Throw new Exception(mysqli_connect_error());
  }

?>