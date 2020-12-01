<?php
//连接服务器
require_once('connect_database.php');
$conn=connect_database();

$sql="select * from article";
$result=mysqli_query($conn, $sql);
$row=$result->fetch_all(MYSQLI_BOTH);

for($i=$result->num_rows-1;$i>=0;$i--)
{
    $temp=array("title"=>$row[$i]["title"],"writer"=>$row[$i]["writer"],"intro"=>$row[$i]["intro"],"uptime"=>$row[$i]["uptime"],"row_number"=>$row[$i]["row_number"]);
    $data[]=$temp;
}

$json= json_encode($data);
echo  $json;
?>