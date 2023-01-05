#!/usr/bin/env php
<?php
require_once __DIR__ . '/vendor/autoload.php';

$path = realpath(dirname(__FILE__));
define('APPLICATION_PATH', $path);

support\App::run();
