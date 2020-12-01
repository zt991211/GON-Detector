<?php
header("content-type:application/x-www-form-urlencoded");
//{"name":username,"passwd":password,"mail":mailbox,"sex":sex,"birth":birth,"place":place}
$name=$_POST["name"];
$passwd=$_POST["passwd"];
$mail=$_POST["mail"];
$sex=$_POST["sex"];
$birth=$_POST["birth"];
$place=$_POST["place"];

//连接服务器
require_once('connect_database.php');
$conn=connect_database();
// 检测连接
/*if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
} 
echo "连接成功";*/

$sql = "select * from userinfo WHERE BINARY username='$name'";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    $message='user_exsit';
}
else
{
    $sql = "select * from userinfo WHERE BINARY mail='$mail'";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
    $message='mailbox_exsit';
    }
else
{
    $sql = "INSERT INTO userinfo (username, password, mail,sex,birth,place)
    VALUES ('$name', '$passwd', '$mail','$sex','$birth','$place')";
    if (mysqli_query($conn, $sql))
    {
        $message='success';
    }
    else
    {
        $message='fail';
        echo "Error: " . $sql . "<br>" . mysqli_error($conn);
    }
}
} 

$sql ="SET @row=0";
mysqli_query($conn, $sql);
$sql ="UPDATE userinfo SET row_number=(@row:=@row+1)";
mysqli_query($conn, $sql);

mkdir("userdata/".$name,0777,true);
mkdir("userdata/".$name."/"."article",0777,true);
mkdir("userdata/".$name."/"."picture",0777,true);

$json_array = array("message"=>$message); //转换成数组类型
$json= json_encode($json_array);  //将数组转换成json对象
echo  $json;
?>
