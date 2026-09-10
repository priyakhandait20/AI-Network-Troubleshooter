import sqlite3


DATABASE_NAME = "database/network_history.db"


def create_database():
    """
    Creates the network history database and table.
    """

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS network_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            local_ip TEXT,
            gateway TEXT,
            interface TEXT,
            wifi_signal INTEGER,
            latency INTEGER,
            packet_loss INTEGER,
            dns_status TEXT,
            internet_status TEXT,
            diagnosis TEXT,
            severity TEXT,
            confidence INTEGER,
            explanation TEXT,
            recommendation TEXT
        )
    """)

    connection.commit()
    connection.close()

def save_report(report):
    """
    Saves a diagnostic report into the database.
    """

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO network_history (
            timestamp,
            local_ip,
            gateway,
            interface,
            wifi_signal,
            latency,
            packet_loss,
            dns_status,
            internet_status,
            diagnosis,
            severity,
            confidence,
            explanation,
            recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report["timestamp"],
        report["network"]["local_ip"],
        report["network"]["gateway"],
        report["network"]["interface"],
        report["network"]["wifi_signal"],
        report["internet_test"]["latency"],
        report["internet_test"]["packet_loss"],
        report["dns_test"]["status"],
        report["internet_test"]["status"],
        report["diagnosis"]["problem"],
        report["diagnosis"]["severity"],
        report["diagnosis"]["confidence"],
        report["diagnosis"]["explanation"],
        report["diagnosis"]["recommendation"]
    ))

    connection.commit()
    connection.close()

def get_history():
    """
    Retrieves all previous diagnostic reports.
    """

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            diagnosis,
            severity,
            confidence,
            latency,
            packet_loss
        FROM network_history
        ORDER BY id DESC
    """)

    history = cursor.fetchall()

    connection.close()

    return history

def get_statistics():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Total number of diagnostic runs
    cursor.execute("""
        SELECT COUNT(*)
        FROM network_history
    """)
    total = cursor.fetchone()[0]

    # Number of healthy runs
    cursor.execute("""
        SELECT COUNT(*)
        FROM network_history
        WHERE severity = 'LOW'
    """)
    healthy = cursor.fetchone()[0]

    # Number of warnings
    cursor.execute("""
        SELECT COUNT(*)
        FROM network_history
        WHERE severity = 'MEDIUM'
    """)
    warnings = cursor.fetchone()[0]

    # Number of critical issues
    cursor.execute("""
        SELECT COUNT(*)
        FROM network_history
        WHERE severity = 'HIGH'
    """)
    critical = cursor.fetchone()[0]

    # Average latency
    cursor.execute("""
        SELECT AVG(latency)
        FROM network_history
        WHERE latency IS NOT NULL
    """)
    average_latency = cursor.fetchone()[0]

    # Average packet loss
    cursor.execute("""
        SELECT AVG(packet_loss)
        FROM network_history
        WHERE packet_loss IS NOT NULL
    """)
    average_packet_loss = cursor.fetchone()[0]

    # Most common diagnosis
    cursor.execute("""
        SELECT diagnosis, COUNT(*) AS occurrences
        FROM network_history
        GROUP BY diagnosis
        ORDER BY occurrences DESC
        LIMIT 1
    """)
    most_common = cursor.fetchone()

    connection.close()

    return {
        "total": total,
        "healthy": healthy,
        "warnings": warnings,
        "critical": critical,
        "average_latency": round(average_latency, 2)
            if average_latency is not None else None,
        "average_packet_loss": round(average_packet_loss, 2)
            if average_packet_loss is not None else None,
        "most_common_problem": most_common[0]
            if most_common else None
    }

if __name__ == "__main__":
    create_database()

    statistics = get_statistics()

    print("\n===== NETWORK STATISTICS =====")
    print("Total Diagnoses      :", statistics["total"])
    print("Healthy Runs         :", statistics["healthy"])
    print("Warnings             :", statistics["warnings"])
    print("Critical Issues      :", statistics["critical"])
    print("Average Latency      :", statistics["average_latency"], "ms")
    print("Average Packet Loss  :", statistics["average_packet_loss"], "%")
    print("Most Common Problem  :", statistics["most_common_problem"])
