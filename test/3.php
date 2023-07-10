<?php
function Calculate($prices)
{
    //--- calculate the number of even and odd digits for the two periods
    $period1 = 120;
    $period2 = 5000;
    $count1 = min($period1, count($prices));
    $count2 = min($period2, count($prices));
    $even1 = 0;
    $odd1 = 0;
    $even2 = 0;
    $odd2 = 0;

    for ($i = count($prices) - $count2; $i < count($prices); $i++) {
        if ($prices[$i] >= 0 && $prices[$i] < 10) {
            if ($prices[$i] % 2 == 0) {
                $even2++;
            } else {
                $odd2++;
            }
        }
    }

    for ($i = count($prices) - $count1; $i < count($prices); $i++) {
        if ($prices[$i] >= 0 && $prices[$i] < 10) {
            if ($prices[$i] % 2 == 0) {
                $even1++;
            } else {
                $odd1++;
            }
        }
    }

    //--- calculate the percentages
    $oddPercentage1 = $odd1 * 100.0 / $count1;
    $evenPercentage1 = $even1 * 100.0 / $count1;
    $oddPercentage2 = $odd2 * 100.0 / $count2;
    $evenPercentage2 = $even2 * 100.0 / $count2;

    //--- return the calculated percentages
    return [
        'oddPercentage1' => $oddPercentage1,
        'evenPercentage1' => $evenPercentage1,
        'oddPercentage2' => $oddPercentage2,
        'evenPercentage2' => $evenPercentage2
    ];
}

//--- sample prices data
$prices = [1.23, 4.56, 7.89, 2.34, 5.67, 8.90];

//--- call the Calculate function
$result = Calculate($prices);

//--- print the results
echo "Odd Percentage 1: " . $result['oddPercentage1'] . "%\n";
echo "Even Percentage 1: " . $result['evenPercentage1'] . "%\n";
echo "Odd Percentage 2: " . $result['oddPercentage2'] . "%\n";
echo "Even Percentage 2: " . $result['evenPercentage2'] . "%\n";
?>
