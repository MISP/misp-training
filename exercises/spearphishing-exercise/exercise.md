### Incident report email

> From csirt@telco.lu
> 
> Dear xy,
> 
> We have had a failed spearphishing attempt targeting our CEO recently with the following details:
> 
> Our CEO received an E-mail on 03/02/2021 15:56 containing a personalised message about a report card for their child. The attacker pretended to be working for the school of the CEO’s daughter, sending the mail from a spoofed address (john.doe@luxembourg.edu). John Doe is a teacher of the student. The email was received from throwaway-email-provider.com (137.221.106.104). 
> 
> The e-mail contained a malicious file (find it attached) that would try to download a secondary payload from https://evilprovider.com/this-is-not-malicious.exe (also attached, resolves to 2607:5300:60:cd52:304b:760d:da7:d5). It looks like the sample is trying to exploit CVE-2015-5465. After a brief triage, the secondary payload has a hardcoded C2 at https://another.evil.provider.com:57666 (118.217.182.36) to which it tries to exfiltrate local credentials. This is how far we have gotten so far. Please be mindful that this is an ongoing investigation, we would like to avoid informing the attacker of the detection and kindly ask you to only use the contained information to protect your constituents.
> 
> Best regards,

- Sample 1: [malicious.exe](https://iglocska.eu/malicious.exe)
- Sample 2: [this-is-not-malicious.exe](https://iglocska.eu/this-is-not-malicious.exe)
