<?php
if (isset($_GET['id'])) {
    $host = "localhost";
    $username = "root";
    $password = "";
    $database = "tilavaraus";

    try {
        $conn = new PDO("mysql:host=$host;dbname=$database", $username, $password);
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $id = $_GET['id'];
        $sql = "DELETE FROM tilat WHERE id = :id";
        $stmt = $conn->prepare($sql);
        $stmt->bindParam(':id', $id);
        $stmt->execute();

        echo "<p>Tila poistettu onnistuneesti!</p>";
    } catch (PDOException $e) {
        echo "<p>Virhe: " . $e->getMessage() . "</p>";
    }
}
?>
