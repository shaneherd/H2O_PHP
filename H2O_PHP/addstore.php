<?php

//load and connect to MySQL database stuff
require("config.inc.php");

if (!empty($_POST)) {
	//initial query
	$query = "INSERT INTO stores ( name, location ) VALUES ( :name, :location ) ";

    //Update query
    $query_params = array(
        ':name' => $_POST['name'],
		':location' => $_POST['location']
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
        $response["message"] = "Database Error. Couldn't add store!";
        die(json_encode($response));
    }

    $response["success"] = 1;
    $response["message"] = "Store Successfully Added!";
    echo json_encode($response);
   
} else {
?>
		<h1>Add Store</h1> 
		<form action="addstore.php" method="post"> 
		    Name:<br /> 
		    <input type="text" name="name" placeholder="store name" /> 
		    <br /><br />
			Location:<br /> 
		    <input type="text" name="location" placeholder="store location" /> 
		    <br /><br />
		    <input type="submit" value="Add Store" /> 
		</form> 
	<?php
}

?> 