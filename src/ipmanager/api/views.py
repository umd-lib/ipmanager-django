# Create your views here.

from django.views import View
from django.http import JsonResponse



class Group_KeyView(View):

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