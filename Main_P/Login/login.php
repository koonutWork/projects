<?php
    session_start();
    include('server.php');
?>

<!DOCTYPE html>
<html>
<head>
<link rel="icon" href="../pics//petS.png">
<title>Customer_Login_Register_UI</title>
<style>
<?php include('login.css');?>
</style>
<script src="https://kit.fontawesome.com/332a215f17.js" crossorigin="anonymous"></script>
<link href="https://fonts.googleapis.com/css?family=Baloo+Chettan+2:400,700&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/remixicon@2.5.0/fonts/remixicon.css" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/boxicons@latest/css/boxicons.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.3.0/css/all.min.css"
        integrity="sha512-SzlrxWUlpfuzQ+pcUCosxcglQRNAq/DZjVsC0lE40xsADsfeQoEypE+enwcOiGjk/bSuGGKHEyjSoQ1zVisanQ=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>
<body>
<header>
<div class="logo"><i class="ri-leaf-fill"></i><a href="../index.php">Cast-Climate</a></div></center></a>
</header>

<div class="hero">

<div class="flex-container">
<div class="flex-child image">
<!-- <img style="
height:500px;margin:5% auto;"src="../pic/bg.jpg"> -->
</div>

<div class="flex-child form-box">
<h2 style="text-align: center;margin-top: 20px;color: #5f9ea0;">USER</h2>
<div class="button-box">

<div id="btn"></div>
<button type="button" class="toggle-btn hover" onclick="login()">LOGIN</button>
<button type="button" class="toggle-btn hover" onclick="register()">REGISTER</button>
</div>
<div id="social-icons">
    <a href="#"><i class="fab fa-facebook facebook"></i></a>
                 <a href="#"><i class="fab fa-twitter twitter"></i></a>
                 <a href="#"><i class="fab fa-google-plus plus"></i></a>
                </div>
<form action="login_db.php" method="post" id="login" class="input-group">
<?php if (isset($_SESSION['error'])) : ?>
<div class="error">
<h4><?php
echo $_SESSION['error'];
unset($_SESSION['error']);
?></h4>
</div>
<?php endif ?>
<?php if (isset($_SESSION['success'])) : ?>
<div class="success">
<h4><?php
echo $_SESSION['success'];
unset($_SESSION['success']);
?></h4>
</div>
<?php endif ?>  
<input type="text" name="username" class="input-field" placeholder="Email" required>
           
            <input type="password" name="password" class="input-field" placeholder="Password" required>
       
        <input type="checkbox" class="chech-box"><span>Remember Me</span>
       
        <button type="submit" class="submit-btn pulsate" name="login_user" >LOGIN</button>
        </form>

        <form action="register_db.php" method="post" id="register" class="input-group">
            <input type="text" class="input-field" placeholder="Username"name="username" required>
   
        <input type="email" class="input-field" placeholder="Email"name="email" required>
   
        <input type="password" class="input-field" placeholder="Password"name="password_1" required>
   
        <input type="password" class="input-field" placeholder="Repeat Password"name="password_2" required>
       
            <button type="submit" class="submit-btn pulsate" name="reg_user" style="margin-top: 10px;">REGISTER</button>
    </form>

        </div>
       

</div>

</div>

<footer class="footer" id="footer">

        <!-- <div class="section-center">
            <p class="text" id="text">
            <span><a href="#" class="footer_a">CONTACT US</a></span><br/>
           
                &copy; <span>Team Cast-Climate</span>
            </p>
        </div> -->

       </footer>
<script>
var x=document.getElementById("login");
var y=document.getElementById("register");
var z=document.getElementById("btn");

function register(){
x.style.left="-400px";
y.style.left="50px";
z.style.left="110px";
}
function login(){
x.style.left="50px";
y.style.left="400px";
z.style.left="0px";
}
</script>
</body>
</html>