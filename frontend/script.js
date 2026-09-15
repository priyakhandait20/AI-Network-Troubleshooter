let latencyChart = null;
let packetLossChart = null;
let diagnosisChart = null;

/* =========================
   Run Network Diagnosis
========================= */

async function runDiagnosis() {

    const status = document.getElementById("status");

    status.textContent = "Running network diagnosis...";
    status.className = "status-indicator";

    try {

        const response = await fetch("/diagnose");

        if (!response.ok) {
            throw new Error("Failed to run diagnosis");
        }

        const data = await response.json();


        /* =========================
           Network Information
        ========================= */

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


        /* =========================
           Internet Diagnostics
        ========================= */

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


        /* =========================
           Diagnosis
        ========================= */

        const primaryDiagnosis = data.diagnosis.primary;

        document.getElementById("problem").textContent =
            primaryDiagnosis.problem;

        const severity = primaryDiagnosis.severity;
        const confidence = primaryDiagnosis.confidence;

        const severityElement =
            document.getElementById("severity");

        const confidenceElement =
            document.getElementById("confidence");

        const confidenceFill =
            document.getElementById("confidence-fill");


        /* Severity */

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


        /* Confidence */

        confidenceElement.textContent =
            confidence + "%";

        confidenceFill.style.width =
            confidence + "%";


        /* Explanation */

        document.getElementById("explanation").textContent =
            primaryDiagnosis.explanation;


        /* Recommendation */

        document.getElementById("recommendation").textContent =
            primaryDiagnosis.recommendation;


        /* =========================
           Overall Status
        ========================= */

        if (severity === "LOW") {

            status.textContent = "🟢 Network Healthy";
            status.className =
                "status-indicator status-healthy";

        }
        else if (severity === "MEDIUM") {

            status.textContent = "🟡 Network Warning";
            status.className =
                "status-indicator status-warning";

        }
        else if (severity === "HIGH") {

            status.textContent = "🔴 Network Critical";
            status.className =
                "status-indicator status-critical";
        }


        /* =========================
           Network Topology
        ========================= */

        const pcNode =
            document.getElementById("pc-node");

        const routerNode =
            document.getElementById("router-node");

        const internetNode =
            document.getElementById("internet-node");

        const pcStatus =
            document.getElementById("pc-status");

        const routerStatus =
            document.getElementById("router-status");

        const internetStatus =
            document.getElementById("internet-status");


        /* PC */

        pcNode.className = "network-node";

        if (data.network.local_ip) {

            pcNode.classList.add("node-healthy");
            pcStatus.textContent = "Connected";

        }
        else {

            pcNode.classList.add("node-critical");
            pcStatus.textContent = "Disconnected";
        }


        /* Router */

        routerNode.className = "network-node";

        if (data.gateway_test.status === "success") {

            routerNode.classList.add("node-healthy");
            routerStatus.textContent = "Reachable";

        }
        else {

            routerNode.classList.add("node-critical");
            routerStatus.textContent = "Unreachable";
        }


        /* Internet */

        internetNode.className = "network-node";

        if (data.internet_test.status === "success") {

            internetNode.classList.add("node-healthy");
            internetStatus.textContent = "Connected";

        }
        else {

            internetNode.classList.add("node-critical");
            internetStatus.textContent = "Disconnected";
        }


        /* =========================
           Connection Health
        ========================= */

        const connection =
            document.getElementById(
                "router-internet-connection"
            );

        const connectionStatus =
            document.getElementById(
                "connection-status"
            );

        const packetLoss =
            data.internet_test.packet_loss;

        const latency =
            data.internet_test.latency;


        connection.className = "connection";


        if (packetLoss !== null && packetLoss > 20) {

            connection.classList.add(
                "connection-warning"
            );

            connectionStatus.textContent =
                packetLoss + "% packet loss";

        }
        else if (latency !== null && latency > 100) {

            connection.classList.add(
                "connection-warning"
            );

            connectionStatus.textContent =
                latency + " ms latency";

        }
        else if (
            data.internet_test.status === "failed"
        ) {

            connection.classList.add(
                "connection-critical"
            );

            connectionStatus.textContent =
                "Connection failed";

        }
        else {

            connection.classList.add(
                "connection-healthy"
            );

            connectionStatus.textContent =
                "Stable";
        }


        /* =========================
           Refresh History
        ========================= */

        await loadHistory();


        /* =========================
           Refresh Statistics
        ========================= */

        await loadStatistics();

        /* =========================
           Refresh Charts
        ========================= */

        await loadCharts();


    } catch (error) {

        console.error(error);

        status.textContent =
            "Unable to connect to the troubleshooting server.";

        status.className =
            "status-indicator status-critical";
    }
}


/* =========================
   Load Statistics
========================= */

