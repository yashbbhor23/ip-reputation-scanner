IP Reputation Scanner - Usage Guide

This guide explains how to install, configure, and use the IP Reputation Scanner step by step. The scanner uses the AbuseIPDB API to check the reputation of IPv4 and IPv6 addresses and generates a CSV report containing the results.

1. Clone the Repository

Open a terminal and clone the repository:

git clone https://github.com/yashbbhor23/ip-reputation-scanner.git

Move into the project directory:

cd ip-reputation-scanner

Verify the project files:

ls

2. Install the Required Dependencies

Install the required Python package using:

python3 -m pip install -r requirements.txt

The project currently requires:

requests

3. Configure the AbuseIPDB API Key

The scanner requires an AbuseIPDB API key to perform reputation checks.

After creating an AbuseIPDB account, obtain your API key from: Account → My API

Do not place the API key directly inside the Python source code.

export ABUSEIPDB_API_KEY="YOUR_API_KEY"

Replace YOUR_API_KEY with your actual AbuseIPDB API key.

Never commit your API key to GitHub or share it publicly.

4. Verify the API Key

Before running the scanner, verify that the environment variable is configured:

if [ -n "$ABUSEIPDB_API_KEY" ]; then echo "API key configured"; else echo "API key missing"; fi

Expected output:

API key configured

If you see API key missing, configure the API key again.

5. Prepare the IP Address List

Create a text file containing the IP addresses you want to check.

For example:

nano ips.txt

Add one IP address per line:

8.8.8.8
1.1.1.1
8.8.4.4

The scanner supports IPv4 addresses, IPv6 addresses, blank lines, comments beginning with #, and duplicate IP addresses.

Example with comments:

# Public DNS servers

8.8.8.8
1.1.1.1

# Another public IP
8.8.4.4

6. Run the Scanner

Run the scanner from the project directory:

python3 abuseipdb_checker.py

The scanner will prompt you to provide the path to your IP list:

Enter path to IP list:

Enter:

ips.txt

7. Using a Different IP List File

You are not required to use the filename ips.txt. You can provide any valid filename or path.

Enter path to IP list: targets.txt

Or provide a full path:

Enter path to IP list: /home/user/Documents/targets.txt

8. Scanner Processing

After providing the IP list, the scanner will:

1. Read the IP addresses from the file.
2. Ignore blank lines.
3. Ignore comments beginning with #.
4. Validate the IP addresses.
5. Remove duplicate IP addresses.
6. Query AbuseIPDB for each valid IP address.
7. Display the results in the terminal.
8. Generate a CSV report.

9. Review the Terminal Output

The scanner displays reputation information while processing the IP addresses.

Results include IP Address, Abuse Confidence Score, Country, ISP, Usage Type, Total Reports, Last Reported, Whitelisted Status, Tor Status, and Assessment.

10. Locate the Generated Report

After the scan is complete, the scanner generates:

abuseipdb_report.csv

The file is created in the project directory. Verify it with:

ls

11. Open the CSV Report

The generated CSV file can be opened using Microsoft Excel, LibreOffice Calc, or another spreadsheet application.

12. Complete Example

git clone https://github.com/yashbbhor23/ip-reputation-scanner.git
cd ip-reputation-scanner
python3 -m pip install -r requirements.txt
export ABUSEIPDB_API_KEY="YOUR_API_KEY"
nano ips.txt

Add IP addresses such as:

8.8.8.8
1.1.1.1
8.8.4.4

Run the scanner:

python3 abuseipdb_checker.py

When prompted:

Enter path to IP list: ips.txt

Check the generated report:

ls abuseipdb_report.csv

13. Troubleshooting

API Key Missing

If you see: [-] ERROR: AbuseIPDB API key is not configured.

export ABUSEIPDB_API_KEY="YOUR_API_KEY"

Then run the scanner again.

IP List File Not Found

Verify the filename and path. For example: ls ips.txt

If the file exists in the current directory, enter ips.txt. Otherwise, provide the complete path.

Invalid IP Address

The scanner validates IP addresses before processing them. Remove invalid entries from the input file and run the scanner again.

14. Security Considerations

Do not add sensitive or confidential IP address lists to a public repository.

Do not commit API keys, .env files, internal IP address lists, generated reputation reports, or confidential scan results.

The repository's .gitignore is configured to exclude common local input and output files.

15. Important Notes

• An active AbuseIPDB API key is required.
• Internet connectivity is required to communicate with the AbuseIPDB API.
• API usage is subject to AbuseIPDB's applicable limits and policies.
• Only scan IP addresses that you are authorized to investigate.
• The reputation assessment is based on data returned by AbuseIPDB and should be interpreted in context.
