<?php
$num=$_POST["num"];

//连接服务器
require_once('connect_database.php');
$conn=connect_database();

$sql ="select comment from article where row_number='$num'";
$result=mysqli_query($conn, $sql);
$row=$result->fetch_array();
$arr=explode(",",$row["comment"],-1);

for($i=0;$i<count($arr);$i++)
{
    $sql ="select * from comment where row_number='$arr[$i]'";
    $result=mysqli_query($conn, $sql);
    $row=$result->fetch_array();

    $username=$row["commenter"];
    $sql="select * from userinfo where username='$username'";
    $rresult=mysqli_query($conn, $sql);
    $rrow=$rresult->fetch_array();

    $picpath="php/userdata/".$username."/tx.".$rrow["userphoto"];

    $temp=array("commenter"=>$row["commenter"],"comment"=>$row["comment"],"uptime"=>$row["uptime"],"pic"=>$picpath);
    $json_array[]=$temp;
}

//$json_array = array("message"=>$str); //转换成数组类型
$json= json_encode($json_array);  //将数组转换成json对象
echo  $json;
?> 