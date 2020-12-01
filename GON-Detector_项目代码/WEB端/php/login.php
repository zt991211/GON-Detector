<?php
header("content-type:application/x-www-form-urlencoded"); 
require_once('connect_database.php');
$conn=connect_database();

$name=$_POST["name"];
$passwd=$_POST["passwd"];

$sql = "select * from userinfo WHERE BINARY username='$name'";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    if($row["password"]==$passwd)
    {
        $message='success';
    }
    else
    {
        $message='wrong_pwd';
    }
}
else{
    $message='wrong_username';
}


$json_array = array("message"=>$message); //转换成数组类型
$json= json_encode($json_array);  //将数组转换成json对象
echo  $json;
?>