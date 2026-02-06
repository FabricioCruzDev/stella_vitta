<?php
// 1. Diagnóstico de erros
ini_set('display_errors', 1);
error_reporting(E_ALL);

header("Content-Type: application/json; charset=UTF-8");

// 2. Tenta carregar as configurações via Array
$configPath = __DIR__ . '/config.php';

if (!file_exists($configPath)) {
    echo json_encode(["success" => false, "message" => "Erro: Arquivo config.php nao encontrado."]);
    exit;
}

// O include agora retorna o array definido no config.php
$config = include $configPath;

// 3. Verifica se o array foi carregado com os dados necessários
if (!is_array($config) || !isset($config['db'])) {
    echo json_encode(["success" => false, "message" => "Erro: As configuracoes nao foram lidas. Verifique se o config.php começa com <?php e tem o 'return'. "]);
    exit;
}

try {
    // 4. Conexão com o Banco usando os dados do Array
    $pdo = new PDO(
        "mysql:host=" . $config['host'] . ";dbname=" . $config['db'] . ";charset=utf8", 
        $config['user'], 
        $config['pass']
    );
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // 5. Processamento dos dados
    $json = file_get_contents("php://input");
    $data = json_decode($json, true);

    if ($data) {
        $nome     = strip_tags(trim($data['nome']));
        $email    = filter_var(trim($data['email']), FILTER_SANITIZE_EMAIL);
        $telefone = strip_tags(trim($data['telefone']));

        if (empty($nome) || empty($email) || empty($telefone)) {
            echo json_encode(["success" => false, "message" => "Preencha todos os campos."]);
            exit;
        }

        // Verifica duplicidade
        $stmt = $pdo->prepare("SELECT id FROM contatos_leads WHERE email = ? OR telefone = ? LIMIT 1");
        $stmt->execute([$email, $telefone]);

        if ($stmt->fetch()) {
            echo json_encode(["success" => false, "message" => "E-mail ou Telefone ja cadastrados."]);
            exit;
        }

        // Insere contato
        $stmt = $pdo->prepare("INSERT INTO contatos_leads (nome, email, telefone, data_registro) VALUES (?, ?, ?, NOW())");
        $stmt->execute([$nome, $email, $telefone]);

        echo json_encode(["success" => true, "message" => "Cadastro realizado com sucesso!"]);
    } else {
        echo json_encode(["success" => false, "message" => "Nenhum dado recebido."]);
    }

} catch (PDOException $e) {
    // Se a conexão falhar aqui, saberemos se é senha ou nome do banco
    echo json_encode(["success" => false, "message" => "Erro de Conexão: " . $e->getMessage()]);
}