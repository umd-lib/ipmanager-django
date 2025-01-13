# Create your views here.
from django.views import View
from django.http import JsonResponse
from django.http import QueryDict

class GroupsView(View):
    def get(self, request):
        # Grab full request URL
        request_url = request.build_absolute_uri()
        exported_groups = ["Group1Key", "Group2Key", "Group3Key"]
        groups = []

        # Populate the groups array, where each group is a dict
        for group_key in exported_groups:
            groups.append({
                "@id": request_url + group_key,
                "key": group_key,
                "name": group_key + "'s name"
            })

        body = {
            "@id": request_url,
            "groups": groups,
        }
        return JsonResponse(body)

class GroupKeyView(View):
    def get(self, request, group_key):
        groups = ["key1", "key2", "key3"]

        if (group_key in groups):
            body = {
                "@id": request.build_absolute_uri(),
                "key": group_key,
                "name": "group " + group_key + "'s name"
            }

            return JsonResponse(body)
        
        else:
            body = {
                "title": "Group not found",
                "detail": "There is no group with the key " + group_key,
                "status": 404
            }

            return JsonResponse(body, status=404)
        

class APICheckView(View):

  def get(self, request):

    # Made-up data
    group_keys = ["A", "B", "C", "D"]

    # Using query_string (unparsed) and to create Query Dict object to extrack parameters
    dict = QueryDict(query_string = request.META['QUERY_STRING'], mutable=False, encoding=None)
    
    # Returning 400 error if wrong parameters or ip not present
    if 'ip' not in dict:
      return JsonResponse({"title": "Unparseable IP address", 
                           "detail": "The value 'invalid_ip' you provided in the 'ip' query parameter cannot be" + 
                                     "parsed as a valid IP address.", 
                           "status": 400}, status=400)
    
    # Can extract ip from dict now
    ip = dict['ip']

    if 'group' not in dict:
      return JsonResponse({"@id":request.build_absolute_uri(), 
                           "ip":ip,
                           # Demo-only data, with actual data iterate through all group_keys and make url and parse response accordingly
                           "checks":[{"@id":"https://ipmanager-test.lib.umd.edu/check?group=Henson00001&ip=127.0.0.1",
                                      "group":{"@id":"ttps://ipmanager-test.lib.umd.edu/groups/Henson00001",
                                               "key":"henson20001","name":"Henson Collection"},
                                      "ip_address":ip,
                                      "contained":False}]})
    else:
      group = dict['group']
      if group in group_keys:
        return JsonResponse({"@id":request.build_absolute_uri(),
                            # We probably need to create the group_key url, if not present as field in the model
                             "group":{"@id":"https://ipmanager-test.lib.umd.edu/groups/henson20001",
                                      "key":group,
                                      "name":"Henson Collection"},
                             "ip_address":
                             ip,"contained": contained()})
      else :
        return JsonResponse({"title": "Group not found", 
                             "detail": "There is no group with the key 'nonexistent-group'.", 
                             "status": 404}, status=404)
      
# When only IP is present, the we need to create url for each group and check for membership. 
# For contained, we need to create a function to actually check for membership and return boolean value.

def contained():
  return True