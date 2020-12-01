<?php
$username = $_POST['username'];

$file = $_FILES['btn_file']['tmp_name']; //上传的文件
$fileName = $_FILES['btn_file']['name']; //文件的名称(用来做文件名)
$path = "userdata/" . $username . "/picture/"; //文件保存位置

require_once('connect_database.php');
$conn = connect_database();

$sql = "select row_number from eye_picture order by row_number DESC limit 1";
$result = mysqli_query($conn, $sql);
$row = $result->fetch_array();

if ($row["row_number"] == '') $row["row_number"] = 1;
else $row["row_number"]+=1;

$pathdata=pathinfo($fileName);
$exten_name=$pathdata['extension'];

//更新数据库eye_picture
$uptime=date('Y-m-d h:i:s', time());
$sql = "INSERT INTO eye_picture (uploader,uptime,picture)
VALUES ('$username', '$uptime', '$exten_name')";
if (mysqli_query($conn, $sql)) {
    $message = 'success';
} else {
    $message = 'fail';
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
}

//保存图片
move_uploaded_file($file, $path . $row["row_number"] . ".".$exten_name);

//刷新row_number
$sql = "SET @row=0";
mysqli_query($conn, $sql);
$sql = "UPDATE eye_picture SET row_number=(@row:=@row+1)";
mysqli_query($conn, $sql);

//更新数据库userinfo
$sql="select historypicture from userinfo where username='$username'";
$result=mysqli_query($conn, $sql);
$rrow=$result->fetch_array();
$newpic=$rrow["historypicture"].$row["row_number"].",";
$sql="update userinfo set historypicture='$newpic' where username='$username'"; 
mysqli_query($conn, $sql);

$json_array = array("message"=>$message,"username"=>$username,"filename"=>$row["row_number"] . ".".$exten_name,"row_number"=>$row["row_number"]); //转换成数组类型
$json= json_encode($json_array);  //将数组转换成json对象
echo  $json;
?>