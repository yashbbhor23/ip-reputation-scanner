#!/usr/bin/env python3

import requests
import ipaddress
import csv
import os
import sys
import time


# ============================================================
# CONFIGURATION
# ============================================================

# AbuseIPDB API key is read from the environment.
# Never hard-code API keys in this source file.
API_KEY = os.getenv("ABUSEIPDB_API_KEY")


# Number of days to look back for AbuseIPDB reports
MAX_AGE_DAYS = 90

# Output CSV file
OUTPUT_FILE = "abuseipdb_report.csv"

# AbuseIPDB API endpoint
API_URL = "https://api.abuseipdb.com/api/v2/check"


# ============================================================
# CHECK API KEY
# ============================================================

if not API_KEY:
    print("\n[-] ERROR: AbuseIPDB API key is not configured.")
    print("[*] Set the ABUSEIPDB_API_KEY environment variable.")
    print('    Example: export ABUSEIPDB_API_KEY="YOUR_API_KEY"\n')
    sys.exit(1)


# ============================================================
# READ IPs FROM TXT FILE
# ============================================================

def read_ips(filename):

    ips = []
    invalid_ips = []

    try:
        with open(filename, "r", encoding="utf-8") as file:

            for line in file:

                line = line.strip()

                # Ignore blank lines
                if not line:
                    continue

                # Ignore comments
                if line.startswith("#"):
                    continue

                # Remove accidental spaces
                line = line.strip()

                try:
                    ipaddress.ip_address(line)

                    if line not in ips:
                        ips.append(line)

                except ValueError:
                    invalid_ips.append(line)

    except FileNotFoundError:
        print(f"\n[-] File not found: {filename}")
        sys.exit(1)

    except PermissionError:
        print(f"\n[-] Permission denied: {filename}")
        sys.exit(1)

    return ips, invalid_ips


# ============================================================
# DETERMINE ASSESSMENT
# ============================================================

def get_assessment(score):

    if score == 0:
        return "No Abuse Reports"

    elif score <= 25:
        return "Low"

    elif score <= 50:
        return "Medium"

    elif score <= 75:
        return "High"

    else:
        return "Very High"


# ============================================================
# CHECK IP AGAINST ABUSEIPDB
# ============================================================

def check_ip(ip):

    headers = {
        "Accept": "application/json",
        "Key": API_KEY
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": MAX_AGE_DAYS
    }

    try:

        response = requests.get(
            API_URL,
            headers=headers,
            params=params,
            timeout=20
        )

        # API error
        if response.status_code != 200:

            try:
                error_data = response.json()

                errors = error_data.get("errors", [])

                if errors:
                    error_message = errors[0].get(
                        "detail",
                        "Unknown API error"
                    )
                else:
                    error_message = "Unknown API error"

            except Exception:
                error_message = response.text

            return {
                "IP": ip,
                "Abuse Confidence Score": "N/A",
                "Country": "N/A",
                "ISP": "N/A",
                "Usage Type": "N/A",
                "Total Reports": "N/A",
                "Last Reported": "N/A",
                "Whitelisted": "N/A",
                "Tor": "N/A",
                "Assessment": "API Error",
                "Status": "Failed",
                "Error": error_message
            }

        # Parse API response
        data = response.json().get("data", {})

        score = data.get(
            "abuseConfidenceScore",
            0
        )

        assessment = get_assessment(score)

        return {
            "IP": data.get("ipAddress", ip),
            "Abuse Confidence Score": score,
            "Country": data.get("countryName", "N/A"),
            "ISP": data.get("isp", "N/A"),
            "Usage Type": data.get("usageType", "N/A"),
            "Total Reports": data.get("totalReports", 0),
            "Last Reported": data.get(
                "lastReportedAt",
                "Never"
            ),
            "Whitelisted": data.get(
                "isWhitelisted",
                "N/A"
            ),
            "Tor": data.get(
                "isTor",
                "N/A"
            ),
            "Assessment": assessment,
            "Status": "Success",
            "Error": ""
        }

    except requests.exceptions.Timeout:

        return {
            "IP": ip,
            "Abuse Confidence Score": "N/A",
            "Country": "N/A",
            "ISP": "N/A",
            "Usage Type": "N/A",
            "Total Reports": "N/A",
            "Last Reported": "N/A",
            "Whitelisted": "N/A",
            "Tor": "N/A",
            "Assessment": "Request Timeout",
            "Status": "Failed",
            "Error": "Request timed out"
        }

    except requests.exceptions.RequestException as e:

        return {
            "IP": ip,
            "Abuse Confidence Score": "N/A",
            "Country": "N/A",
            "ISP": "N/A",
            "Usage Type": "N/A",
            "Total Reports": "N/A",
            "Last Reported": "N/A",
            "Whitelisted": "N/A",
            "Tor": "N/A",
            "Assessment": "Connection Error",
            "Status": "Failed",
            "Error": str(e)
        }


