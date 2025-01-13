# Create your views here.
from django.views import View
from django.http import JsonResponse

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