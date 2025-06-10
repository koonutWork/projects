<?php 
    session_start();
    include('server.php');
    

    if (isset($_POST['reg_user'])) {
        $username = mysqli_real_escape_string($conn, $_POST['username']);
        $email = mysqli_real_escape_string($conn, $_POST['email']);
        $password_1 = mysqli_real_escape_string($conn, $_POST['password_1']);
        $password_2 = mysqli_real_escape_string($conn, $_POST['password_2']);

        if ($password_1 != $password_2) {            
            $_SESSION['error'] = "The two passwords do not match";
        }

        $user_check_query = "SELECT * FROM user WHERE (user_name = '$username' OR email = '$email') LIMIT 1";
        $query = mysqli_query($conn, $user_check_query);
        $result = mysqli_fetch_assoc($query);

        if ($result) { // if user exists
            if ($result['user_name'] === $username) {            
                $_SESSION['error'] = "Username already exists";
            }
            if ($result['email'] === $email) {                
                $_SESSION['error'] = "Email already exists";
            }
        }

        if (!isset($_SESSION['error'])) {
            // $password = md5($password_1);

            $sql = "INSERT INTO user (user_name, email, password) VALUES ('$username', '$email', '$password_1')";
            mysqli_query($conn, $sql);

            $_SESSION['username'] = $username;
            $_SESSION['success'] = "Account created successfully";
            header('location: login.php');
        } else {
            header("location: login.php");
        }
    }

?>