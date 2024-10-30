<?php
$host = "localhost";
$username = "root";
$password = "";
$database = "tilavaraus";

try {
    $conn = new PDO("mysql:host=$host;dbname=$database", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}

function add_tila($tilan_nimi, $conn) {
    try {
        $stmt = $conn->prepare("INSERT INTO tilat (tilan_nimi) VALUES (:tilan_nimi)");
        $stmt->bindParam(':tilan_nimi', $tilan_nimi);
        $stmt->execute();
        return "Tila '$tilan_nimi' lisätty.";
    } catch (PDOException $e) {
        return "Virhe: " . $e->getMessage();
    }
}

function add_varaaja($varaajan_nimi, $conn) {
    try {
        $stmt = $conn->prepare("INSERT INTO varaajat (nimi) VALUES (:varaajan_nimi)");
        $stmt->bindParam(':varaajan_nimi', $varaajan_nimi);
        $stmt->execute();
        return "Varaaja '$varaajan_nimi' lisätty.";
    } catch (PDOException $e) {
        return "Virhe: " . $e->getMessage();
    }
}

function add_varaus($tila_id, $varaaja_id, $varauspaiva, $conn) {
    try {
        $stmt = $conn->prepare("INSERT INTO varaukset (tila, varaaja, varauspaiva) VALUES (:tila, :varaaja, :varauspaiva)");
        $stmt->bindParam(':tila', $tila_id);
        $stmt->bindParam(':varaaja', $varaaja_id);
        $stmt->bindParam(':varauspaiva', $varauspaiva);
        $stmt->execute();
        return "Varaus lisätty.";
    } catch (PDOException $e) {
        return "Virhe: " . $e->getMessage();
    }
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $message = "";

    // Tilan lisääminen
    if (isset($_POST['add_tila'])) {
        $tilan_nimi = $_POST['tilan_nimi'];
        $message = add_tila($tilan_nimi, $conn);
    }

    // Varaajan lisääminen
    if (isset($_POST['add_varaaja'])) {
        $varaajan_nimi = $_POST['varaaja_nimi'];
        $message = add_varaaja($varaajan_nimi, $conn);
    }

    // Varauksen lisääminen
    if (isset($_POST['add_varaus'])) {
        $tila_id = $_POST['tila_id'];
        $varaaja_id = $_POST['varaaja_id'];
        $varauspaiva = $_POST['varauspaiva'];
        $message = add_varaus($tila_id, $varaaja_id, $varauspaiva, $conn);
    }

    // Siirrä takaisin index.php:hen viestin kanssa
    header("Location: index.php?message=" . urlencode($message));
    exit;
}
?>
