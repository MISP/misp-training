# Introduction

Placeholder to describe the format for the common exercise format.


## Header information

uuid: uuid  Auto-generated
name: string    descriptive name
description: string short description
expanded: string    long description
tags: list
version: string unique version ID; prefer to have the current date in YYYYMMDD
valid_until: string describe the timestamp how long this training is valid; no value means undefinite
level: the level of maturity from the student; beginnner; intermediate or advanced
namespace: string container to collect related exercises

```
"exercise": {
    "uuid": "75d7460-af9d-4098-8ad1-754457076b32",
    "name": "Phishing e-mail",
    "description": "Simple Spear Phishing e-mail example, mimicing a fraud case",
    "expanded": "# Simple Spear Phishing e-mail example, mimicing a fraud case",
    "tags": [
      "exercise:software-scope=\"misp\"",
      "state:production"
    ],
    "version": "20210611",
    "valid_until": "20310611",
    "level": "beginner",
    "namespace": "phishing"
  },
  ```

  ## Infrastructure

  tbd