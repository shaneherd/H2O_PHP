<?php

//load and connect to MySQL database stuff
require("config.inc.php");

if (!empty($_POST)) {
	//initial query
	$query = "INSERT INTO nodes(address, type, parent, active) VALUES (UNHEX(:address), :type, UNHEX(:parent), :active)";
	//Update query
    $query_params = array(
		':address' => $_POST['address'],
		':type' => $_POST['type'],
		':parent' => $_POST['parent'],
    	':active' => $_POST['active']
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
        $response["message"] = "Database Error. Couldn't add node!";
        die(json_encode($response));
    }

    $response["success"] = 1;
    $response["message"] = "Node Successfully Added!";
    echo json_encode($response);
   
} else {
?>
		<h1>Add Node</h1> 
		<form action="addnode.php" method="post"> 
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
		    <input type="submit" value="Add Node" /> 
		</form> 
	<?php
}

?> 