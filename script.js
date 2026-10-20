
const scanForm = document.getElementById("scanForm");
const logFile = document.getElementById("logFile");
const scanButton = document.getElementById("scanButton");
const scanStatus = document.getElementById("scanStatus");
const findingsBody = document.getElementById("findingsBody");
const downloadButton = document.getElementById("downloadButton");

let latestReport = null;

scanForm?.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = logFile?.files?.[0];

    if (!file) {
        scanStatus.textContent = "Please choose a .log or .txt file.";
        return;
    }

    if (!/\.(log|txt)$/i.test(file.name)) {
        scanStatus.textContent = "Only .log and .txt files are allowed.";
        return;
    }

    if (file.size > 2 * 1024 * 1024) {
        scanStatus.textContent = "File exceeds the 2 MB limit.";
        return;
    }

    const formData = new FormData();
    formData.append("logfile", file);

    scanButton.disabled = true;
    scanStatus.textContent = "Analyzing log file...";

    try {
        const response = await fetch("/api/scan", {
            method: "POST",
            body: formData
        });

        const report = await response.json();

        if (!response.ok) {
            throw new Error(report.error || "Scan failed.");
        }

        latestReport = report;
        downloadButton.disabled = false;

        document.getElementById("totalEvents").textContent = report.total_events;
        document.getElementById("errorCount").textContent = report.errors;
        document.getElementById("warningCount").textContent = report.warnings;
        document.getElementById("threatCount").textContent = report.suspicious_events;

        findingsBody.replaceChildren();

        if (report.findings.length === 0) {
            const row = findingsBody.insertRow();
            const cell = row.insertCell();
            cell.colSpan = 3;
            cell.textContent = "No findings detected.";
        } else {
            report.findings.forEach((finding) => {
                const row = findingsBody.insertRow();

                const levelCell = row.insertCell();
                levelCell.textContent = finding.level;

                const messageCell = row.insertCell();
                messageCell.textContent = finding.message;

                const classificationCell = row.insertCell();
                classificationCell.textContent = finding.classification;
            });
        }

        scanStatus.textContent =
            `Scan complete: ${report.total_events} events analyzed.`;

        if (typeof updateEventChart === "function") {
            updateEventChart(report);
        }
    } catch (error) {
        scanStatus.textContent = `Error: ${error.message}`;
    } finally {
        scanButton.disabled = false;
    }
});

downloadButton?.addEventListener("click", () => {
    if (!latestReport) {
        scanStatus.textContent = "Run a scan before exporting a report.";
        return;
    }

    const blob = new Blob(
        [JSON.stringify(latestReport, null, 2)],
        { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "logsentry-report.json";
    link.click();
    URL.revokeObjectURL(url);
});
