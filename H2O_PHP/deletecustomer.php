<?php

//load and connect to MySQL database stuff
require("config.inc.php");

if (!empty($_POST)) {	
	//initial query
	$id = $_POST['id'];
	$valveID = $_POST['valveID'];
	$query = "DELETE FROM customers WHERE id = $id";
  
	//execute query
    try {
        $stmt   = $db->prepare($query);
        $result = $stmt->execute();
    }
    catch (PDOException $ex) {
        $response["success"] = 0;
        $response["message"] = "Database Error. Couldn't delete customer!";
        die(json_encode($response));
    }

    $response["success"] = 1;
    $response["message"] = "Customer Successfully Deleted!";
    echo json_encode($response);
    
    //update the valve status
    $query = "UPDATE nodes SET active=0 WHERE id=$valveID";
     
    //execute query
    try {
    	$stmt   = $db->prepare($query);
    	$stmt->execute();
    }
    catch (PDOException $ex) {
    	$response["success"] = 0;
    	$response["message"] = "Database Error. Couldn't update node!";
    	die(json_encode($response));
    }
    
    $response["success"] = 1;
    $response["message"] = "Node Successfully Updated!";
    echo json_encode($response);
} else {
?>
		<h1>Delete Customer</h1> 
		<form action="deletecustomer.php" method="post"> 
			id:<br /> 
		    <input type="text" name="id" placeholder="id" /> 
		    <br /><br />
		    <input type="submit" value="Delete Customer" /> 
		</form> 
	<?php
}

?> 