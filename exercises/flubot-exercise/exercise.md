---
tags: MISP, misp-training, training, exercise, hands-on
---
# MISP Encoding Exercise: Flubot malware capture by honeypot
(Inspired by the [blogpost of telekom.com](https://www.telekom.com/en/blog/group/article/flubot-under-the-microscope-636368))

## Ressources
- [Cheatsheet: Concepts & Data model](https://www.misp-project.org/misp-training/cheatsheet.pdf)
- [Attributes Categories and Types](https://iglocska.eu/pages/display/doc/categories_and_types)
- [MISP Objects](https://www.misp-project.org/objects.html) and [searchable in MISP](https://iglocska.eu/taxonomies/index)
- [Galaxies](https://www.misp-project.org/galaxy.html) and [searchable in MISP](https://iglocska.eu/galaxies/index)
- [Taxonomies](https://www.misp-project.org/taxonomies.html) and [searchable in MISP](https://iglocska.eu/taxonomies/index)


## Context
Our honeypot detected a FluBot infection with the following details:
 
The honeypot received a SMS text message on `2022-03-12 13:27` from `+352131575` containing a text notifying that the recipient missed a call, and a suspicious link they should click on to listen to a voicemail. Upon multiple reception of these text messages, we observed that the link is personalized. Here is a sample of such text message:
```
Missed Call: You have a missed call.
Caller left you a message: https://evilprovider.com/r.php?e1525c0f
```

This link points to a payload to be downloaded (also attached as `sample.apk`, the link resolves to `8.231.77.176`)

We downloaded the malware hosted on that URL and ran it in our sandbox. It looks like the sample is trying to exploit `CVE-2022-27835` and fetches its configuration from an hardcoded C2 server at `https://another.evil.provider.com:42666/c.php?e1525c0f` (`226.140.183.77` and `2efe:65b4:7533:4f5f:1081:0995:ff87:348f`).

We generated a YARA rule that can be used for blocking similar payload:
```
rule android_flubot {
    meta:
        author = "Thomas Barabosch, Telekom Security"
        version = "20210720"
        description = "matches on dumped, decrypted V/DEX files of Flubot version > 4.2"
        sample = "37be18494cd03ea70a1fdd6270cef6e3"

    strings:
        $dex = "dex"
        $vdex = "vdex"
        $s1 = "LAYOUT_MANAGER_CONSTRUCTOR_SIGNATURE"
        $s2 = "java/net/HttpURLConnection;"
        $s3 = "java/security/spec/X509EncodedKeySpec;"
        $s4 = "MANUFACTURER"

    condition:
        ($dex at 0 or $vdex at 0)
        and 3 of ($s*)
}
```

After a while, the installed malware exfiltrates the contact list to the C2 server.
Periodically, the bot queries the same C2 to receive a new target to try to infect and a SMS text.
Example:
```
Missed Call: You have a missed call.
Caller left you a message: https://evilprovider.com/r.php?a1f9f536
```

We strongly believe that the seemingly random sequence of character at the end of the URL is used as a form of token for validation.

This is how far we have gotten so far. Please be mindful that this is an ongoing investigation, we would like to avoid informing the attacker of the detection and kindly ask you to only use the contained information to protect your constituents.

- Sample: [sample.apk](https://iglocska.eu/malicious.exe)

## Type of data extracted from evidences
- Phishing SMS
- URL of the phishing website
- CVE
- URL of the C2 server
- Yara rule
- Another phishing SMS sent from infected device
- Malicous APK

## Data extracted from evidences


- Orignal phishing SMS collected from honeypot
```
Missed Call: You have a missed call.
Caller left you a message: https://evilprovider.com/r.php?e1525c0f
```

- `+352131575`
    - Phoner number sender of original SMS
- `https://evilprovider.com/r.php?e1525c0f`
    - Phishing URL contained in the original SMS
- `8.231.77.176`
    - Resolved IP address for the above domain
- [sample.apk](https://iglocska.eu/malicious.exe)
    - Malicious APK infecting the device
- `CVE-2022-27835`
    - CVE exploited by the malware
- `https://another.evil.provider.com:42666/c.php?e1525c0f`
    - URL of the C2 server
- `226.140.183.77` and `2efe:65b4:7533:4f5f:1081:0995:ff87:348f`
    - IP addresses resolving to the C2
- Provided Yara rule for blocking similar payload
```yara
rule android_flubot {
    meta:
        author = "Thomas Barabosch, Telekom Security"
        version = "20210720"
        description = "matches on dumped, decrypted V/DEX files of Flubot version > 4.2"
        sample = "37be18494cd03ea70a1fdd6270cef6e3"

    strings:
        $dex = "dex"
        $vdex = "vdex"
        $s1 = "LAYOUT_MANAGER_CONSTRUCTOR_SIGNATURE"
        $s2 = "java/net/HttpURLConnection;"
        $s3 = "java/security/spec/X509EncodedKeySpec;"
        $s4 = "MANUFACTURER"

    condition:
        ($dex at 0 or $vdex at 0)
        and 3 of ($s*)
}
```

- Phishing SMS sent from infected device
```
Missed Call: You have a missed call.
Caller left you a message: https://evilprovider.com/r.php?a1f9f536
```


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
