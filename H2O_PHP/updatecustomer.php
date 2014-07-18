<?php

//load and connect to MySQL database stuff
require("config.inc.php");

if (!empty($_POST)) {	
	$id = $_POST['id'];
	$valveID = $_POST['valveID'];
	$firstName = $_POST['firstName'];
	$lastName = $_POST['lastName'];
	$serviceStartDate = $_POST['serviceStartDate'];
	$litersPerDay = $_POST['litersPerDay'];
	$pricePerLiter = $_POST['pricePerLiter'];
	$oldValveID = $_POST['oldValveID'];
    $query = "UPDATE customers SET valveID=$valveID, firstName='$firstName', lastName='$lastName', serviceStartDate='$serviceStartDate', litersPerDay=$litersPerDay, pricePerLiter=$pricePerLiter WHERE id=$id";
    
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
    
    $query = "UPDATE nodes SET active=0 WHERE id=$oldValveID";
     
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
    
    //update the valve status
    $query = "UPDATE nodes SET active=1 WHERE id=$valveID";
    	
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
		<h1>Add Customer</h1> 
		<form action="updatecustomer.php" method="post"> 
			ID:<br /> 
		    <input type="text" name="id" placeholder="id" /> 
		    <br /><br />
			valveID:<br /> 
		    <input type="text" name="valveID" placeholder="valveID" /> 
		    <br /><br />
		    firstName:<br /> 
		    <input type="text" name="firstName" placeholder="firstName" /> 
		    <br /><br />
			lastName:<br /> 
		    <input type="text" name="lastName" placeholder="lastName" /> 
		    <br /><br />
			serviceStartDate:<br /> 
		    <input type="text" name="serviceStartDate" placeholder="serviceStartDate" /> 
		    <br /><br />
			litersPerDay:<br /> 
		    <input type="text" name="litersPerDay" placeholder="litersPerDay" /> 
		    <br /><br />
			pricePerLiter:<br /> 
		    <input type="text" name="pricePerLiter" placeholder="pricePerLiter" /> 
		    <br /><br />
		    <input type="submit" value="Update Customer" /> 
		</form> 
	<?php
}

?> 