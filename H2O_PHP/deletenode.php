<?php

//load and connect to MySQL database stuff
require("config.inc.php");

if (!empty($_POST)) {	
	//initial query
	$valveID = $_POST['valveID'];
	
	//update the valve status
	$query = "UPDATE customers SET valveID=NULL WHERE valveID=$valveID";
	 
	//execute query
	try {
		$stmt   = $db->prepare($query);
		$stmt->execute();
	}
	catch (PDOException $ex) {
		$response["success"] = 0;
		$response["message"] = "Database Error. Couldn't update customer with valveID=$valveID!";
		die(json_encode($response));
	}
	
	$response["success"] = 1;
	$response["message"] = "Customer Successfully Updated!";
	echo json_encode($response);
	
	$query = "DELETE FROM nodes WHERE id = $valveID";
  
	//execute query
    try {
        $stmt   = $db->prepare($query);
        $result = $stmt->execute();
    }
    catch (PDOException $ex) {
        $response["success"] = 0;
        $response["message"] = "Database Error. Couldn't delete node!";
        die(json_encode($response));
    }

    $response["success"] = 1;
    $response["message"] = "Node Successfully Deleted!";
    echo json_encode($response);
} else {
?>
		<h1>Delete Node</h1> 
		<form action="deletenode.php" method="post"> 
			id:<br /> 
		    <input type="text" name="valveID" placeholder="valveID" /> 
		    <br /><br />
		    <input type="submit" value="Delete Node" /> 
		</form> 
	<?php
}

?> 