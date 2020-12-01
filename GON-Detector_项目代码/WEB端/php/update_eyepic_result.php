<?php
$prob = $_POST['prob'];
$vcdr=$_POST['vcdr'];
$hcdr=$_POST['hcdr'];
$num=$_POST['row_number'];

require_once('connect_database.php');
$conn = connect_database();

$sql="update eye_picture set prob='$prob',vcdr='$vcdr',hcdr='$hcdr' where row_number='$num' ";
if (mysqli_query($conn, $sql)) {
    $message = 'success';
} else {
    $message = 'fail';
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
}

$json_array = array("message"=>$message);
$json= json_encode($json_array);
echo  $json;
?>