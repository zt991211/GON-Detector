<?php
header("content-type:application/x-www-form-urlencoded"); 
$name=$_POST["username"];

require_once('connect_database.php');
$conn=connect_database();

$sql = "select * from userinfo WHERE BINARY username='$name'";
$result = $conn->query($sql);
$row = $result->fetch_assoc();

if($row["userphoto"]=='')
{
    $path="php/userdata/default_headpic.jpeg";
}
else
{
    $path="php/userdata/".$name."/tx.".$row["userphoto"];
}
$json_array = array("mail"=>$row["mail"],"sex"=>$row["sex"],"birth"=>$row["birth"],"place"=>$row["place"],"path"=>$path); //转换成数组类型
$json= json_encode($json_array);  //将数组转换成json对象
echo  $json;
?>