<?php
$username=$_POST["username"];

//连接服务器
require_once('connect_database.php');
$conn=connect_database();

$sql ="select * from userinfo where username='$username'";
$result=mysqli_query($conn, $sql);
$row=$result->fetch_array();
$arr=explode(",",$row["historypicture"],-1);
$userid=$row["row_number"];

for($i=0;$i<count($arr);$i++)
{
    $sql ="select * from eye_picture where row_number='$arr[$i]'";
    $result=mysqli_query($conn, $sql);
    $row=$result->fetch_array();

    $path="php/userdata/".$username."/picture/".$row["row_number"].'.'.$row["picture"];

    //$picid="100000000"+strval($row["row_number"]);
    $picid=100000000+$row["row_number"];

    $temp=array("path"=>$path,"uptime"=>$row["uptime"],"prob"=>$row["prob"],"vcdr"=>$row["vcdr"],"hcdr"=>$row["hcdr"],"picid"=>$picid);
    $json_array[]=$temp;
    
}

$json= json_encode($json_array);  //将数组转换成json对象
echo  $json;
?> 