async function loadStatistics() {

    try {

        const response =
            await fetch("/statistics");

        if (!response.ok) {
            throw new Error(
                "Failed to load statistics"
            );
        }

        const data =
            await response.json();


        document.getElementById("total-runs").textContent =
            data.total;

        document.getElementById("healthy-runs").textContent =
            data.healthy;

        document.getElementById("warning-runs").textContent =
            data.warnings;

        document.getElementById("critical-runs").textContent =
            data.critical;


        document.getElementById("average-latency").textContent =
            data.average_latency !== null
                ? data.average_latency + " ms"
                : "N/A";


        document.getElementById("average-packet-loss").textContent =
            data.average_packet_loss !== null
                ? data.average_packet_loss + "%"
                : "N/A";


        document.getElementById("most-common-problem").textContent =
            data.most_common_problem ?? "N/A";


    } catch (error) {

        console.error(
            "Statistics error:",
            error
        );
    }
}


/* =========================
   Load Analytics Charts
========================= */

async function loadCharts() {

    try {

        const response = await fetch("/history");

        if (!response.ok) {
            throw new Error("Failed to load chart data");
        }

        const data = await response.json();

        const history = [...data.history].reverse();

        const labels = history.map(record => {
            return "#" + record.id;
        });

        const latencyData = history.map(record => {
            return record.latency;
        });

        const packetLossData = history.map(record => {
            return record.packet_loss;
        });


        /* =========================
           Latency Chart
        ========================= */

        const latencyContext =
            document.getElementById("latency-chart");

        if (latencyChart) {
            latencyChart.destroy();
        }

        latencyChart = new Chart(latencyContext, {

            type: "line",

            data: {
                labels: labels,

                datasets: [{
                    label: "Latency (ms)",
                    data: latencyData,

                    borderWidth: 2,

                    tension: 0.3,

                    spanGaps: true
                }]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                scales: {
                    y: {
                        beginAtZero: true,

                        title: {
                            display: true,
                            text: "Milliseconds"
                        }
                    },

                    x: {
                        title: {
                            display: true,
                            text: "Diagnostic Run"
                        }
                    }
                }
            }
        });


        /* =========================
           Packet Loss Chart
        ========================= */

        const packetLossContext =
            document.getElementById("packet-loss-chart");

        if (packetLossChart) {
            packetLossChart.destroy();
        }

        packetLossChart = new Chart(
            packetLossContext,
            {

                type: "line",

                data: {
                    labels: labels,

                    datasets: [{
                        label: "Packet Loss (%)",
                        data: packetLossData,

                        borderWidth: 2,

                        tension: 0.3,

                        spanGaps: true
                    }]
                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    scales: {
                        y: {
                            beginAtZero: true,

                            title: {
                                display: true,
                                text: "Packet Loss (%)"
                            }
                        },

                        x: {
                            title: {
                                display: true,
                                text: "Diagnostic Run"
                            }
                        }
                    }
                }
            }
        );

        // Diagnosis distribution
        const diagnosisCounts = {};

        history.forEach(record => {
            const diagnosis = record.diagnosis;

            if (diagnosisCounts[diagnosis]) {
                diagnosisCounts[diagnosis]++;
            } else {
                diagnosisCounts[diagnosis] = 1;
            }
        });

        const diagnosisLabels = Object.keys(diagnosisCounts);
        const diagnosisValues = Object.values(diagnosisCounts);

        const diagnosisContext = document.getElementById("diagnosis-chart");

        if (diagnosisChart) {
            diagnosisChart.destroy();
        }

        diagnosisChart = new Chart(diagnosisContext, {
            type: "bar",
            data: {
                labels: diagnosisLabels,
                datasets: [{
                    label: "Occurrences",
                    data: diagnosisValues,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        },
                        title: {
                            display: true,
                            text: "Number of Runs"
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: "Diagnosis"
                        }
                    }
                }
            }
        });

    } catch (error) {

        console.error(
            "Chart error:",
            error
        );
    }
}



/* =========================
   Load Diagnostic History
========================= */

async function loadHistory() {

    const historyBody =
        document.getElementById(
            "history-body"
        );

    try {

        const response =
            await fetch("/history");

        if (!response.ok) {
            throw new Error(
                "Failed to load history"
            );
        }

        const data =
            await response.json();


        historyBody.innerHTML = "";


        if (data.history.length === 0) {

            historyBody.innerHTML = `
                <tr>
                    <td colspan="7">
                        No history available
                    </td>
                </tr>
            `;

            return;
        }


        data.history.forEach(record => {

            const row =
                document.createElement("tr");


            let severityClass = "";


            if (record.severity === "LOW") {

                severityClass =
                    "history-low";

            }
            else if (record.severity === "MEDIUM") {

                severityClass =
                    "history-medium";

            }
            else if (record.severity === "HIGH") {

                severityClass =
                    "history-high";
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

                <td>
                    ${record.latency ?? "N/A"} ms
                </td>

                <td>
                    ${record.packet_loss ?? "N/A"}%
                </td>
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


/* =========================
   Initial Page Load
========================= */

loadHistory();
loadStatistics();
loadCharts();