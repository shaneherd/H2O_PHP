<?php

//load and connect to MySQL database stuff
require("config.inc.php");

if (!empty($_POST)) {
	$id = $_POST['id'];
    $query = "UPDATE status SET status=1  where id = $id";
    
    //execute query
    try {
    	$stmt   = $db->prepare($query);
    	$stmt->execute();
    }
    catch (PDOException $ex) {
    	$response["success"] = 0;
    	$response["message"] = "Database Error. Couldn't update status!";
    	die(json_encode($response));
    }

    $response["success"] = 1;
    $response["message"] = "Status Successfully Updated!";
    echo json_encode($response); 
    
    $query = "UPDATE status SET status=0  where id != $id";
    
    //execute query
    try {
    	$stmt   = $db->prepare($query);
    	$stmt->execute();
    }
    catch (PDOException $ex) {
    	$response["success"] = 0;
    	$response["message"] = "Database Error. Couldn't update status!";
    	die(json_encode($response));
    }
    
    $response["success"] = 1;
    $response["message"] = "Status Successfully Updated!";
    echo json_encode($response);
} else {
?>
		<h1>Update Status</h1> 
		<form action="updatestatus.php" method="post"> 
			id:<br /> 
		    <input type="text" name="id" placeholder="id" /> 
		    <br /><br />
		    <input type="submit" value="Update Status" /> 
		</form> 
	<?php
}

?> 