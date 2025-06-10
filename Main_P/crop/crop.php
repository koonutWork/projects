<?php 
    session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <title>crop</title>

    <style>
        <?php include "main-style.css" ?>
        body{
                     animation: fadeEffect 1s;
              }
              @keyframes fadeEffect {
                     from {opacity: 0;}
                     to {opacity: 1;}
              }
              
    </style>
    <link rel="stylesheet" href="crop.css">
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
<div class="logo"><i class="ri-leaf-fill"></i><a href="../home/home.php">Cast-Climate</a></div></a>
</header>
<center>
    <fieldset>
    <legend><h1>Enter Location Details</h1></legend>
    <form action="crop_db.php" method="POST" enctype="multipart/form-data" class="form-body">  
        
 
    <label for="state">State:</label>
    <select id="state" name="state">
        <option value="none">select</option>
        <option value="karnataka">Karnataka</option>
        <option value="andhra pradesh">Andhra pradesh</option>
        <option value="maharastra">Maharastra</option>
    </select>
   
    <label for="district">District:</label>
    <select id="district" name="district">
        <option value="none">select</option>
        <option value="bangalore">Bangalore</option>
        <option value="visakhapatnam">Visakhapatnam</option>
        <option value="mumbai">Mumbai</option>
    </select>

    <label for="month">Month:</label>
    <select id="month" name="month">
        <option value="none">select</option>
        <option value="Jan">Jan</option>
        <option value="Feb">Feb</option>
        <option value="Mar">Mar</option>
        <option value="Apr">Apr</option>
        <option value="May">May</option>
        <option value="Jun">Jun</option>
        <option value="Jul">Jul</option>
        <option value="Aug">Aug</option>
        <option value="Sep">Sep</option>
        <option value="Oct">Oct</option>
        <option value="Nov">Nov</option>
        <option value="Dec">Dec</option>
    </select>
    
    <label for="soil">Soil :</label>
    <select id="soil" name="soil">
        <option value="none">select</option>
        <option value="red loamy soil">red loamy soil</option>
        <option value="lateritic soil">lateritic soil</option>
        <option value="alluvial soil">alluvial soil</option>
        <option value="black cotton soil">black cotton soil</option>
        <option value="forest soil">forest soil</option>
    </select>
    
        <div>
            <br>
            <input type="submit" name="Submit" value="Submit" class="btn fa-input" >            
        </div>
    
    <?php if (isset($_SESSION['error'])) : ?>
					<div class="error">
						<h1 class="print"><?php 
							echo $_SESSION['error'];
							unset($_SESSION['error']);
						?></h4>
					</div>
				<?php endif ?>
    <?php if (isset($_SESSION['success'])) : ?>
					<div class="success">
						<h1 class="print"><?php 
							echo "The Suggestion crop : ", $_SESSION['success'];
							unset($_SESSION['success']);
						?></h4>
					</div>
				<?php endif ?> 
                </form>
            </center>
    </fieldset>

</body>

</html>