import subprocess
import re
import json
from datetime import datetime

from diagnosis.diagnose import diagnose
from database.database import save_report


def get_network_info():
    """Gets the local IPv4 address and default gateway."""

    result = subprocess.run(
        ["ipconfig"],
        capture_output=True,
        text=True
    )

    output = result.stdout

    ip_match = re.search(
        r"IPv4 Address[.\s]*:\s*([\d.]+)",
        output
    )

    gateway_match = re.search(
        r"Default Gateway[.\s]*:\s*([\d.]+)",
        output
    )

    local_ip = ip_match.group(1) if ip_match else None
    gateway = gateway_match.group(1) if gateway_match else None

    return {
        "local_ip": local_ip,
        "gateway": gateway
    }


def gateway_test(gateway):
    """Checks whether the default gateway is reachable."""

    if gateway is None:
        return {
            "status": "failed",
            "message": "Default gateway not found."
        }

    result = subprocess.run(
        ["ping", "-n", "4", gateway],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return {
            "status": "success",
            "message": f"Gateway {gateway} is reachable."
        }

    return {
        "status": "failed",
        "message": f"Gateway {gateway} is unreachable."
    }


def ping_test(host="8.8.8.8"):
    """Checks Internet connectivity, latency and packet loss."""

    result = subprocess.run(
        ["ping", "-n", "4", host],
        capture_output=True,
        text=True
    )

    output = result.stdout

    if result.returncode != 0:
        return {
            "status": "failed",
            "latency": None,
            "packet_loss": None,
            "message": f"Unable to reach {host}."
        }

    loss_match = re.search(
        r"\((\d+)% loss\)",
        output
    )

    packet_loss = None

    if loss_match:
        packet_loss = int(loss_match.group(1))

    avg_match = re.search(
        r"Average = (\d+)ms",
        output
    )

    latency = None

    if avg_match:
        latency = int(avg_match.group(1))

    return {
        "status": "success",
        "latency": latency,
        "packet_loss": packet_loss,
        "message": f"{host} is reachable."
    }


def dns_test(host="google.com"):
    """
    Checks whether DNS name resolution is working.
    """

    result = subprocess.run(
        ["nslookup", host],
        capture_output=True,
        text=True
    )

    if result.returncode == 0 and "Address" in result.stdout:
        return {
            "status": "success",
            "message": f"DNS resolution for {host} is working."
        }

    return {
        "status": "failed",
        "message": f"DNS resolution for {host} failed."
    }

def traceroute_test(host="8.8.8.8"):
    """
    Traces the network path to the destination.
    """

    result = subprocess.run(
        ["tracert", "-h", "10", host],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return {
            "status": "success",
            "output": result.stdout
        }

    return {
        "status": "failed",
        "output": result.stdout
    }

def get_interface_info():
    """
    Gets basic network interface information.
    """

    result = subprocess.run(
        ["ipconfig", "/all"],
        capture_output=True,
        text=True
    )

    output = result.stdout

    interface = "Unknown"

    if "Wireless LAN adapter Wi-Fi" in output:
        interface = "Wi-Fi"
    elif "Ethernet adapter Ethernet" in output:
        interface = "Ethernet"

    return {
        "interface": interface
    }

def get_wifi_signal():
    """
    Gets Wi-Fi signal strength percentage.
    """

    result = subprocess.run(
        ["netsh", "wlan", "show", "interfaces"],
        capture_output=True,
        text=True
    )

    output = result.stdout

    signal_match = re.search(
        r"Signal\s*:\s*(\d+)%",
        output
    )

    if signal_match:
        return int(signal_match.group(1))

    return None

def create_diagnostic_report(
    network,
    interface_info,
    wifi_signal,
    gateway_result,
    internet_result,
    dns_result,
    trace_result,
    diagnosis
):
    """
    Creates a structured diagnostic report.
    """

    report = {
        "timestamp": datetime.now().isoformat(),

        "network": {
            "local_ip": network["local_ip"],
            "gateway": network["gateway"],
            "interface": interface_info["interface"],
            "wifi_signal": wifi_signal
        },

        "gateway_test": {
            "status": gateway_result["status"],
            "message": gateway_result["message"]
        },

        "internet_test": {
            "status": internet_result["status"],
            "latency": internet_result["latency"],
            "packet_loss": internet_result["packet_loss"],
            "message": internet_result["message"]
        },

        "dns_test": {
            "status": dns_result["status"],
            "message": dns_result["message"]
        },

        "traceroute": {
            "status": trace_result["status"],
            "output": trace_result["output"]
        },

        "diagnosis": {
            "problem": diagnosis["problem"],
            "severity": diagnosis["severity"],
            "confidence": diagnosis["confidence"],
            "explanation": diagnosis["explanation"],
            "recommendation": diagnosis["recommendation"]
        }
    }

    return report


if __name__ == "__main__":

    print("\n================================")
    print("       NETWORK TROUBLESHOOTER")
    print("================================")

    # 1. Get network information
    network = get_network_info()
    interface_info = get_interface_info()
    wifi_signal = get_wifi_signal()

    print("\n--- Network Information ---")
    print(f"Local IP    : {network['local_ip']}")
    print(f"Gateway     : {network['gateway']}")
    print(f"Interface   : {interface_info['interface']}")
    print(f"Wi-Fi Signal: {wifi_signal}%")

    # 2. Test gateway
    gateway_result = gateway_test(
        network["gateway"]
    )

    print("\n--- Gateway Test ---")
    print(f"Status      : {gateway_result['status']}")
    print(f"Message     : {gateway_result['message']}")

    # 3. Test Internet
    internet_result = ping_test()

    print("\n--- Internet Test ---")
    print(f"Status      : {internet_result['status']}")
    print(f"Latency     : {internet_result['latency']} ms")
    print(f"Packet Loss : {internet_result['packet_loss']}%")
    print(f"Message     : {internet_result['message']}")


    # 4. Test DNS
    dns_result = dns_test()

    print("\n--- DNS Test ---")
    print(f"Status      : {dns_result['status']}")
    print(f"Message     : {dns_result['message']}")

    # 5. Trace network path
    trace_result = traceroute_test()

    print("\n--- Traceroute ---")
    print(f"Status      : {trace_result['status']}")
    print(trace_result["output"])

    # 6. Diagnose the network
    diagnosis = diagnose(
    network,
    gateway_result,
    internet_result,
    dns_result,
    wifi_signal
    )

    print("\n================================")
    print("         DIAGNOSIS")
    print("================================")

    print(f"Problem        : {diagnosis['problem']}")
    print(f"Severity       : {diagnosis['severity']}")
    print(f"Confidence     : {diagnosis['confidence']}%")
    print(f"Explanation    : {diagnosis['explanation']}")
    print(f"Recommendation : {diagnosis['recommendation']}")

    print("\n================================")

    # 7. Create structured diagnostic report
    report = create_diagnostic_report(
        network,
        interface_info,
        wifi_signal,
        gateway_result,
        internet_result,
        dns_result,
        trace_result,
        diagnosis
    )

    save_report(report)
    print("\nDiagnostic report saved to database.")

    print("\n--- Structured Diagnostic Report ---")
    print(json.dumps(report, indent=4))
