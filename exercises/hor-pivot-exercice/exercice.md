# Human operated ransomware attack.



## Your assignement

You are acting as a CTI analyst reviewing the incident response report produced after the ransomware attack against ACME.

Based on the available IOCs and observed techniques, are you able to determine the ransom group that perpertrated this attack with a higl level of confidence. ?

For this, determine and encode only relevant information into MISP, It may include both IOCs (network, host, user) but also and observed techniques mapped to MITRE ATT&CK.

Assess the quality and completeness of the data, taking into account known investigation limitations. 

Pivot within MISP  to identify overlaps with other known campaigns or threat actors.


# Incident report

## Executive Summary

### Current engagement
On 26 May 2025, the firm ACME detected a ransomware attack. Following the incident, ACME mandated the Computer Emergency Response Team (CERT), to conduct a breach analysis of its information system and assist with threat containment. The objectives of the incident response team’s intervention were to:

* Assess the scope and impact of the compromise.
* Identify the attack vector and method of intrusion.
* Support ACME in implementing containment measures.
* Provide recommendations to strengthen ACME’s defenses against similar attacks.


### Mission limitations
Due to their destructive nature, ransomware attacks inherently hinder forensic investigations. When parts of the infrastructure are rendered inoperable, logs and forensic artifacts are often no longer available. At ACME, several logs were irretrievably lost, notably the VPN logs. In addition, other log sources—such as FortiClient logs and Windows logs from servers and workstations were not centralized. As a result, only locally stored logs could be analyzed; these had short retention periods or had been entirely deleted by the attackers.

Another major constraint on the investigation was the lack of time synchronization across the infrastructure. For instance, both firewalls exhibited timestamp discrepancies of up to 30 minutes compared to logs from other systems. These inconsistencies required the incident response team to perform additional preparatory work to correlate events accurately.

## Mission conclusions
On 26 May 2025, ACME was impacted by a ransomware attack. These conclusions outline the actions carried out by the adversaries, from initial access to full compromise of the infrastructure. To facilitate understanding, this report follows the MITRE ATT&CK for Enterprise framework. ATT&CK is a knowledge base of adversary tactics and techniques derived from real-world observations, providing cybersecurity teams with a common and standardized taxonomy. 

### Initial access
The threat intelligence service of the National CERT asserts that the credentials used by the adversaries were stolen on May 10, 2025 on a device yet not identified, via a stealer malware. This information surfaced on May 12in their partner’s database. It is also unknown how the device was infected by this malware. The compromised account is "ACME\TechAccount", which belongs to a third-party provider of ACME.

The account is tied to the domain "extranet.acme.com", one of the VPN endpoints used by ACME.

From May 12 to 18, the VPN logs attest of various successful connections by this account, but without any subsequent traffic, indicating that threat actors were probably validating the account.
This changes on May 18, as a first active connection (with actual traffic) is observed but the only traffic seen are DNS queries.More idle connections are made the following days, until the adversaries connect on the 24th, from a virtual private server. The adversaries will continue using the same device until the end of the attack.

### Discovery
After this phase of initial access, the adversaries scanned the network and performed Active Directory reconnaissance. The firewall logs show lateral scans of entire subnets, with NetBIOS, SMB and LDAP
ports tested (including global catalog on the domain controllers). They were also seen scanning and harvesting data from network shares.

### Privilege escalation
The adversaries gain domain administrator privileges less than 2 hours after their initial access on the 24th, leveraging the account ACME\AdminUser. This user was a member of the Domain Administrator
group and was a dormant account. The investigations did not yield the privilege escalations method used, but considering the short time span, the account used and the network shares scan, it is likely that
they merely found the password in plaintext in a file. Note that adversaries were also seen using the account ACME\Administrator but only after the next day.

### Persistence and lateral movement
The adversaries continued their exploration of the network unnoticed, using the Windows Remote Management (WinRM) protocol to move laterally. WinRM is a Microsoft Windows remote management
protocol. They deployed a custom dll as a persistence mechanism and Command-and-Control (C2) communication channel on several devices. Information about the DLL is available in below, It should be noted, the adversaries operated this channel mainly from two hosts, an exchange server, and a domain server.

### Collection and Exfiltration
During the night of the 25th, a large quantity of data is exfiltrated to cloud services providers. This exfiltration is done from the Trendmicro server, with the account ACME\Administrator. It should be noted that the adversaries seemed to have used another C2 channel on this device. They also left the credentials to access the cloud storage on the device.
ACME, under the agreement of the law enforcement authorities, attempted to access it on June 16, but the account was no longer available at that time.

### Impact

Shortly after completing the exfiltration on 26 May, the adversaries deployed ransomware across the infrastructure, impacting all systems. Analysis of the ransom notes recovered from multiple devices did not allow attribution to a specific ransomware group.

## Timeline


