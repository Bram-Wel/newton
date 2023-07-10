<?php

// Function to retrieve tick data for a specific currency market
function getTickData($market) {
    $apiToken = 'KvYb9l3iQwSRKeC';
    
    // Build the API request URL
    $url = 'https://deriv.example.com/api/ticks?market=' . urlencode($market) . '&limit=5000';
    
    // Set the headers with the API token
    $headers = array(
        'Authorization: Bearer ' . $apiToken,
        'Content-Type: application/json'
    );
    
    // Initialize cURL
    $ch = curl_init();
    
    // Set the cURL options
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    
    // Execute the API request
    $response = curl_exec($ch);
    
    // Close cURL
    curl_close($ch);
    
    // Return the tick data as an associative array
    return json_decode($response, true);
}

// Function to calculate the percentage of odd and even ticks for a given tick data array
function calculatePercentage($tickData, $period) {
    $totalTicks = count($tickData);
    $count = min($period, $totalTicks);
    $even = 0;
    $odd = 0;
    
    for ($i = $totalTicks - $count; $i < $totalTicks; $i++) {
        if ($tickData[$i] % 2 === 0) {
            $even++;
        } else {
            $odd++;
        }
    }
    
    // Calculate the percentage values
    $evenPercentage = ($even / $count) * 100;
    $oddPercentage = ($odd / $count) * 100;
    
    return array(
        'even' => $evenPercentage,
        'odd' => $oddPercentage
    );
}

// API endpoint to fetch tick data and calculate percentages
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Retrieve the market parameter from the query string
    $market = $_GET['market'] ?? '';
    
    if ($market) {
        // Fetch the tick data for the specified market
        $tickData = getTickData($market);
        
        // Calculate the percentages for different periods
        $percentage5000 = calculatePercentage($tickData, 5000);
        $percentage120 = calculatePercentage($tickData, 120);
        $percentage20 = calculatePercentage($tickData, 20);
        
        // Create a JSON response
        $response = array(
            'market' => $market,
            'percentage5000' => $percentage5000,
            'percentage120' => $percentage120,
            'percentage20' => $percentage20
        );
        
        // Set the response headers
        header('Content-Type: application/json');
        
        // Send the JSON response
        echo json_encode($response);
        exit();
    }
}

// If the request method is not GET or the market parameter is missing, return an error
http_response_code(400);
echo json_encode(array('error' => 'Invalid request'));
exit();

?>
