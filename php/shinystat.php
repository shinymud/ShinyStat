<?php
$HOST = "www.incendiarysoftware.com";
$PORT = 4112;
$IMAGE_BASE_URL = "http://www.incendiarysoftware.com/shinystat/";
$GAME_PAGE = "http://shiny.incendiarysoftware.com/#see";

$template = <<<TEMP
<html>
<head>
<base href="$IMAGE_BASE_URL" />
<link rel="stylesheet" type="text/css" href="shinystat.css" />
</head>
<body>
<div id="shiny_game_results">
<div id="shiny_status" style="height: 50px;">
<a href="$GAME_PAGE" target="_blank"><img id="status_img" src="%s.png"/></a>
<div id="shiny_text_block">
<div id="shiny_status_text">Our <a target="_blank" href="$GAME_PAGE">ShinyMUD</a> server is:
<span id="shiny_online">%s</span></div>
%s
</div>
</div>
<div id="shiny_game_status_footer"></div>
</div>
<body>
</html>
TEMP;

$offline = <<<FAIL
<div id="shiny_restarted">Don't worry, we'll have it back up soon!</div>
FAIL;

try{
    $fp = fsockopen($HOST, $PORT, $errno, $errstr, 0.5);
}
catch(Exception $e){
    # Assume the server is offline if something goes awry in opening the socket
    printf($template, 'offline', 'Offline', $offline);
}
if (!$fp) {
    # Assume that the server is offline if we don't get a connection
    printf($template, 'offline', 'Offline', $offline);
} else {
    $response = fgets($fp, 1024);
    fclose($fp);
    // data is given in the form name,name:date
    $data = explode(':', $response);
    $num_names = $data[1] ? count(explode(',', $data[1])) : 0;
    $restart = date("F d, Y", $data[0]);
    if ($num_names == 0) {$playing = 'There are <span class="highlight">no players</span>';}
    elseif ($num_names == 1) {$playing = 'There is <span class="highlight">1 player</span>';}
    else {$playing = 'There are <span class="highlight">' . $num_names . " players</span>";}
    $online = <<<WIN
<div id="shiny_restarted">Last restarted: <span class="highlight">$restart</span></div>
<div id="shiny_player">$playing online right now.</div>
WIN;
    printf($template, 'online', 'Online', $online);
}
?>