# ============================================================
# PRINT RESULT
# ============================================================

def print_result(result):

    print("\n" + "-" * 70)

    print(f"IP                    : {result['IP']}")
    print(
        f"Abuse Confidence Score: "
        f"{result['Abuse Confidence Score']}%"
    )
    print(f"Country               : {result['Country']}")
    print(f"ISP                   : {result['ISP']}")
    print(f"Usage Type            : {result['Usage Type']}")
    print(f"Total Reports         : {result['Total Reports']}")
    print(f"Last Reported         : {result['Last Reported']}")
    print(f"Whitelisted           : {result['Whitelisted']}")
    print(f"Tor                   : {result['Tor']}")
    print(f"Assessment            : {result['Assessment']}")

    if result["Status"] == "Failed":
        print(f"Error                 : {result['Error']}")


# ============================================================
# SAVE CSV REPORT
# ============================================================

def save_csv(results):

    fieldnames = [
        "IP",
        "Abuse Confidence Score",
        "Country",
        "ISP",
        "Usage Type",
        "Total Reports",
        "Last Reported",
        "Whitelisted",
        "Tor",
        "Assessment",
        "Status",
        "Error"
    ]

    try:

        with open(
            OUTPUT_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()

            for result in results:
                writer.writerow(result)

        return True

    except Exception as e:

        print(f"\n[-] Could not create CSV: {e}")
        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("             ABUSEIPDB IP REPUTATION CHECKER")
    print("=" * 70)

    print("\n[*] Report lookback period:", MAX_AGE_DAYS, "days")

    # --------------------------------------------------------
    # Ask for TXT file
    # --------------------------------------------------------

    filename = input(
        "\nEnter TXT file path containing IP addresses: "
    ).strip()

    # Remove quotes if user pastes a quoted path
    filename = filename.strip('"').strip("'")

    if not filename:

        print("\n[-] No file specified.")
        sys.exit(1)

    # --------------------------------------------------------
    # Read IPs
    # --------------------------------------------------------

    ips, invalid_ips = read_ips(filename)

    print(f"\n[+] Valid IP addresses found : {len(ips)}")

    if invalid_ips:

        print(
            f"[!] Invalid entries skipped   : "
            f"{len(invalid_ips)}"
        )

        for invalid in invalid_ips:
            print(f"    - {invalid}")

    if not ips:

        print("\n[-] No valid IP addresses found.")
        sys.exit(1)

    # --------------------------------------------------------
    # Check IPs
    # --------------------------------------------------------

    results = []

    print("\n[*] Starting AbuseIPDB reputation checks...")

    for index, ip in enumerate(ips, start=1):

        print(
            f"\n[{index}/{len(ips)}] Checking {ip}..."
        )

        result = check_ip(ip)

        results.append(result)

        print_result(result)

        # Small delay between requests
        # Helps avoid unnecessarily rapid API requests
        if index < len(ips):
            time.sleep(1)

    # --------------------------------------------------------
    # Save CSV
    # --------------------------------------------------------

    print("\n" + "=" * 70)

    if save_csv(results):

        print(
            f"[+] CSV report created: "
            f"{os.path.abspath(OUTPUT_FILE)}"
        )

    else:

        print("[-] CSV report could not be created.")

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    successful = sum(
        1 for result in results
        if result["Status"] == "Success"
    )

    failed = len(results) - successful

    print("\n" + "=" * 70)
    print("                         SUMMARY")
    print("=" * 70)

    print(f"Total IPs checked : {len(results)}")
    print(f"Successful        : {successful}")
    print(f"Failed            : {failed}")

    print("\n[+] Assessment completed.")


# ============================================================
# START SCRIPT
# ============================================================

if __name__ == "__main__":
    main()
