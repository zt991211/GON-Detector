<?php
require_once('connect_database.php');
$conn=connect_database();

$sql="SELECT * FROM article ORDER BY comment_num DESC";
$result=mysqli_query($conn, $sql);
$row=$result->fetch_all();
//返回指定条目的特定字符串个数
//echo $row;

for($i=0;$i<3;$i++)
{
    if($row[$i][3]=='')
    {
        $path="php/userdata/default_picture.jpg";
    }
    else{
        $path="php/userdata/".$row[$i][1]."/article/".$row[$i][7].'.'.$row[$i][3]; 
    }

    $temp=array("title"=>$row[$i][0],"uptime"=>$row[$i][4],"writer"=>$row[$i][1],"path"=>$path,"num"=>$row[$i][7]);
    $arr[]=$temp;
}

$json= json_encode($arr);  //将数组转换成json对象
echo  $json;
?>