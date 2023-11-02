---
tags: MISP, misp-training, training, exercise, hands-on
---
# MISP Encoding Exercise : Ransomware infection via e-mail

## Ressources

- [Cheatsheet: Concepts & Data model](https://www.misp-project.org/misp-training/cheatsheet.pdf)
- [Attributes Categories and Types](https://iglocska.eu/pages/display/doc/categories_and_types)
- [MISP Objects](https://www.misp-project.org/objects.html) and [searchable in MISP](https://iglocska.eu/taxonomies/index)
- [Galaxies](https://www.misp-project.org/galaxy.html) and [searchable in MISP](https://iglocska.eu/galaxies/index)
- [Taxonomies](https://www.misp-project.org/taxonomies.html) and [searchable in MISP](https://iglocska.eu/taxonomies/index)
## Chronology
- **11:42:43 UTC+0**: Email containing the ransomware from supposedly Andrew Ryan
- **11:47:27 UTC+0**: Email was read and its attachment opened and executed
- **11:47:28 UTC+0**: Malware add persistence
- **12:08:18 UTC+0**: Malware successfully contacted the C2 to get the PK
- **12:08:19 UTC+0**: Malware saved the PK in the registry
- **12:25:04 UTC+0**: Malware began the encryption process
- **2022-03-25 08:39:21 UTC+0**: Victim contacted the police

## Collected evidences

- E-mail received by the victim
- E-mail attachment of the ransomware as an .exe payload
- Windows registry
- Ransomware's public key (PK)
- Captured network traffic
- Message displayed by the ransomware

## Type of data extracted from evidences

- Original **e-mail**
- The actual ransomware **binary**
- **Registry Keys** for persistence and configuration
- **Public Key** used for encryption
- C&C server **ip address** used to generate the Private Key (SK)
- The **bitcoin address** on which the ransom should be paid
- The **person**, impersonated or fake that sent the email

## Data extracted from evidences

- ransomware `email`
> Subject: 4829-2375
>From: "Andrew_Ryan" <Andrew_Ryan@rindustries.rp>
>
>Please see the attached Iolta report for 4829-2375.
>
>We received a check request in the amount of $19,637.28 for the above referenced file. However, the attached report refects a $0 balance. At your earliest convenience, please advise how this request is to be funded.
>
>Thanks.
>
>Andrew_Ryan *
>Accounts Payable
>
>Ryan Industries
>42, Central Control Hephaestus - Rapture
>www.rindustries.rp
>
>*Not licensed to practise law.
>
>This communication contains information that is intended only for the recipient named and may be privileged, confidential, subject to the attorney-client privilege, and/or exempt from disclosure under applicable law. If you are not the intended recipient or agent responsible for delivering this communication to the intended recipient, you are hereby notified that you have received this communication in error, and that any review, disclosure, dissemination, distribution, use, or copying of this communication is STRICTLY PROHIBITED. If you have received this communication in error, please notify us immediately by telephone at 1-800-766-7751 or 1-972-643-6600 and destroy the material in its entirety, whether in electronic or hard copy format.
- `bin.exe`
    - Ransomware attached to the mail
    - [`bin.exe`](https://cra.circl.lu/bin.exe)
- `81.177.170.166`
    - `ip address` of a C2 server used to generate the SK
- `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run "CryptoLocker"`
    - The registry key used for persistence
- `HKCU\SOFTWARE\CryptoLocker VersionInfo`
    - The registry key containing configuration data
- `HKCU\SOFTWARE\CryptoLocker PublicKey`
    - The registry key containing the RSA public key received from the C2 server
- `0x819C33AE`
    - XOR key used to encode the configuration data
- The public key received from the C2 used to encrypt files
```text
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDaogllvHPytDAdUWZPk9aWXJ5G
Lk9F+HzDaj5qGXou8XmISwChbia/NC84QmBHTiyg4B1tqVjqk5X6yh6pcZuVw+GX
0CrH5O5o2Q0XVYzYYsEZQB36VHxwm7xTx21yOy2rSOQyOupQ6e7HMGtu7p7+RlWO
D5UfPkv337plrEiUuwIDAQAB
-----END PUBLIC KEY-----
```
- `1KP72fBmh3XBRfuJDMn53APaqM6iMRspCh`
    - Bitcoin address on which to transfer the ransom
- Person, e-mail, occupation and role
    - `Andrew Ryan`, `Andrew_Ryan@rindustries.rp`
    - `Accountant`, `Suspect`, `Victim`, `Originator`


## Tasks

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
        - `malware_classification`, `ransomware`
    - Infection vector
        - `ransomware`, `maec-delivery-vectors`, `europol-event`
    - **Adversary infrastructure**
        - `adversary`
    - **Adversary tactics and techniques**
        - `attack-pattern` Galaxy
    - Malware-specific information
        - `ransomware`, `maec-malware-capabilities`
    - Mitigations and Detection
        - `Course of Action`
    - Collaboration and sharing
        - `workflow`, `collaborative-intelligence`
7. Create a small write-up as an *event report*

8. Review the distribution level and publish

