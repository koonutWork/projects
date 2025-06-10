<?php 
    session_start();
    include('server.php');

    if (isset($_POST['Submit'])) {
        $state=mysqli_real_escape_string($conn, $_POST['state']);
        $district=mysqli_real_escape_string($conn, $_POST['district']);
        $month=mysqli_real_escape_string($conn, $_POST['month']);
        $t_soil=mysqli_real_escape_string($conn, $_POST['soil']);
        $query="SELECT crops From crop where state='$state'AND district='$district' AND month='$month' AND t_soil='$t_soil' ";
        $result = mysqli_query($conn, $query);
        $row = mysqli_fetch_assoc($result);
        if(mysqli_num_rows($result)==1)
        { 
          $newresult = implode($row);
            $_SESSION['success'] =  $newresult;
            header('location: crop.php');
        //echo "The Suggestion crop : ", $newresult;  
        }
        else
        {
            $_SESSION['error'] ="Invalid Inputs";
            header('location: crop.php');
            
        }
          
    }
?>