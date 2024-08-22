---
tags: MISP, misp-training, training, exercise, hands-on
---
# MISP Encoding Exercise : Campaign Targeting Multiple ISACs

## Ressources

- [Cheatsheet: Concepts & Data model](https://www.misp-project.org/misp-training/cheatsheet.pdf)
- [Attributes Categories and Types](https://www.misp-project.org/datamodels/)
- [MISP Objects](https://www.misp-project.org/objects.html)<!-- and [searchable in MISP](https://iglocska.eu/taxonomies/index) -->
- [Taxonomies](https://www.misp-project.org/taxonomies.html)<!-- and [searchable in MISP](https://iglocska.eu/taxonomies/index) -->
- [Galaxies](https://www.misp-project.org/galaxy.html)<!-- and [searchable in MISP](https://iglocska.eu/galaxies/index) -->


## Involved parties
One or more members of:
- Retail and Hospitality ISAC (**RH-ISAC**): Retailers, restaurants, hotels, ...
- **Space ISAC**: Space sector organization, Satellite operators, space agencies, ...
- Top-Level Domain ISAC (**TLD-ISAC**): Registries, DNS Operators, ...
- Consumer Data Industry Association (**CDA-ISAC**): Consumer data industry, credit reporting agencies, data brokers, ...
- Aviation ISAC (**A-ISAC**): Airlines, airports, manufacturers, ...

## Chronology of Events

- **Day 1** - **Spear Phishing Campaign**
    - **RH-ISAC** members are hit by a simple spear-phishing campaign
    - The phishing emails contain a malicious attachment that installs a backdoor
    - Their infrastructure is used to send a second wave of phishing email targeting Space ISAC
- **Day 2** - **Second Spear Phishing Wave**
    - **RH-ISAC** members notice unusual traffic originating from their infrastructure
    - They notify **Space ISAC**'s member about the campaign and potential compromise
- **Day 3** - **Exploit on Known Vulnerability and Phishing websites**
    - **TLD-ISAC** members are targeted by a known vulnerability on an unpatched exposed software giving access to TLD registry's systems.
    - DNS record for **RH** and **space** sector are manipulated to cloned phishing pages
    - **CDA-ISAC** members are impacted as well and a cloned website is used to steal personal information
- **Day 4** - **Disruptions and ISACs collaboration**
    - Stolen identities are used to disrupt operations and perform unauthorized purchases
    - All ISACs collaborates together to mitigates and stop the attacks

#### Summary of the whole campaign:
1. Spear-phishing campaign 1 + backdoor
2. Spear-phishing campaign 2 + backdoor
3. Vulnerable software is exploited
4. DNS record are changed

## Evidence Collected

- **Malicious Email Attachment**: Malicious file attached to the spear phishing emails
- **Network Traffic Analysis**: Evidence of C2 communication after the backdoor installation
- **Backdoor installation**: The backdoor identified on compromised systems
- **Known Vulnerability**: Exploit code use to attack the known vulnerability
- **Redirected DNS Logs**: Logs showing unauthorized DNS changes

## Data Extracted from Evidence (IoCs)

- **IP Addresses**
    - `195.208.152.43`: IP address of the C2 server associated with the backdoor communication
    - `80.72.225.30`: IPs linked to the malicious sites used in DNS redirection
- **Domain Names**
    - Known URLs used for the C2 server so far
        - `https://c2.intgmx.deadnxuyla.ru`
        - `https://c2.axwscw.deadnxuyla.ru`
        - `https://c2.kgodir.deadnxuyla.ru`
        - `https://c2.nvbvod.deadnxuyla.ru`
        - `https://c2.qpdjrn.deadnxuyla.ru`
        - `https://c2.isannt.deadnxuyla.ru`
        - `https://c2.pofkwn.deadnxuyla.ru`
        - `https://c2.xlalfg.deadnxuyla.ru`
    - Malicious domain where traffic was redirected after DNS manipulation
        - `secure-pay.com`
        - `secure-book.com`
- **Algorithm used to pick the next C2 domain**
    - Reversed algorithm from the backdoor
    ```bash
    #!/bin/bash

    generate_domain() {
        static_prefix="https://c2."
        static_suffix=".deadnxuyla.ru"

        random_part=$(tr -dc 'a-z' < /dev/urandom | head -c 6)

        domain="${static_prefix}${random_part}${static_suffix}"
        echo $domain
    }
    ```
- **Rules to block traffic to these domains**
    - Suricata rule
    ```suricata
    drop ip any any -> any any (msg:"Block traffic to specific domains"; content:"deadnxuyla.ru"; pcre:"/c2\.[a-z]{6}-deadnxuyla\.ru/"; sid:100001;)
    ```
    - iptables Rule
    ```text
    iptables -A OUTPUT -p tcp -m string --string "deadnxuyla.ru" --algo bm -j REJECT
    iptables -A OUTPUT -p udp -m string --string "deadnxuyla.ru" --algo bm -j REJECT
    ```
- **Payloads and Exploit code**
    - [`Account_Verification.docx.exe`](https://cra.circl.lu/Account_Verification.docx.exe)
    - [`exploit-exposed-software.sh`](https://cra.circl.lu/exploit-exposed-software.sh)
- **Registry Keys**
    - `HKCU\SOFTWARE\MSCall PublicKey`: Registry key containing the backdoor configuration
- **Public Key**
    - `0x281A77EA`: The XOR key received from the C2 to encrypt known C2 domains. Collected through network interception.
- **Spear Phishing Email with Headers**
    > Received: from mailout-us.gmx.ru
    > Received: from 91.122.31.203 by rms-us015 with HTTP
    > Return-Path: admin@secure-company.net
    > From: noreply@trustedsender.org
    > To: jane.doe@hotel.com
    > Subject: Urgent: Bank Account Verification Required
    > 
    > Dear Jane Doe,
    > 
    > We’ve detected unusual activity in your account and need to verify your information to ensure continued payement of your salary. Please download and review the attached document containing the details and follow the instructions to verify your bank account details.
    > 
    > Failure to do so within 24 hours may result in a temporary suspension of your payment.
    > 
    > Thank you for your prompt attention to this matter.
    > 
    > Best regards,
    > Sandy Brown
    > HR Financial Team Lead

## Tasks
1. Create a new Event
2. Encode all data: Both Indicators (IoCs) and Supportive Data
3. Add few relationships
4. Perform enrichments where applicable
5. Add context
    - **Releasability** and **Permissible Actions**
    - **Adversary infrastructure**
    - **Adversary tactics and techniques**
6. Review the Distribution Levels
    - Shared with **All**:
        - **C2 IP Address**
        - **Malicious Domain Names** and **Reversed Algorithm**
        - **Remediation scripts**
        - **Email Attachment**
        - **Spearphishing Email**
    - Shared with a **Subset of ISACs**:
        - **Exploit code** for the unpatched exposed software
        - **Redirected DNS Logs**
    - Kept internal:
        - **Spearphishing victims**
7. Publish the Event
