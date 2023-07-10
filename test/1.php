<?php

// Deriv API credentials
$api_key = 'YOUR_API_KEY';
$base_url = 'https://api.deriv.com';

// Currency to retrieve statistics for
$currency = 'USD';

// Endpoint URL for currency statistics
$endpoint = "/v2/reference/symbols/$currency";

// Construct the request URL
$request_url = $base_url . $endpoint;

// Set request headers
$headers = array(
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key,
);

// Initialize cURL session
$ch = curl_init();

// Set cURL options
curl_setopt($ch, CURLOPT_URL, $request_url);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

// Execute the API request
$response = curl_exec($ch);

// Check for errors
if(curl_error($ch)) {
    die('Error: ' . curl_error($ch));
}

// Close the cURL session
curl_close($ch);

// Parse the response
$data = json_decode($response, true);

// Extract the relevant statistics
$symbol = $data['symbols'][0]['symbol'];
$display_name = $data['symbols'][0]['display_name'];
$pip = $data['symbols'][0]['pip'];

// Display the statistics
echo "Symbol: $symbol <br>";
echo "Display Name: $display_name <br>";
echo "PIP: $pip <br>";

?>
