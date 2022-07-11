<?php

use Ratchet\Server\IoServer;
use MyApp\Chat;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;
 
require dirname ( __DIR__ ) . '/vendor/autoload.php';

require_once 'src/chat.php';
 


// $server = IoServer::factory ( new HttpServer( new WsServer( new Chat () ) ), 9540 );
// $server->run ();

$app = new \Ratchet\Http\HttpServer(
    new \Ratchet\WebSocket\WsServer(
        new Chat()
    )
);

$loop = \React\EventLoop\Factory::create();

$secure_websockets = new \React\Socket\Server('0.0.0.0:9540', $loop);
$secure_websockets = new \React\Socket\SecureServer($secure_websockets, $loop, [
    'local_cert' => 'C:/Certbot/live/bekondaisuki.hopto.org/cert.pem',
    'local_pk' => 'C:/Certbot/live/bekondaisuki.hopto.org/privkey.pem',
    'verify_peer' => false
]);

$secure_websockets_server = new \Ratchet\Server\IoServer($app, $secure_websockets, $loop);
$secure_websockets_server->run();




// php bin/server.php & で起動