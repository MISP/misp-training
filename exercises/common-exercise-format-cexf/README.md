
# Common Exercise Format (CEXF)

Common Exercise Format is a proposed format to describe an exercise including the exercise metadata, inject flow, the inject and the associated validations/scoring.

# Why structuring exercises in a common format such as CEXF?

- To ensure that an exercise contains all the required elements;
- To validate exercise definitions, in particular potential issues such as the missing or incorrect elements;
- To automate the planning and injects;
- To trace the evolution of an exercise (via diff ang git);
- To allow external contributions by using a common format;

## Common Exercise format - Sample


```json
{
    "exercise": {
       "uuid": "75d7460-af9d-4098-8ad1-754457076b32",
       "name": "Phishing e-mail",
       "description": "Simple Spear Phishing e-mail example, mimicing a fraud case",
       "tags": ["exercise:software-scope=\"\misp\"", "state:production"]
    },
    "inject_flow": [
        {
            "inject_uuid": "19272db1-a7c4-4cb3-aa33-df775b8fec8c",
            "trigger": "startex",
            "requirements": []
        },
                {
            "inject_uuid": "c104aa37-e394-43ce-b82b-a733d3745468",
            "trigger": "inject-resolution",
            "requirements": {
                "inject_uuid": "19272db1-a7c4-4cb3-aa33-df775b8fec8c",
                "resolution_requirement": "Publishing"
            }
        }
    ],
    "injects": [
        {
            "uuid": "19272db1-a7c4-4cb3-aa33-df775b8fec8c",
            "name": "received e-mail from csirt@telco.lu",
            "action": "email_to_participants",
            "action_payload_resource_uuid": "930c6f6b-f89d-456d-a59d-5cb89bdec0b1",
            "target_tool": "MISP",
            "inject_evaluation": [
                {
                    "result": "MISP event creation",
                    "parameters": [
                        {
                            "Event.info": {
                                "comparison": "contains",
                                "values": ["phishing", "CEO"]
                            }
                        }
                    ],
                    "score_range": [0, 10]
                },
                {
                    "result": "MISP attribute capture",
                    "parameters": [
                        {
                            "Event.attribute": {
                                "comparison": "equals",
                                "values": {
                                    {
                                        "value": "john.doe@luxembourg.edu",
                                        "type": ["email-src", "email"]
                                    },
                                    {
                                        "value": "throwaway-email-provider.com",
                                        "type": "domain"
                                    },
                                    {
                                        "value": "137.221.106.104",
                                        "type": ["ip-src", "ip-dst"]
                                    },
                                    {
                                        "value": "CVE-2015-5465",
                                        "type": ["vulnerability"]
                                    }
                                }
                            }
                        }
                    ],
                    "score_range": [0, 40]
                },
                {
                    "result": "MISP object use",
                    "parameters": [
                        {
                            "Event.Object": {
                                "comparison": "count",
                                "values": [">3"]
                            }
                        }
                    ],
                    "score_range": [0, 30]
                },
                {
                    "result": "Mitre ATT&CK use",
                    "parameters": [
                        "OR": [
                            {
                                "Event.EventTag.Tag.{n}.Tag.name": {
                                    "comparison": "contains",
                                    "values": ["T1566"]
                                }
                            },
                            {
                                "Event.Attribute.{n}.AttributeTag.{n}.Tag.name": {
                                    "comparison": "contains",
                                    "values": ["T1566"]
                                }
                            }
                        ]
                    ],
                    "score_range": [0, 10]
                },
                {
                    "result": "Publishing",
                    "parameters": [
                        {
                            "Event.published": {
                                "comparison": "is",
                                "values": [1]
                            }
                        }
                    ],
                    "score_range": [0, 10]
                }
            }
        },
        {
            "uuid": "c104aa37-e394-43ce-b82b-a733d3745468",
            "name": "malicious network flow",
            "action": "network connection",
            "action_payload_resource_uuid": "9b519819-36cc-48b1-8418-43831f2d3a6a",
            "target_tool": "Suricata",
            "inject_evaluation": [
                {
                    "result": "alert",
                    "parameters": [
                        {
                            "source-ip": {
                                "comparison": "is",
                                "values": ["137.221.106.104"]
                            }
                        }
                    ],
                    "score_range": [0, 50]
                }
            ]
                    
        }
    ],
    "inject_payloads": [
        {
            "uuid": "930c6f6b-f89d-456d-a59d-5cb89bdec0b1",
            "name": "",
            "type": "file",
            "parameters": {
                "filename": "email.eml",
                "contents": "Dear xy,

We have had a failed spearphishing attempt targeting our CEO recently with the following details:

Our CEO received an E-mail on 03/02/2021 15:56 containing a personalised message about a report card for their child. The attacker pretended to be working for the school of the CEO’s daughter, sending the mail from a spoofed address (john.doe@luxembourg.edu). John Doe is a teacher of the student. The email was received from throwaway-email-provider.com (137.221.106.104). 

The e-mail contained a malicious file (find it attached) that would try to download a secondary payload from https://evilprovider.com/this-is-not-malicious.exe (also attached, resolves to 2607:5300:60:cd52:304b:760d:da7:d5). It looks like the sample is trying to exploit CVE-2015-5465. After a brief triage, the secondary payload has a hardcoded C2 at https://another.evil.provider.com:57666 (118.217.182.36) to which it tries to exfiltrate local credentials. This is how far we have gotten so far. Please be mindful that this is an ongoing investigation, we would like to avoid informing the attacker of the detection and kindly ask you to only use the contained information to protect your constituents.

Best regards,",
                "content-type": "raw"
            }
        },
        {
            "uuid": "9b519819-36cc-48b1-8418-43831f2d3a6a",
            "name": "",
            "type": "telnet_connection",
            "parameters": {
                "source": "137.221.106.104",
                "destination": "player_network_mail_server"
            }
        }
    ]
}
```
