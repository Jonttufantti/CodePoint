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
    echo '</div>';

    echo '<div class="taulukko">';
    echo "<h2>Varaajat</h2>";
    nayta_taulukko($conn, $sql_varaajat, ["ID", "Nimi"]);
    echo '</div>';

    echo '<div class="taulukko">';
    echo "<h2>Varaukset</h2>";
    nayta_taulukko($conn, $sql_varaukset, ["ID", "Tila ID", "Varaaja ID", "Varauspäivä"]);
    echo '</div>';
    
    echo '</div>';
    ?>

</body>

</html>