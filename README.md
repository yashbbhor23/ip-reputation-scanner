# IP Reputation Scanner

A Python-based security utility for checking the reputation of IPv4 and IPv6 addresses using the AbuseIPDB API.

The tool accepts a text file containing IP addresses, validates the entries, queries AbuseIPDB, displays the results in the terminal, and generates a CSV report.

## Features

- IPv4 and IPv6 address validation
- Duplicate IP detection
- Ignores blank lines and comments in the input file
- AbuseIPDB reputation lookup
- Abuse Confidence Score
- Country and ISP information
- Usage type
- Total abuse reports
- Last reported date
- Whitelist status
- Tor status
- Basic risk assessment
- CSV report generation
- API error handling
- Request timeout handling
- Delay between API requests

## Requirements

- Python 3
- AbuseIPDB API key
- `requests`

## Installation

Clone the repository:

```bash
git clone https://github.com/yashbbhor23/ip-reputation-scanner.git
cd ip-reputation-scanner
