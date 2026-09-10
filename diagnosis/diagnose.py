def diagnose(network, gateway, internet, dns, wifi_signal):
    """
    Classifies the most likely network problem
    using the collected diagnostic results.
    """

    # --------------------------------
    # 1. Local network problem
    # --------------------------------

    if network["local_ip"] is None:
        return {
            "problem": "Local network connection problem",
            "severity": "HIGH",
            "confidence": 95,
            "explanation": "No local IPv4 address was detected.",
            "recommendation": "Check your Wi-Fi or Ethernet connection."
        }

    # --------------------------------
    # 2. Gateway problem
    # --------------------------------

    if network["gateway"] is None:
        return {
            "problem": "Default gateway unavailable",
            "severity": "HIGH",
            "confidence": 95,
            "explanation": "A default gateway could not be detected.",
            "recommendation": "Check your router and network configuration."
        }

    if gateway["status"] == "failed":
        return {
            "problem": "Router/Gateway unreachable",
            "severity": "HIGH",
            "confidence": 90,
            "explanation": "Your computer cannot communicate with the local gateway.",
            "recommendation": "Check Wi-Fi/Ethernet connection and restart the router."
        }

    # --------------------------------
    # 3. Internet connectivity problem
    # --------------------------------

    if internet["status"] == "failed":
        return {
            "problem": "Internet connectivity problem",
            "severity": "HIGH",
            "confidence": 85,
            "explanation": "The gateway is reachable, but the external Internet host cannot be reached.",
            "recommendation": "Check your ISP connection or Internet service."
        }

    # --------------------------------
    # 4. DNS problem
    # --------------------------------

    if dns["status"] == "failed":
        return {
            "problem": "DNS resolution problem",
            "severity": "MEDIUM",
            "confidence": 90,
            "explanation": "Internet connectivity works, but domain-name resolution failed.",
            "recommendation": "Try changing the DNS server to 8.8.8.8 or 1.1.1.1."
        }

        # --------------------------------
    # 5. Weak Wi-Fi signal
    # --------------------------------

    if (
        wifi_signal is not None
        and wifi_signal < 40
    ):
        return {
            "problem": "Weak Wi-Fi signal",
            "severity": "MEDIUM",
            "confidence": 85,
            "explanation": f"Wi-Fi signal strength is only {wifi_signal}%.",
            "recommendation": "Move closer to the router or reduce obstacles/interference."
        }
    
    # --------------------------------
    # 6. Packet loss
    # --------------------------------

    if (
        internet["packet_loss"] is not None
        and internet["packet_loss"] > 20
    ):
        return {
            "problem": "High packet loss",
            "severity": "MEDIUM",
            "confidence": 90,
            "explanation": f"{internet['packet_loss']}% of packets were lost.",
            "recommendation": "Check Wi-Fi signal, network cables, router load, or ISP connection."
        }

    # --------------------------------
    # 7. High latency
    # --------------------------------

    if (
        internet["latency"] is not None
        and internet["latency"] > 100
    ):
        return {
            "problem": "High network latency",
            "severity": "MEDIUM",
            "confidence": 85,
            "explanation": f"Average Internet latency is {internet['latency']} ms.",
            "recommendation": "Check network congestion, Wi-Fi signal, or ISP routing."
        }

    # --------------------------------
    # 8. Healthy network
    # --------------------------------

    return {
        "problem": "Network is healthy",
        "severity": "LOW",
        "confidence": 95,
        "explanation": "Local network, gateway, Internet connectivity and DNS are working normally.",
        "recommendation": "No action required."
    }