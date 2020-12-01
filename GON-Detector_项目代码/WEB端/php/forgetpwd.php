<?php 
require_once('connect_database.php');
$name=$_POST["name"];
$mailbox=$_POST["mailbox"];

$conn=connect_database();

$sql = "select * from userinfo WHERE BINARY username='$name'";
$result=mysqli_query($conn, $sql);
if($result==FALSE)
{
    $state="namewrong";
    $message=NULL;
}
else
{
$row=$result->fetch_array();
if($row["mail"]==$mailbox)
{
    $state="right";
    $message=$row["password"];
}
else
{
    $state="mailwrong";
    $message=NULL;
}
}

$json_array = array("state"=>$state,"message"=>$message); //转换成数组类型
$json= json_encode($json_array);  //将数组转换成json对象
echo  $json;
?>