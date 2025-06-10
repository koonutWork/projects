<?php 
    session_start();
    include('server.php');

    if (isset($_POST['login_user'])) {
        $username = mysqli_real_escape_string($conn, $_POST['username']);
        $password = mysqli_real_escape_string($conn, $_POST['password']);        
        // $password = md5($password);
        $query = "SELECT * FROM user WHERE email = '$username' AND password = '$password' ";
        $result = mysqli_query($conn, $query);
        $row = mysqli_fetch_assoc($result);
        if (mysqli_num_rows($result) == 1) {
            $_SESSION['email'] = $username;                
            $_SESSION['id'] = $row['user_id'];
            header("location: ../home/home.php");
        } else {
            $_SESSION['error'] = "Incorrect username or password";
            header("location: login.php");
        }  
    }
?>