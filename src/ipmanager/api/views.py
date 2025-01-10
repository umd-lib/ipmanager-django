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