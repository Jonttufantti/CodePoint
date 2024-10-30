<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles.css">
    <title>Tietokantatiedot</title>

</head>

<body>
    <?php
    $host = "localhost";
    $username = "root";
    $password = "";
    $database = "tilavaraus";

    try {
        $conn = new PDO("mysql:host=$host;dbname=$database", $username, $password);
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    } catch (PDOException $e) {
        echo "<p>Connection failed: " . $e->getMessage() . "<p>";
    }

    $sql_tilat = "SELECT * FROM tilat";
    $sql_varaajat = "SELECT * FROM varaajat";
    $sql_varaukset = "
        SELECT 
            varaukset.id,
            tilat.tilan_nimi AS tila,
            varaajat.nimi AS varaaja,
            varaukset.varauspaiva
        FROM 
            varaukset
        INNER JOIN 
            tilat ON varaukset.tila = tilat.id
        INNER JOIN 
            varaajat ON varaukset.varaaja = varaajat.id
    ";

    function nayta_taulukko($conn, $sql, $otsikot) {
        try {
            $query = $conn->prepare($sql);
            $query->execute();
            $result = $query->fetchAll(PDO::FETCH_ASSOC);

            echo "<table border='1'><tr>";
            foreach ($otsikot as $otsikko) {
                echo "<th>$otsikko</th>";
            }
            echo "</tr>";

            foreach ($result as $row) {
                echo "<tr>";
                foreach ($row as $cell) {
                    echo "<td>$cell</td>";
                }
                echo "</tr>";
            }
            echo "</table><br>";
        } catch (PDOException $e) {
            die("Query error: " . $e->getMessage());
        }
    }

echo '<div class="taulukko-container">';

echo '<div class="taulukko">';
echo "<h2>Tilat</h2>";
nayta_taulukko($conn, $sql_tilat, ["ID", "Tilan nimi"]);

echo '<h3>Lisää uusi tila</h3>';
echo '<form method="post" action="">
    <input type="text" name="tilan_nimi" placeholder="Tilan nimi" required>
    <button type="submit" name="add_tila">Lisää tila</button>
</form>';
echo '</div>';

echo '<div class="taulukko">';
echo "<h2>Varaajat</h2>";
nayta_taulukko($conn, $sql_varaajat, ["ID", "Nimi"]);

echo '<h3>Lisää uusi varaaja</h3>';
echo '<form method="post" action="">
    <input type="text" name="varaaja_nimi" placeholder="Varaajan nimi" required>
    <button type="submit" name="add_varaaja">Lisää varaaja</button>
</form>';
echo '</div>';

echo '<div class="taulukko">';
echo "<h2>Varaukset</h2>";
nayta_taulukko($conn, $sql_varaukset, ["ID", "Tila", "Varaaja", "Varauspäivä"]);

echo '<h3>Lisää uusi varaus</h3>';
echo '<form method="post" action="">
    <input type="number" name="varaus_tila" placeholder="Tila ID" required>
    <input type="number" name="varaus_varaaja" placeholder="Varaaja ID" required>
    <input type="date" name="varauspaiva" required>
    <button type="submit" name="add_varaus">Lisää varaus</button>
</form>';
echo '</div>';

echo '</div>';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Lisää tila
    if (isset($_POST['add_tila'])) {
        $tilan_nimi = $_POST['tilan_nimi'];
        $stmt = $conn->prepare("INSERT INTO tilat (tilan_nimi) VALUES (:tilan_nimi)");
        $stmt->bindParam(':tilan_nimi', $tilan_nimi);
        $stmt->execute();
        echo "<p>Tila '$tilan_nimi' lisätty.</p>";
        header("Location: " . $_SERVER['PHP_SELF']);
        exit; 
    }

    // Lisää varaaja
    if (isset($_POST['add_varaaja'])) {
        $varaaja_nimi = $_POST['varaaja_nimi'];
        $stmt = $conn->prepare("INSERT INTO varaajat (nimi) VALUES (:varaaja_nimi)");
        $stmt->bindParam(':varaaja_nimi', $varaaja_nimi);
        $stmt->execute();
        echo "<p>Varaaja '$varaaja_nimi' lisätty.</p>";
        header("Location: " . $_SERVER['PHP_SELF']);
        exit; 
    }

    // Lisää varaus
    if (isset($_POST['add_varaus'])) {
        $varaus_tila = $_POST['varaus_tila'];
        $varaus_varaaja = $_POST['varaus_varaaja'];
        $varauspaiva = $_POST['varauspaiva'];
        $stmt = $conn->prepare("INSERT INTO varaukset (tila, varaaja, varauspaiva) VALUES (:tila, :varaaja, :varauspaiva)");
        $stmt->bindParam(':tila', $varaus_tila);
        $stmt->bindParam(':varaaja', $varaus_varaaja);
        $stmt->bindParam(':varauspaiva', $varauspaiva);
        $stmt->execute();
        echo "<p>Varaus lisätty.</p>";
        header("Location: " . $_SERVER['PHP_SELF']);
        exit; 
    }
}
?>


</body>

</html>