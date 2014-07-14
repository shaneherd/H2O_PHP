<?php

//load and connect to MySQL database stuff
require("config.inc.php");

if (!empty($_POST)) {
	$valveID = $_POST['valveID'];
	$address = $_POST['address'];
	$type = $_POST['type'];
	$parent = $_POST['parent'];
	$active = $_POST['active'];
	$oldAddress = $_POST['oldAddress'];
    $query = "UPDATE nodes SET address = x'$address', type=$type, parent=x'$parent', active=$active  where id = $valveID";
    
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
    
    //execute query
    try {
    	$stmt   = $db->prepare($query);
    	$stmt->execute();
    }
    catch (PDOException $ex) {
    	$response["success"] = 0;
    	$response["message"] = "Database Error. Couldn't update customer!";
    	die(json_encode($response));
    }
    
    $response["success"] = 1;
    $response["message"] = "Customer Successfully Updated!";
    echo json_encode($response);
   
} else {
?>
		<h1>Update Node</h1> 
		<form action="updatenode.php" method="post"> 
			valveID:<br /> 
		    <input type="text" name="valveID" placeholder="valveID" /> 
		    <br /><br />
			address:<br /> 
		    <input type="text" name="address" placeholder="address" /> 
		    <br /><br />
		    type:<br /> 
		    <input type="text" name="type" placeholder="type" /> 
		    <br /><br />
			parent:<br /> 
		    <input type="text" name="parent" placeholder="parent" /> 
		    <br /><br />
		    active:<br /> 
		    <input type="text" name="active" placeholder="active" /> 
		    <br /><br />
		    <input type="submit" value="Update Node" /> 
		</form> 
	<?php
}

?> 