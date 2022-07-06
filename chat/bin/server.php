<?php

use Ratchet\Server\IoServer;
use MyApp\Chat;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;
 
require dirname ( __DIR__ ) . '/vendor/autoload.php';

require_once 'src/chat.php';
 
$server = IoServer::factory ( new HttpServer( new WsServer( new Chat () ) ), 9540 );
$server->run ();

// php bin/server.php & で起動