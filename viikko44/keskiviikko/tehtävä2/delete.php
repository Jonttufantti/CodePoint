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

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['delete'])) {
        $id = $_POST['id'];

        // Tarkistetaan, onko kyseessä tila, varaaja vai varaus
        $stmt = $conn->prepare("SELECT * FROM tilat WHERE id = :id");
        $stmt->bindParam(':id', $id);
        $stmt->execute();

        if ($stmt->rowCount() > 0) {
            // Tarkistetaan, onko tilalla aktiivisia varauksia
            $checkReservations = $conn->prepare("SELECT * FROM varaukset WHERE tila = :id");
            $checkReservations->bindParam(':id', $id);
            $checkReservations->execute();

            if ($checkReservations->rowCount() > 0) {
                // Tila ei voi poistua, koska sillä on aktiivisia varauksia
                header("Location: index.php?error=Tilaa ei voi poistaa, koska sillä on aktiivisia varauksia.");
                exit;
            }

            // Poistetaan tila
            $stmt = $conn->prepare("DELETE FROM tilat WHERE id = :id");
            $stmt->bindParam(':id', $id);
            $stmt->execute();
            header("Location: index.php?message=Tila poistettu.");
            exit;
        }

        // Tarkistetaan varaajat
        $stmt = $conn->prepare("SELECT * FROM varaajat WHERE id = :id");
        $stmt->bindParam(':id', $id);
        $stmt->execute();

        if ($stmt->rowCount() > 0) {
            // Tarkistetaan, onko varaajalla aktiivisia varauksia
            $checkReservations = $conn->prepare("SELECT * FROM varaukset WHERE varaaja = :id");
            $checkReservations->bindParam(':id', $id);
            $checkReservations->execute();

            if ($checkReservations->rowCount() > 0) {
                // Varaaja ei voi poistua, koska sillä on aktiivisia varauksia
                header("Location: index.php?error=Varaajaa ei voi poistaa, koska hänellä on aktiivisia varauksia.");
                exit;
            }

            // Poistetaan varaaja
            $stmt = $conn->prepare("DELETE FROM varaajat WHERE id = :id");
            $stmt->bindParam(':id', $id);
            $stmt->execute();
            header("Location: index.php?message=Varaaja poistettu.");
            exit;
        }

        // Tarkistetaan varaukset
        $stmt = $conn->prepare("SELECT * FROM varaukset WHERE id = :id");
        $stmt->bindParam(':id', $id);
        $stmt->execute();
        if ($stmt->rowCount() > 0) {
            // Varaus löytyy, poistetaan
            $stmt = $conn->prepare("DELETE FROM varaukset WHERE id = :id");
            $stmt->bindParam(':id', $id);
            $stmt->execute();
            header("Location: index.php?message=Varaus poistettu.");
            exit;
        }
    }
}
?>
