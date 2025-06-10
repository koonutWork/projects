<?php
    session_start();
    include('server.php');
?>
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="services.css">
<script src="https://kit.fontawesome.com/332a215f17.js" crossorigin="anonymous"></script>
<link href="https://fonts.googleapis.com/css?family=Baloo+Chettan+2:400,700&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/remixicon@2.5.0/fonts/remixicon.css" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/boxicons@latest/css/boxicons.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.3.0/css/all.min.css"
        integrity="sha512-SzlrxWUlpfuzQ+pcUCosxcglQRNAq/DZjVsC0lE40xsADsfeQoEypE+enwcOiGjk/bSuGGKHEyjSoQ1zVisanQ=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;1,100;1,300&display=swap');
</style>
<style>

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
  
  <hr>
    <center>
<div class="row">
  <div class="column">
    <div class="card">
    <img src="../pic/first.jpg" alt="Jane" style="width:60%">
      <div class="container">
        <h2 style="text-align:center">Crop Suggestion</h2>
        <p class="title" style="text-align:center">The system would analyze historical data on crop yields and weather patterns in the specified state and district during the given month, 
        as well as information on the soil type of the farm.Based on this information, the system would recommend crops that are best suited for the soil type and can thrive in the 
        prevailing weather conditions. For instance, if the soil is acidic and the month is June, the system may recommend crops like maize, 
        soybean, or cotton, which are known to do well in such conditions. However, it's important to note that this approach would be less 
        personalized and may not take into account specific farm-level factors that can impact crop yields.</p>
      
      </div>
    </div>
  </div>
  
  <div class="column">
    <div class="card">
    <img src="../pic/second.jpg" alt="Jane" style="width:60%">
      <div class="container">
        <h2 style="text-align:center">Buy/Sale</h2>
        <p class="title" style="text-align:center">A buy/sell crop system typically works as an online marketplace where farmers can post listings for their crops and buyers can browse and purchase them. 
        The system facilitates transactions and ensures that both parties receive their agreed-upon payment and product. 
        Farmers can create listings for their crops by providing details like crop type, quantity, quality, and price. 
        Buyers can then search for crops based on their requirements and purchase them directly from the farmers. 
        The system may also offer features like rating and review systems to help buyers make informed decisions, as well as payment and
         logistics support to ensure smooth transactions. By providing a platform for direct sales, buy/sell crop systems can help farmers get fair 
         prices for their products and increase their access to buyers, while also providing buyers with fresh and locally sourced crops.</p>
        
      </div>
    </div>
  </div>
</div>
</div>
</center>
</body>
<hr>
<footer class="u-align-center u-clearfix u-footer u-grey-80 u-footer" id="sec-0dec">
                              <div class="u-clearfix u-sheet u-sheet-1">
                              <center>
               <p class="footer_p"> Copyright 2022-2023 by Refsnes Data. All Rights Reserved. <br>Clast-climate
               </p>
      </div>
                              </center></footer>
</html>