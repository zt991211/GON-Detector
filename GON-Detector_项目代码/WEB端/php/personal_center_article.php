<?php
$username=$_POST["username"];

//连接服务器
require_once('connect_database.php');
$conn=connect_database();

$sql ="select article from userinfo where username='$username'";
$result=mysqli_query($conn, $sql);
$row=$result->fetch_array();
$arr=explode(",",$row["article"],-1);

for($i=0;$i<count($arr);$i++)
{
    $sql ="select * from article where row_number='$arr[$i]'";
    $result=mysqli_query($conn, $sql);
    $row=$result->fetch_array();

    if($row["picture"]=='')
    {
        $picpath="php/userdata/default_picture.jpg";
    }
    else
    {
        //$pathdata=pathinfo($row["picture"]);
        //$exten_name=$pathdata['extension'];
        $picpath="php/userdata/".$row["writer"]."/article/".$row["row_number"].'.'.$row["picture"];   
    }

    $articleid=200000000+$row["row_number"];
    $temp=array("title"=>$row["title"],"uptime"=>$row["uptime"],"comment_num"=>$row["comment_num"],"path"=>$picpath,"articleid"=>$articleid);
    $json_array[]=$temp;
}

$json= json_encode($json_array);  //将数组转换成json对象
echo  $json;
?> 