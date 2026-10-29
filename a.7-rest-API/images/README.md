# Screenshot provenance

[rest-client.png](rest-client.png) is a genuine Chromium capture from the default
theme of an isolated MISP **2.5.50** instance at commit
`fc99c9e3fc85beddc6ef18835359f3c8b7f44608`, taken on 29 October 2026.

It shows `/api/rest` with an ordinary training user, the POST method,
`/attributes/restSearch` and a synthetic `.example` domain query. The header
contains the visible placeholder `YOUR_API_KEY`. The prepared request was not
submitted; success and response contracts were verified separately through
live API tests and Newman.

No production data or working key appears. Browser form controls and CodeMirror
were filled through their normal interfaces. This is not a generated mockup.
