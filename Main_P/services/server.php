<?php 

    $servername = "localhost:3310";
    $username = "root";
    $password = "";
    $dbname = "cast_climate";

    // Create Connection
    $conn = mysqli_connect($servername, $username, $password, $dbname);

    // Check connection
    if (!$conn) {
        die("Connection failed" . mysqli_connect_error());
    } 
?>