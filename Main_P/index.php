<?php
if (isset($_GET['logout'])) {
        session_destroy();
        unset($_SESSION['username']);
        header('location: index.php');
    }
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="index_style.css">
    <link href="https://cdn.jsdelivr.net/npm/remixicon@2.5.0/fonts/remixicon.css" rel="stylesheet">
    <link rel="stylesheet" href="https://unpkg.com/boxicons@latest/css/boxicons.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.3.0/css/all.min.css"
        integrity="sha512-SzlrxWUlpfuzQ+pcUCosxcglQRNAq/DZjVsC0lE40xsADsfeQoEypE+enwcOiGjk/bSuGGKHEyjSoQ1zVisanQ=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap');
        
    </style>
</head>

<body>
    <header>
        <div class="navbar">
            <div class="logo"><i class="ri-leaf-fill"></i><a href="#">Cast-Climate</a></div>
            <ul class="links">
                <li><a href="#" class="active">Home</a></li>
                <li><a href="./about_us/about.php">About Us</a></li>
                <li><a href="./services/services.php">Services</a></li>
            </ul>
            <a href="./Login/login.php" class="action_btn">SignIn/SignUp</a>
            <div class="toggle_btn"><i class="fa-solid fa-bars"></i></div>
        </div>

        <div class="dropdown_menu">
            <li><a href="#" class="active">Home</a></li>
            <li><a href="./about_us/about.php">About Us</a></li>
            <li><a href="./services/services.php">Services</a></li>
            <a href="./Login/login.php" class="action_btn">SignIn/SignUp</a>
        </div>
    </header>

    <main>
        <section id="hero">
            <h1>Predict • Protect • Provide</h1>
            <p style="font-size: 20px;"> With this system, farmers can receive localized weather predictions, facilitating their farming activities more efficiently and reduce the risk of crop failure
                due to unexpected weather changes.</p>

                <!-- <button class="hero-btn">Click here to learn more</button> -->
        </section>
    </main>

    <script>
        const toggleBtn = document.querySelector('.toggle_btn')
        const toggleBtnIcon = document.querySelector('.toggle_btn i')
        const dropDownMenu = document.querySelector('.dropdown_menu')

        toggleBtn.onclick = function () {
            dropDownMenu.classList.toggle('open')
            const isOpen = dropDownMenu.classList.contains('open')

            toggleBtnIcon.classList = isOpen
                ? 'fa-solid fa-xmark'
                : 'fa-solid fa-bars'
        }
    </script>
    </section>

</body>

</html>