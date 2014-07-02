<?php

/*
Our "config.inc.php" file connects to database every time we include or require
it within a php script.  Since we want this script to add a new user to our db,
we will be talking with our database, and therefore,
let's require the connection to happen:
*/
require("config.inc.php");
$query_params=null;

//initial query
$query = "Select id, valveID, firstName, lastName, serviceStartDate, litersPerDay, pricePerLiter, active FROM customers";

//execute query
try {
    $stmt   = $db->prepare($query);
    $result = $stmt->execute($query_params);
}
catch (PDOException $ex) {
    $response["success"] = 0;
    $response["message"] = "Database Error!";
    die(json_encode($response));
}

// Finally, we can retrieve all of the found rows into an array using fetchAll 
$rows = $stmt->fetchAll();


if ($rows) {
    $response["success"] = 1;
    $response["message"] = "Post Available!";
    $response["posts"]   = array();
    
    foreach ($rows as $row) {
        $post             = array();
		$post["id"]  = $row["id"];
		$post["valveID"] = $row["valveID"];
        $post["firstName"] = $row["firstName"];
        $post["lastName"]    = $row["lastName"];
		$post["serviceStartDate"]  = $row["serviceStartDate"];
		$post["litersPerDay"]  = $row["litersPerDay"];
		$post["pricePerLiter"]  = $row["pricePerLiter"];
		$post["active"]  = $row["active"];
        
        
        //update our repsonse JSON data
        array_push($response["posts"], $post);
    }
    
    // echoing JSON response
    echo json_encode($response);
    
    
} else {
    $response["success"] = 0;
    $response["message"] = "No Post Available!";
    die(json_encode($response));
}

?>
