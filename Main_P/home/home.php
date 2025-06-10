<?php
    session_start();
    if (isset($_GET['logout'])) {
        session_destroy();
        unset($_SESSION['username']);
        header('location: home.php');
    }
    include('server.php');
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
        <li><a href="../crop/crop.php">Crop suggestion</a></li>
        <li><a href="../../agrocraft/index.html">Buy/Sale</a></li>
        <li><a href="../about_us/about.php">About Us</a></li>
      </ul>
      <a href="../index.php" class="action_btn">Logout
        
      </a>
      <div class="toggle_btn"><i class="fa-solid fa-bars"></i></div>
    </div>

    <div class="dropdown_menu">
      <li><a href="#">Home</a></li>
      <li><a href="../crop/crop.php">Crop suggestion</a></li>
      <li><a href="../agrocraft/index.html">Buy/Sale</a></li>
      <li><a href="../about_us/about.php">About Us</a></li>
      <a href="../index.php" class="action_btn">Logout</a>
    </div>
  </header>

  <main>
    <section id="hero">
      <h1>Cast-Climate</h1>
      <p>This Climate Prediction and Crop Suggestion System can have a significant impact on agriculture and
        related industries. Accurate weather forecasting is crucial for farmers to make informed decisions about
        planting, harvesting, and managing their crops. With this system, farmers can receive localized weather
        predictions, facilitating their farming activities more efficiently and reduce the risk of crop failure
        due to unexpected weather changes.</p>
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