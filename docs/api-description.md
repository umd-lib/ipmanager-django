# Routes for IP Manager API

## /check

Checks if a given IP Address is present in the group or not. Takes two parameters “ip” (String, Required; IP address to be checked for membership) and group (String; Key of the group).
It has as 3 different response types:
* 400 - Unsuccessful request due to invalid parameters, returns the title, detail, and status code
* 404 - Unsuccessful request due to group key not being found, returns the title, detail, and status code
* 200 - Gives back one of two responses -
  * If group and IP are provided, then it returns the URL of the request which includes the query parameters (ex: https://ipmanager-test.lib.umd.edu/check?group=Henson00001&ip=127.0.0.1), group details (url (ex: https://ipmanager-test.lib.umd.edu/groups/Henson00001), key, and name of the group), ip address (whose membership is to be checked), and a boolean (true if contained or false if not)

  * If only IP is provided, then it returns the  URL of the request which includes the query parameters (ex: https://ipmanager-test.lib.umd.edu/check?ip=127.0.0.1),  ip address (whose membership is to be checked), and an array of check results (it checks against all groups), each check consists of information which is returned by (1. group and ID both provided).

## /groups

The /groups route of the API returns a list of groups in JSON format that are flagged as exported. This route only has 1 response defined, and it’s for the 200 status code. Upon a successful response, the API will return the entire request URL as the value to an “@id” key, and it will also return an array of exported groups. For each group, the API returns its key, its name, and a link to its own route. If no groups are marked as exported, then the response will still be successful but the array of groups will be empty.

## /groups/{group_key}

This route has one required parameter which is a string, group_key. In a successful response, with the 200 status code, it returns information about the group with the key group_key. This information includes the request URL which is @id, the key, and the name of the group. If group_key is not the key of a group, the request is unsuccessful and the status is 404. It returns the title, “Group not found” and the detail that there’s no group with that key.
