async function runDiagnosis() {

    const status = document.getElementById("status");

    status.textContent = "Running network diagnosis...";

    try {

        const response = await fetch("/diagnose");

        if (!response.ok) {
            throw new Error("Failed to run diagnosis");
        }

        const data = await response.json();

        // Network information
        document.getElementById("local-ip").textContent =
            data.network.local_ip ?? "Not detected";

        document.getElementById("gateway").textContent =
            data.network.gateway ?? "Not detected";

        document.getElementById("interface").textContent =
            data.network.interface ?? "Unknown";

        document.getElementById("wifi-signal").textContent =
            data.network.wifi_signal !== null
                ? data.network.wifi_signal + "%"
                : "N/A";


        // Internet diagnostics
        document.getElementById("latency").textContent =
            data.internet_test.latency !== null
                ? data.internet_test.latency + " ms"
                : "N/A";

        document.getElementById("packet-loss").textContent =
            data.internet_test.packet_loss !== null
                ? data.internet_test.packet_loss + "%"
                : "N/A";

        document.getElementById("internet").textContent =
            data.internet_test.status;

        document.getElementById("dns").textContent =
            data.dns_test.status;


        // Diagnosis
        document.getElementById("problem").textContent =
            data.diagnosis.problem;

        const severity = data.diagnosis.severity;
        const confidence = data.diagnosis.confidence;

        const severityElement = document.getElementById("severity");
        const confidenceElement = document.getElementById("confidence");
        const confidenceFill = document.getElementById("confidence-fill");

        // Severity
        severityElement.textContent = severity;
        severityElement.className = "severity-badge";

        if (severity === "LOW") {
            severityElement.classList.add("severity-low");
        }
        else if (severity === "MEDIUM") {
            severityElement.classList.add("severity-medium");
        }
        else if (severity === "HIGH") {
            severityElement.classList.add("severity-high");
        }

        // Confidence
        confidenceElement.textContent = confidence + "%";
        confidenceFill.style.width = confidence + "%";

        // Explanation
        document.getElementById("explanation").textContent =
            data.diagnosis.explanation;

        // Recommendation
        document.getElementById("recommendation").textContent =
            data.diagnosis.recommendation;

        // Network topology status

        const pcNode = document.getElementById("pc-node");
        const routerNode = document.getElementById("router-node");
        const internetNode = document.getElementById("internet-node");

        const pcStatus = document.getElementById("pc-status");
        const routerStatus = document.getElementById("router-status");
        const internetStatus = document.getElementById("internet-status");


        // PC status
        pcNode.className = "network-node";

        if (data.network.local_ip) {
            pcNode.classList.add("node-healthy");
            pcStatus.textContent = "Connected";
        } else {
            pcNode.classList.add("node-critical");
            pcStatus.textContent = "Disconnected";
        }


        // Router status
        routerNode.className = "network-node";

        if (data.gateway_test.status === "success") {
            routerNode.classList.add("node-healthy");
            routerStatus.textContent = "Reachable";
        } else {
            routerNode.classList.add("node-critical");
            routerStatus.textContent = "Unreachable";
        }


        // Internet status
        internetNode.className = "network-node";

        if (data.internet_test.status === "success") {
            internetNode.classList.add("node-healthy");
            internetStatus.textContent = "Connected";
        } else {
            internetNode.classList.add("node-critical");
            internetStatus.textContent = "Disconnected";
        }

        // Connection health

        const connection = document.getElementById(
            "router-internet-connection"
        );

        const connectionStatus = document.getElementById(
            "connection-status"
        );

        const packetLoss = data.internet_test.packet_loss;
        const latency = data.internet_test.latency;

        connection.className = "connection";

        if (packetLoss !== null && packetLoss > 20) {

            connection.classList.add("connection-warning");

            connectionStatus.textContent =
                packetLoss + "% packet loss";

        }
        else if (latency !== null && latency > 100) {

            connection.classList.add("connection-warning");

            connectionStatus.textContent =
                latency + " ms latency";

        }
        else if (data.internet_test.status === "failed") {

            connection.classList.add("connection-critical");

            connectionStatus.textContent =
                "Connection failed";

        }
        else {

            connection.classList.add("connection-healthy");

            connectionStatus.textContent =
                "Stable";
        }


        // Overall status
        const status = document.getElementById("status");

        if (severity === "LOW") {
            status.textContent = "🟢 Network Healthy";
            status.className = "status-indicator status-healthy";
        }
        else if (severity === "MEDIUM") {
            status.textContent = "🟡 Network Warning";
            status.className = "status-indicator status-warning";
        }
        else if (severity === "HIGH") {
            status.textContent = "🔴 Network Critical";
            status.className = "status-indicator status-critical";
        }
    } catch (error) {

        console.error(error);

        status.textContent =
            "Unable to connect to the troubleshooting server.";
    }
}

async function loadHistory() {

    const historyBody = document.getElementById("history-body");

    try {

        const response = await fetch("/history");

        if (!response.ok) {
            throw new Error("Failed to load history");
        }

        const data = await response.json();

        historyBody.innerHTML = "";

        if (data.history.length === 0) {

            historyBody.innerHTML = `
                <tr>
                    <td colspan="7">No history available</td>
                </tr>
            `;

            return;
        }

        data.history.forEach(record => {

            const row = document.createElement("tr");

            let severityClass = "";

            if (record.severity === "LOW") {
                severityClass = "history-low";
            }
            else if (record.severity === "MEDIUM") {
                severityClass = "history-medium";
            }
            else if (record.severity === "HIGH") {
                severityClass = "history-high";
            }

            row.innerHTML = `
                <td>${record.id}</td>
                <td>${record.timestamp}</td>
                <td>${record.diagnosis}</td>
                <td>
                    <span class="history-severity ${severityClass}">
                        ${record.severity}
                    </span>
                </td>
                <td>${record.confidence}%</td>
                <td>${record.latency ?? "N/A"} ms</td>
                <td>${record.packet_loss ?? "N/A"}%</td>
            `;

            historyBody.appendChild(row);
        });

    } catch (error) {

        console.error(error);

        historyBody.innerHTML = `
            <tr>
                <td colspan="7">
                    Unable to load diagnostic history
                </td>
            </tr>
        `;
    }
}

loadHistory();