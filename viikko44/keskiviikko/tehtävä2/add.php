<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lisää uusi tila</title>
</head>
<body>
    <h2>Lisää uusi tila</h2>
    <form action="add.php" method="POST">
        <label for="tilan_nimi">Tilan nimi:</label>
        <input type="text" name="tilan_nimi" id="tilan_nimi" required>
        <input type="submit" value="Lisää">
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $host = "localhost";
        $username = "root";
        $password = "";
        $database = "tilavaraus";

        try {
            $conn = new PDO("mysql:host=$host;dbname=$database", $username, $password);
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

            $tilan_nimi = $_POST['tilan_nimi'];
            $sql = "INSERT INTO tilat (tilan_nimi) VALUES (:tilan_nimi)";
            $stmt = $conn->prepare($sql);
            $stmt->bindParam(':tilan_nimi', $tilan_nimi);
            $stmt->execute();

            echo "<p>Uusi tila lisätty onnistuneesti!</p>";
        } catch (PDOException $e) {
            echo "<p>Virhe: " . $e->getMessage() . "</p>";
        }
    }
    ?>
</body>
</html>
