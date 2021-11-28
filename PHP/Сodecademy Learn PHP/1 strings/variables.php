<?php
$mood = ":)";
$biography = "\nI love cats (･ω･)";
$favorite_food = "\n" . "tur" . "duck" . "en";

$name = "Kita";
$language = "PHP";
echo "\nmy name is " . $name;
echo "\nI'm learning " . $language;

$noun = "cat";
$adjective = "emotional";
$verb = "chill";
echo "\nThe world's most beloved $noun was very $adjective and loved to $verb every single day.";
echo "\nI have always been obsessed with ${noun}s. I'm ${adjective}ish. I'm always ${verb}ing.";

$movie = "Serial Experiments Lain";
$old_favorite = $movie;
echo "\nI'm a fickle person, my favorite movie used to be $movie.";
$movie = "Yuru Yuri";
echo "\nBut now my favorite is $movie.";
echo "\nBut I'll always have a special place in my heart for $old_favorite.";

$sentence = "\nI'm going on a picnic, and I'm taking apples";
$sentence .= ", burgers";
$sentence .= ", cider and a salad.";
echo $sentence;

$very_bad_unclear_name = "15 chicken wings";
$order =& $very_bad_unclear_name;
$order .= ", a salad";
$order .= " and a cola.";
echo "\nYour order is: $very_bad_unclear_name.";
