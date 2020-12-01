<?php
require_once('connect_database.php');
//header("content-type:application/x-www-form-urlencoded");
//{"commenter":commenter,"comment":comment,"uptime":uptime,"articlenum":articlenum}
$commenter=$_POST["commenter"];
$comment=$_POST["comment"];
$uptime=$_POST["uptime"];
$articlenum=$_POST["articlenum"];

//连接服务器
$conn=connect_database();

//取得当前评论的数目
$sql ="select row_number from comment order by row_number DESC limit 1";
$result=mysqli_query($conn, $sql);
$row=$result->fetch_array();
if($row["row_number"]=='')$row["row_number"]=0;
$newnum=$row["row_number"]+1;

//读取原有文章
$sql="select comment from article where row_number='$articlenum'";
$result=mysqli_query($conn, $sql);
$row=$result->fetch_array();
$newcomment=$row["comment"].$newnum.",";
$sql="update article set comment='$newcomment' where row_number='$articlenum'"; 
mysqli_query($conn, $sql);
$sql="update article set comment_num=comment_num+1 where row_number='$articlenum'";
mysqli_query($conn, $sql);
//插入数据
$sql= "INSERT INTO comment (commenter,comment,uptime)
VALUES ('$commenter', '$comment', '$uptime')";
    if (mysqli_query($conn, $sql))
    {
        $message='上传成功';
    }
    else
    {
        $message='上传失败';
        echo "Error: " . $sql . "<br>" . mysqli_error($conn);
    }

 

$sql ="SET @row=0";
mysqli_query($conn, $sql);
$sql ="UPDATE comment SET row_number=(@row:=@row+1)";
mysqli_query($conn, $sql);


$json_array = array("message"=>$message); //转换成数组类型
$json= json_encode($json_array);  //将数组转换成json对象
echo  $json;
?>