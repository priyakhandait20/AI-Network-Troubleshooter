from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from diagnostics.network_tests import (
    get_network_info,
    get_interface_info,
    get_wifi_signal,
    gateway_test,
    ping_test,
    dns_test,
    traceroute_test,
    create_diagnostic_report,
)

from diagnosis.diagnose import diagnose
from database.database import get_history, save_report, get_statistics


app = FastAPI(
    title="AI Network Troubleshooter",
    description="Network diagnostics and troubleshooting API",
    version="1.0"
)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/diagnose")
def run_diagnosis():

    # 1. Get network information
    network = get_network_info()

    # 2. Get interface information
    interface_info = get_interface_info()

    # 3. Get Wi-Fi signal
    wifi_signal = get_wifi_signal()

    # 4. Test gateway
    gateway_result = gateway_test(network["gateway"])

    # 5. Test Internet
    internet_result = ping_test()

    # 6. Test DNS
    dns_result = dns_test()

    # 7. Traceroute
    trace_result = traceroute_test()

    # 8. Diagnose the network
    diagnosis = diagnose(
        network,
        gateway_result,
        internet_result,
        dns_result,
        wifi_signal
    )

    # 9. Create structured report
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

    return report

@app.get("/history")
def history():
    records = get_history()

    return {
        "count": len(records),
        "history": [
            {
                "id": row[0],
                "timestamp": row[1],
                "diagnosis": row[2],
                "severity": row[3],
                "confidence": row[4],
                "latency": row[5],
                "packet_loss": row[6]
            }
            for row in records
        ]
    }

@app.get("/statistics")
def statistics():
    return get_statistics()