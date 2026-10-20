
import re


def analyze_logs(content):
    lines = content.splitlines()

    findings = []
    errors = 0
    warnings = 0
    suspicious_events = 0

    for line_number, line in enumerate(lines, start=1):
        text = line.strip()

        if not text:
            continue

        level = "INFO"
        classification = "General Event"
        suspicious = False

        if re.search(r"\b(ERROR|CRITICAL|FATAL|EXCEPTION)\b", text, re.I):
            level = "ERROR"
            classification = "Error"
            errors += 1

        elif re.search(r"\b(WARN|WARNING)\b", text, re.I):
            level = "WARNING"
            classification = "Warning"
            warnings += 1

        if re.search(
            r"failed login|login failed|unauthorized|"
            r"authentication failure|invalid password|"
            r"brute.?force|access denied",
            text,
            re.I
        ):
            suspicious = True
            classification = "Suspicious Activity"
            suspicious_events += 1

        findings.append({
            "line": line_number,
            "level": level,
            "message": text,
            "classification": classification,
            "suspicious": suspicious
        })

    return {
        "total_events": len(findings),
        "errors": errors,
        "warnings": warnings,
        "suspicious_events": suspicious_events,
        "findings": findings
    }
