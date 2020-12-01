<?php
function connect_database()
{
$servername = "localhost";
$username = "root";
$password = "123456";
$dbname = "gon_detecter"; 
$conn = new mysqli($servername, $username, $password,$dbname);

return $conn;
}
?>