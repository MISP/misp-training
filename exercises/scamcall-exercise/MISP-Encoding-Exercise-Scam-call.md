---
tags: MISP, misp-training, training, exercise, hands-on
---
# MISP Encoding Exercise: Scam call

## Ressources
- [Cheatsheet: Concepts & Data model](https://www.misp-project.org/misp-training/cheatsheet.pdf)
- [Attributes Categories and Types](https://training.misp-community.org/pages/display/doc/categories_and_types)
- [MISP Objects](https://www.misp-project.org/objects.html) and [searchable in MISP](https://training.misp-community.org/objectTemplates/index)
- [Galaxies](https://www.misp-project.org/galaxy.html) and [searchable in MISP](https://training.misp-community.org/galaxies/index)
- [Taxonomies](https://www.misp-project.org/taxonomies.html) and [searchable in MISP](https://training.misp-community.org/taxonomies/index)


## Context
A victim was asked to transfer money to a novice scammer

## Narrative
A victim was called by the suspected scammer Wallace Breen using the following number: +12243359185. The scammer pretended to be a Microsoft employee, managed to convince the victim that he could help by using remote desktop assistance.

Once he had access, the scammer downloaded a binary bin.exe from the following url https://zdgyot.ugic0k.ru/assets/bin.exe. He then proceed to install the binary, probably to use it a backdoor for future access.

After the installation, he asked the victim to transfer money to the scammer bank account: GB29NWBK60161331926819

The day after, the victim suspecting a scam contacted the police.

## Type of data extracted from evidences
- RDP Log file
- Installed binary
- Victim's browser history
- Bank account statement
- Victim's phone call log

## Data extracted from evidences
- Scammer's ip address
- Potentially malicious binary
- URL (and domain) from which the binary was downloaded
- Scammer's bank account and phone number
- Scammer's full name and nationality

## Extracted values
- `194.78.89.250`
    - *ip-address* from log file
- [`bin.exe`](https://cra.circl.lu/bin.exe)
    - Downloaded binary *malware-sample*
- `https://zdgyot.ugic0k.ru/assets/bin.exe`
    - Download `URL`
- `GB 29 NWBK 601613 31926819`
    - *IBAN* number
    - *Swift*: `NWBK`, *Account number*: `31926819`, *Currency*: `GBP`
- `+12243359185`
    - *Phone number*
- `Wallace Breen` is from `GB`
    - *Name* and *nationality*

## Encoding tasks
These are the steps you are asked to do. The order is provided as a suggestion.
1. Create an new *event*
2. Encode all data to be shared
    - **Indicators**
    - Supportive data / Observable
    - Non technical indicators
3. Add relationships to recreate the events and story
4. Add the time component to recreate the chronology
5. Perform enrichments where applicable (e.g location if IP address)
6. Add contextualization
    - **Incident type**
        - `circl`, `enisa`, `europol-incident`
    - **Releasability** and **Permissible Actions**
        - `tlp`, `PAP`
    - **Malware type / familly**
        - `malware_classification`, `ransomware`, `malpedia` Galaxy
    - Infection vector
        - `ransomware`, `maec-delivery-vectors`, `europol-event`
    - **Adversary infrastructure**
        - `adversary`
    - **Adversary tactics and techniques**
        - `attack-pattern` Galaxy
    - Malware-specific information
        - `ransomware`, `maec-malware-capabilities`
    - Mitigations and Detection
        - `Course of Action` Galaxy
    - Sector and Location
        - `Sector` Galaxy, `Country` Galaxy
    - Collaboration and sharing
        - `workflow`, `collaborative-intelligence`
7. Create a small write-up as an *event report*
8. Review the distribution level and publish