| Date Time | Events | Source |
| --- | -------- | -------- |
|2025-04-26 14:46|Creation of the domain office365-rnanag.com|VeriSign|
|2025-05-11 16:25|TechAccount account credentials stolen from unidentified machine|SpyCloud| CTI
|2025-05-12 12:20|First Illegitimate connections to extranet.ACME.com (VPN) using TechAccount stolen credentials, no traffic exchanged| VPN ACME
2025-05-26 05:12|VPN connections using TechAccount stolen credentials from vm.thanos.org, internal IP: 10.10.10.10 |VPN ACME
2025-05-24 23:58|(*)Network scans from 10.10.10.10|FW ACME
2025-05-24 22:20|(*)AD discovery on DC1 (global catalog) from 10.10.10.10|FW ACME
2025-05-24 23:28|Network shares traversal from 10.10.10.10|FW ACME
2025-05-24 22:54|Adversaries gain domain administrators privileges via AdminUser|ADTimeline
2025-05-24 23:14|Implantation of backdoor (del.dll) | WEBSERVER MFT
2025-05-24 23:18|RDP connection of ACME\AdminUser from WebServer.ACME.com to DC2.ACME.com|DC2
2025-05-24 23:27|Network scan with netscan.exe (AdminUser)|DC2
2025-05-24 23:28|Implantation of backdoor (del.dll)| MAIL-1 MFT
2025-05-25 00:26|(*)Lateral movements (WinRM)| FW ACME
2025-05-26 00:45|(*)Communication to the C2 IP address from various hosts| FW ACME
2025-05-26 00:40|(*)Communication to the C2 (malicious[.]com) from MAIL-1 (UTM logs)| FW ACME
2025-05-25 02:45|RDP connection of ACME\Administrator from WEBSERVER to TrendMicro|TrendMicro
2025-05-25 05:42|Execution of "juras.exe" (not identified) by ACME\Administrator| TrendMicro
2025-05-25 12:45|Observed activities by AdminUser on DC2 (files opened)| DC2’s MFT
2025-05-25 16:28|Multiple attempts of service creation| TrendMicro
2025-05-26 04:04|(*)Potential communication to another C2 from Trendmicro|FW ACME
2025-05-25 21:55|New group ESX Admins created and AdminUser added to it| ADTimeline
2025-05-25 23:14|RDP connection of ACME\AdminUser from WEBSERVER.ACME.com to DC1.ACME.com|DC1’s events
2025-05-25 23:17|Network scan with netscan.exe (AdminUser)DC1’s events Data exfiltration to AS9009 from TrendMicro| FW ACME
2025-05-26 01:06|Preparation of batch script to execute the ransomware|DC1’s MFT
2025-05-26 03:34|Ransomware deployment and execution via PsExec (AdminUser) |Multiple hosts logs

Note that for the firewalls, timestamps marked with (*) were sourced from the FortiAnalyzer rather than the devices themselves, as the firewalls were not synchronized with NTP.


## Forensic analysis
| IOC | Description  |
| -------- | -------- | 
|a4ea10ad050778eddec3cebbc2710d352fb822db| Ransomware sha1 hash for: “win32.exe”, aka “win32x.exe”, “win64.exe”, aka “win64x.exe”, aka “6b240b74_exe.exe”
|21b6f6faaa5e877ed5f1851189ff916c2e1f1ad5|“turnoff.bat”, sha1 hash, defensive batch script
0466e90bf0e83b776ca8716e01d35a8a2e5f96d3| “mhyprot2.sys”, sha1 hash, process killer driver
f036e75812893026474cf9498860be2a22581ad9|“kill.exe”, process killer, uses mhyprot2|
|52332ce16ee0c393b8eea6e71863ad41e3caeafd|Sha1 hashes of “netscan.exe”, network scanner based on wireshark|
|6d95153333f08d22ca6b5be8dc7eb2079c16530b|second sha1 hashes of "netstcan.exe"
0ce9ff331d6378f9f58ddc2b21de73f101ffb8c3 | Sha1 hashes of “def.dll”, original name "chispublic53003.dll" C2 client DLL, Rust, uses chisel to communicate
|7a7d7306f9916c8e2838c0cf389a77cf87c37068| Second sha1 hash fro "def.dll"
66cddd5d63f8e39978fb8357f5de29c076aa4452|“svhost.exe”, sha1 hash, really just “rclone.exe”
66c0e23b88c3a432af7ebcb329e820fca4512380|first “juras.exe” sha1 hash, not retrieved
91137a7c0b99b074ad29d016d714736631f38b41|second “juras.exe” sha1 hash, not retrieved 
|Go-http-client/1.1|C2 client user agent
office365-rnanag.com| C2 domain, fronted by cloudflare: 172.72.72.72, 104.76.76.76
|office365-rnanag.com/login?id=bzy8f3a1c9e2b4d6075a6f0e1c2d3b4a9_xy | C2 Beacon collected
|office365-rnanag.com/login?id=bzy0c7e5a1d9f2b4e6a8c3f7d1b0e9a4c_uv| C2 Beacon collected
|office365-rnanag.com/login?id=bzyb1e9f4c2a6d0e8f7c5a3b9d2e1a4c5_rs | C2 Beacon collected
|office365-rnanag.com/login?id=bzyd4a9e0c7f2b1a6e8c5d3f9b0a1e2c_mw| C2 Beacon collected
vm.vpsips.org|  Abuse: police@vpsips.org 45.36.36.36, 134.106.162.21IP addresses sources from vm.thanos.org
154.201.63.184; 181.214.1.23, 185.103.110.235, 190.190.190.190, 2.58.194.132, 207.244.71.82, 212.10.10.10, 80.67.10.142, 95.211.187.223 | Various actors connected with the stolen credentials using those IPs
104.21.3.3| Potential C2 IP address used from serveur TrendMicro
s3.eu-west-2.wasabisys.com | Exfiltration destination, cloud storage| CNAME to eu-west-2.wasabisys.com
eu-west-2.wasabisys.com.| 130.117.185.100, 130.117.185.101, 130.117.185.102, 130.117.185.103, AS395717




## Tasks
1. Create an new event
    - The `info` field MUST AT LEAST contain the keyword `operated` in it.
2. Do a "quick and dirty" encoding of the above
3. Through the usage of MISP:
    - Find the Threat Actor, then tag your event
    - Find the **Initial access** & **Exfiltration** TTPs used commonly, then tag your event
    - Find the regex used in the C2 domain beaconing, then add the regex to your event
