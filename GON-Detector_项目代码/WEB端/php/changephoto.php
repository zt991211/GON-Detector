<?php
$username = $_POST['change_picture_name'];

$file = $_FILES['userphoto']['tmp_name']; //上传的文件
$fileName = $_FILES['userphoto']['name']; //文件的名称(用来做文件名)
$path = "userdata/" . $username . "/"; //文件保存位置

$pathdata=pathinfo($fileName);
$exten_name=$pathdata['extension'];
move_uploaded_file($file, $path . "tx" . ".".$exten_name);

//更新数据库
require_once('connect_database.php');
$conn = connect_database();

$sql = "UPDATE userinfo SET userphoto='$exten_name' where username='$username'";
if(mysqli_query($conn, $sql))
{
    $message='success';
}
else
{
    $message='fail';
}

$json_array = array("message"=>$message); //转换成数组类型
$json= json_encode($json_array);  //将数组转换成json对象
echo  $json;
?>