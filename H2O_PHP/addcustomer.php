<?php

//load and connect to MySQL database stuff
require("config.inc.php");

if (!empty($_POST)) {	
	//initial query
	$query = "INSERT INTO customers ( valveID, firstName, lastName, serviceStartDate, litersPerDay, pricePerLiter ) VALUES ( :valveID, :firstName, :lastName, :serviceStartDate, :litersPerDay, :pricePerLiter)";
    $query_params = array(
		':valveID' => $_POST['valveID'],
		':firstName' => $_POST['firstName'],
		':lastName' => $_POST['lastName'],
		':serviceStartDate' => $_POST['serviceStartDate'],
		':litersPerDay' => $_POST['litersPerDay'],
		':pricePerLiter' => $_POST['pricePerLiter']
    );
  
	//execute query
    try {
        $stmt   = $db->prepare($query);
        $result = $stmt->execute($query_params);
    }
    catch (PDOException $ex) {
        // For testing, you could use a die and message. 
        //die("Failed to run query: " . $ex->getMessage());
        
        //or just use this use this one:
        $response["success"] = 0;
        $response["message"] = "Database Error. Couldn't add customer!";
        die(json_encode($response));
    }

    $response["success"] = 1;
    $response["message"] = "Customer Successfully Added!";
    echo json_encode($response);
    
    $valve = $_POST['valveID'];
    $query = "UPDATE nodes SET active=1 WHERE id = $valve";
    
    //execute query
    try {
    	$stmt   = $db->prepare($query);
    	$stmt->execute();
    }
    catch (PDOException $ex) {
    	$response["success"] = 0;
    	$response["message"] = "Database Error. Couldn't activate valve!";
    	die(json_encode($response));
    }
    
    $response["success"] = 1;
    $response["message"] = "Valve Successfully Activated!";
    echo json_encode($response);
} else {
?>
		<h1>Add Customer</h1> 
		<form action="addcustomer.php" method="post"> 
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
		    <input type="submit" value="Add Customer" /> 
		</form> 
	<?php
}

?> 