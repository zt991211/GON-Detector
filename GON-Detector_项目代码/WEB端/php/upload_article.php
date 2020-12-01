<?php
$username = $_POST['username'];
$title = $_POST["bj_title"];
$intro = $_POST["bj_intro"];
$uptime=date('Y-m-d h:i:s', time());

//连接数据库
require_once('connect_database.php');
$conn = connect_database();

//确定新的文章在article数据库中的编号
$sql ="select row_number from article order by row_number DESC limit 1";
$result=mysqli_query($conn, $sql);
$row=$result->fetch_array();
if($row["row_number"]=='')$row["row_number"]=0;
$row["row_number"]+=1;

//向article中插入新的文章
$sql = "INSERT INTO article (title,writer,intro,uptime)
VALUES ('$title', '$username', '$intro','$uptime')";
if (mysqli_query($conn, $sql)) {
    $message = 'success';
} else {
    $message = 'fail';
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
}

//保存上传的文章
$file = $_FILES['afile']['tmp_name']; //上传的文件
$fileName = $_FILES['afile']['name']; //文件的名称(用来做文件名)
$path = "userdata/" . $username . "/article/"; //文件保存位置
move_uploaded_file($file, $path . $row["row_number"] . ".md");

$sql = "SET @row=0";
mysqli_query($conn, $sql);
$sql = "UPDATE article SET row_number=(@row:=@row+1)";
mysqli_query($conn, $sql);

//保存上传的图片并更新数据库
if ($_FILES['pfile']['error'] == 0) {
    $file = $_FILES['pfile']['tmp_name']; //上传的文件
    $fileName = $_FILES['pfile']['name']; //文件的名称(用来做文件名)
    $path = "userdata/" . $username . "/article/"; //文件保存位置

    $pathdata=pathinfo($fileName);
    $exten_name=$pathdata['extension'];
    $newfilename=$row["row_number"].'.'.$exten_name;

    move_uploaded_file($file, $path . $newfilename);

    $newnum=$row["row_number"];
    $sql="UPDATE article SET picture='$exten_name' WHERE row_number='$newnum'";
    if (mysqli_query($conn, $sql)) {
    $message = 'success';
    } else {
    $message = 'fail';
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
    }  
}

//更新文章
$sql="select article from userinfo where username='$username'";
$result=mysqli_query($conn, $sql);
$row=$result->fetch_array();
$newarticle=$row["article"].$newnum.",";
$sql="update userinfo set article='$newarticle' where username='$username'"; 
mysqli_query($conn, $sql);


$json_array = array("message" => $message); //转换成数组类型
$json = json_encode($json_array);  //将数组转换成json对象
echo  $json;
/*$url = "http://localhost/forum.html?username=" . $username;
if (isset($url)) {
    echo "<SCRIPT language= 'JavaScript'>location.href='$url'</SCRIPT>";
} else {
    echo "没有跳转的地址！";
}*/
?>