<?php
$name=$_POST["name"];
$num=$_POST["num"];

require_once('connect_database.php');
$conn=connect_database();

$sql ="select * from article where row_number='$num'";
$result=mysqli_query($conn, $sql);
$row=$result->fetch_array();

if($row["picture"]=='')
{
    $path="php/userdata/default_picture.jpg";
}
else{
    //$pathdata=pathinfo($row["picture"]);
    //$exten_name=$pathdata['extension'];
    $path="php/userdata/".$row["writer"]."/article/".$row["row_number"].'.'.$row["picture"];
}

$str = file_get_contents("userdata/".$name."/article/".$num.".md");

$json_array = array("message"=>$str,"path"=>$path); 
$json= json_encode($json_array);  
echo  $json;
?> 