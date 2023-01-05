<?php

namespace app\controller;

use support\Request;
use support\Response;

class IndexController {

    public function index(Request $request): Response {

        exec(APPLICATION_PATH . "/aaa.sh");
        return json([]);


        $parameter = $request->get();
        $data = $request->post();


        var_dump($parameter);
        var_dump($data);
        var_dump($request->header());


        // 判断【URL请求】中是否存在【key】
        if (!array_key_exists('key', $parameter)) return json(['status' => false, 'message' => 'Fail', 'code' => -100]);
        $key = $parameter['key'];

        // 加载当前配置文件
        $configPath = APPLICATION_PATH . '\\config.json';
        $config = file_get_contents($configPath);
        $config = json_decode($config, true);

        // 判断当前【key】是否在配置文件中，如果在读取密钥
        if (!array_key_exists($key, $config)) return json(['status' => false, 'message' => 'Fail', 'code' => -101]);
        $secretKey = $config[$key];

        // 从请求中读取 github 的签名值
        $signature = $request->header('HTTP_x-hub-signature-256');


        return json($secretKey);
    }

}
