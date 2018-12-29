MISP is a huge beast hat oes lots of things you really don't want to mess with. But our approach is to make your life as easy as possible to interconnect it with 3rd party services, within your own organisation, and to the outside world.

We already talked about syncing, connecting it to TheHive, and sending HTTP requests to it to get information out of the platform to push it into your SIEM for example.

It is nice and all, but at the moment you want to use something else than extracting attributes in CSV, or updating the sightings, it get's tricky to do it with bash and curl. And please, please do not connect directly to the database: it bypasses all ACLs, and if you start editing the datasets, you will most probably break it: there is a lot of data-massaging done when the data enters the system through the web interface, bypassing it will end up in a disaster, and we won't be able to help you.

Before going into the PyMISP internals, let's discuss a bit the API itself.

The format used to push and recieve data to and from a MISP instance is JSON. In the past, there was an XML interface too, but this one has been deprecated years ago. If you're still using it, you should know isn't supported anymore, and hasn't been in the last 2 years, at least.

To query the interface, you send a JSON blob, and it will answer with an other JSON blob. In Python, it is easy, you can load a json blob and get a dictionary, and dump it back to json. It is relatively simple to do it manually for simple requests such as adding a tag, getting the most recently updated attributes, but it get's pretty trycky when you want to run complex search queries, or create new events.


This is the reason we developped PyMISP.

PyMISP has two main interfaces: the first one is directly interacting with a remote MISP instance. Keep in mine that it follows the same access control rules as the ones defined for the account on the web interface.

In order to use the API, you need to get the automation key associated to your account -> URL
If you don't have one, it means your user doesn't have the "Auth key access", you will need to get in touch with your org admin, or the administrator of the platform.

With the key, you can access the same data you can see on the web interface.

# RO

The most common requests we see are the following:
* Get the most recent updates on a timeframe
* Lookup attributes or campaigns

## Recent changes

There are 3 main cases here:
* Metadata of the events that have been modified
    * search_index -> timestamp (1h, 1d, 7d, ...)
        returns list of all the modified events
* Full events (metadata + attributes)
    * search -> timestamp (1h, 1d, 7d, ...)
* Modified attributes
    * search -> controller = attributes & timestamp (1h, 1d, 7d, ...)
     if you want to get all the attributes of a modified event: controller = attributes & timestamp (1h, 1d, 7d, ...)

Other use case: get last **published** events by using the last parameter

## Search

* Easy, but slow: full text search with `search_all`
* search by tag, type, to_ids flag set enforce the warning lists, with attachments, date interval, by organisation
* get malware samples


# Write

add event /attributes/tag/objects, ...

Upload malware sample (with or without the expansion)

(overview, no creation yet)

# Admin tasks

Assuming you have the proper access, you can also do plenty of administrative tasks through the API, such as managing users, organisations, and sync servers.


# Offline creation of a MISPEvent (usage)


# Examples in the example directory


# Internals of the module itself (dev)


Organisation of the project, muttable types




--------------------------------------------



In order to make your life easier, we developped a python modules that will help you to programmatically interact with a MISP instance: PyMISP.


PyMISP has default settings for plenty of comon use cases which simplify the interactions with MISP as much as possible.


PyMISP is the recommended way to programmatically connect MISP to your internal systems, in Python.

It uses the API, which means it is
