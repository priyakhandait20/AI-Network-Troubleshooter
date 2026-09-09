import subprocess
import re


def ping_test(host="8.8.8.8"):
    """
    Checks connectivity, latency and packet loss.
    """

    result = subprocess.run(
        ["ping", "-n", "4", host],
        capture_output=True,
        text=True
    )

    output = result.stdout

    # Check whether ping was successful
    if result.returncode != 0:
        return {
            "status": "failed",
            "latency": None,
            "packet_loss": None,
            "message": f"Unable to reach {host}."
        }

    # Extract packet loss
    loss_match = re.search(r"\((\d+)% loss\)", output)

    packet_loss = None

    if loss_match:
        packet_loss = int(loss_match.group(1))

    # Extract average latency
    avg_match = re.search(r"Average = (\d+)ms", output)

    latency = None

    if avg_match:
        latency = int(avg_match.group(1))

    return {
        "status": "success",
        "latency": latency,
        "packet_loss": packet_loss,
        "message": f"{host} is reachable."
    }


if __name__ == "__main__":

    result = ping_test()

    print("=== Network Diagnostic ===")
    print(f"Status      : {result['status']}")
    print(f"Latency     : {result['latency']} ms")
    print(f"Packet Loss : {result['packet_loss']}%")
    print(f"Message     : {result['message']}")