<?php
require_once('connect_database.php');
$conn=connect_database();

$sql="select * from article";
$result=mysqli_query($conn, $sql);
$row=$result->fetch_all(MYSQLI_BOTH);
for($i=0;$i<$result->num_rows;$i++)
{
    if($row[$i]["picture"]=='')
    {
        $data[]="php/userdata/default_picture.jpg";
        continue;
    }
    $path="php/userdata/".$row[$i]["writer"]."/article/".$row[$i]["row_number"].'.'.$row[$i]["picture"];   
    $data[]=$path;
}

$json= json_encode($data); 
echo $json;
?>