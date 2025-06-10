<?php
    session_start();
    include('server.php');
?>
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="about.css">
<script src="https://kit.fontawesome.com/332a215f17.js" crossorigin="anonymous"></script>
<link href="https://fonts.googleapis.com/css?family=Baloo+Chettan+2:400,700&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/remixicon@2.5.0/fonts/remixicon.css" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/boxicons@latest/css/boxicons.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.3.0/css/all.min.css"
        integrity="sha512-SzlrxWUlpfuzQ+pcUCosxcglQRNAq/DZjVsC0lE40xsADsfeQoEypE+enwcOiGjk/bSuGGKHEyjSoQ1zVisanQ=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
        <!-- <link rel="stylesheet" href="../css/bootstrap.min.css"> -->
</head>
<style>
  img {
  border-radius: 50%;
}
footer{
     background-color: #292b2c;
    color: goldenrod;
  
}
.footer_p
{
      padding: 16px 0;
    margin: 0
}
</style>
<body>

<header>
<div class="logo"><i class="ri-leaf-fill"></i><a onclick="history.back()">Cast-Climate</a></div></center></a>
</header>

<div class="about-section">
  <h1>Our passionate</h1>
  <p>The benefits of crop recommendation and selling system are manifold. 
    Farmers can make informed decisions about their crop selection and cultivation practices, leading to higher yields and profits. 
    The system also provides real-time information about market trends and demands, enabling farmers to make strategic 
    decisions about when and where to sell their produce.</p>
    <p>In addition, the crop recommendation and selling system also assists farmers in marketing their crops by connecting them to 
        potential buyers through an online platform.<br>
        This allows farmers to sell their produce at fair prices, eliminating the need for intermediaries and reducing the risk of price exploitation.</p>
  
</div>
<div class="below-section">
<h1 class="us" style="text-align:center">Our Team</h1>
<div class="row">
  <div class="column">
    <div class="card">
      <img src="../pic/karthik.jpg" alt="karthik pohane" style="width: 350px;
  height: 400px;">
      <div class="container">
        <h2 style="text-align:center">KARTHIK POHANE</h2>
        <p class="title" style="text-align:center">CEO & Founder</p>
        
      </div>
    </div>
  </div>

  <div class="column">
    <div class="card">
    <img src="../pic/koonut.jpg" alt="koonut thongchang" style="width: 350px;
  height: 400px;">
      <div class="container">
        <h2 style="text-align:center">KOONUT THONGCHANG</h2>
        <p class="title" style="text-align:center">CEO & Founder</p>
      </div>
    </div>
  </div>
  
  <div class="column">
    <div class="card">
    <img src="../pic/siddharth.jpg" alt="siddharth raj" style="width: 350px;
  height: 400px;">
      <div class="container">
        <h2 style="text-align:center">SIDDHARTH RAJ</h2>
        <p class="title" style="text-align:center">CEO & Founder</p>
      </div>
    </div>
  </div>
</div>
</div>

</body>
<hr>
<footer >
                              <div class="u-clearfix u-sheet u-sheet-1">
                              <center>
               <p class="footer_p"> Copyright 2022-2023 by Refsnes Data. All Rights Reserved. <br>Clast-climate
               </p>
      </div>
                              </center></footer>
</html>