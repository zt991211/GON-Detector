<?php
require_once('connect_database.php');
//header("content-type:application/x-www-form-urlencoded;charset=utf-8");
header("content-type:application/x-www-form-urlencoded"); 
$name=$_POST["username"];
$oldpwd=$_POST["oldpwd"];
$newpwd=$_POST["newpwd"];

$conn=connect_database();

$sql = "select * from userinfo WHERE BINARY username='$name'";
$result = $conn->query($sql);
$row = $result->fetch_assoc();
if($oldpwd!=$row["password"])
{
    $message="原密码错误";
}
else{
    $sql = "UPDATE userinfo SET password='$newpwd' WHERE BINARY username='$name'";
    $retval = mysqli_query( $conn, $sql );//我也不知道为什么要加这句话，但是没有就是无法更新成功

/*    $retval = mysqli_query( $conn, $sql );
    if(! $retval )
    {
        die('无法更新数据: ' . mysqli_error($conn));
    }
    echo '数据更新成功！';
*/

    $message="密码修改成功";
}

$json_array = array("message"=>$message); //转换成数组类型
$json= json_encode($json_array);  //将数组转换成json对象
echo  $json;

//echo $b;

/*$data = [
    'code'=>'1',
    'msg'=>'成功',
    'data'=>array('1'=>'1','2'=>'2'),
];
return json_encode($data,JSON_UNESCAPED_UNICODE);
*/
?>