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

    // Viestien näyttäminen
    if (isset($_GET['message'])) {
        echo "<p id='success-message' style='color: green;'>" . $_GET['message'] . "</p>";
    }

    if (isset($_GET['error'])) {
        echo "<p id='error-message' style='color: red;'>" . $_GET['error'] . "</p>";
    }

    function nayta_taulukko($conn, $sql, $otsikot)
    {
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
                
                echo '<td style="text-align: center;">
                    <form method="post" action="delete.php">
                        <input type="hidden" name="id" value="' . $row['id'] . '">
                        <button type="submit" name="delete">Poista</button>
                    </form>
                </td>';
                echo "</tr>";
            }
            echo "</table><br>";
        } catch (PDOException $e) {
            die("Query error: " . $e->getMessage());
        }
    }

    // Taulukot
    echo '<div class="taulukko-container">';

    echo '<div class="taulukko">';
    echo "<h2>Tilat</h2>";
    nayta_taulukko($conn, $sql_tilat, ["ID", "Tilan nimi", "Toiminnot"]);
    echo '</div>';

    echo '<div class="taulukko">';
    echo "<h2>Varaajat</h2>";
    nayta_taulukko($conn, $sql_varaajat, ["ID", "Nimi", "Toiminnot"]);
    echo '</div>';

    echo '<div class="taulukko">';
    echo "<h2>Varaukset</h2>";
    nayta_taulukko($conn, $sql_varaukset, ["ID", "Tila", "Varaaja", "Varauspäivä", "Toiminnot"]);
    echo '</div>';

    echo '</div>';

    

    ?>

    <script>
        // Aseta timeri viestien piilottamiseksi
        setTimeout(function () {
            let successMessage = document.querySelector('success-message');
            let errorMessage = document.querySelector('error-message');
            if (successMessage) {
                successMessage.style.display = 'none';
            }
            if (errorMessage) {
                errorMessage.style.display = 'none';
            }
        }, 2000); // 1000 ms = 1 second
    </script>

    <footer>
        <div class="footer-form">
            <div>
                <h3>Lisää uusi tila</h3>
                <form method="post" action="add.php">
                    <input type="text" name="tilan_nimi" placeholder="Tilan nimi" required>
                    <button type="submit" name="add_tila">Lisää tila</button>
                </form>
            </div>
            <div>
                <h3>Lisää uusi varaaja</h3>
                <form method="post" action="add.php">
                    <input type="text" name="varaaja_nimi" placeholder="Varaajan nimi" required>
                    <button type="submit" name="add_varaaja">Lisää varaaja</button>
                </form>
            </div>
            <div>
                <h3>Lisää uusi varaus</h3>
                <form method="post" action="add.php">
                    <select name="tila_id" required>
                        <option value="">Valitse tila</option>
                        <?php
                        // Hae tilat tietokannasta
                        $stmt = $conn->query("SELECT id, tilan_nimi FROM tilat");
                        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                            echo "<option value='" . $row['id'] . "'>" . $row['tilan_nimi'] . "</option>";
                        }
                        ?>
                    </select>
                    <select name="varaaja_id" required>
                        <option value="">Valitse varaaja</option>
                        <?php
                        // Hae varaajat tietokannasta
                        $stmt = $conn->query("SELECT id, nimi FROM varaajat");
                        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                            echo "<option value='" . $row['id'] . "'>" . $row['nimi'] . "</option>";
                        }
                        ?>
                    </select>
                    <input type="date" name="varauspaiva" required>
                    <button type="submit" name="add_varaus">Lisää varaus</button>
                </form>
            </div>
        </div>
    </footer>
</body>

</html>