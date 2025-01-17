# Create your views here.
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from ipaddress import IPv4Address, AddressValueError
from .models import Group
from urllib.parse import urlencode

def contained(ip_address, group_key):
  return True

def build_group_metadata(request, group):
    return {
        "@id": request.build_absolute_uri(reverse("group_key", args=[group.key])),
        "key": group.key,
        "name": group.name,
    }

def build_checks_result(ip_address, group, request):
    return {
        "@id": request.build_absolute_uri(reverse("check")) + "?" + urlencode({"group":group.key, "ip":ip_address}),
        "group":  build_group_metadata(request, group),
        "ip": ip_address,
        "contained": contained(ip_address, group.key),
    } 

class GroupsView(View):
    def get(self, request):
        request_url = request.build_absolute_uri()
        exported_groups = Group.objects.filter(export=True)
        groups = [build_group_metadata(request, group) for group in exported_groups]

        body = {
            "@id": request_url,
            "groups": groups,
        }
        return JsonResponse(body)


class GroupKeyView(View):
    def get(self, request, group_key):
        try:
            group = Group.objects.get(key=group_key)
            
            return JsonResponse(build_group_metadata(request, group))
        except Group.DoesNotExist:
            body = {
                "title": "Group not found",
                "detail": f"There is no group with the key {group_key}",
                "status": 404
            }
            
            return JsonResponse(body, status=404)
        

class CheckView(View):
  def get(self, request):
    all_groups = Group.objects.all()

    if 'ip' not in request.GET:
      return JsonResponse({"title": "IP address not provided", 
                           "detail": "IP address was not provided as a query parameter", 
                           "status": 400}, status=400)
    
    ip = request.GET['ip']
    try :
        IPv4Address(ip)
    except AddressValueError:
        return JsonResponse({"title": "Unparseable IP address", 
                             "detail": f"The value {ip} you provided in the 'ip' query parameter cannot be " + 
                                      "parsed as a valid IP address.", 
                             "status": 400}, status=400)

    if 'group' not in request.GET:
      return JsonResponse({"@id":request.build_absolute_uri(), 
                           "ip":ip,
                           "checks": [build_checks_result(ip, group, request) for group in all_groups],
                        })
    else:
      group_key = request.GET['group']
      try:
        db_group = Group.objects.get(key=group_key)
        return JsonResponse(build_checks_result(ip, db_group, request))
      except Group.DoesNotExist:
        return JsonResponse({"title": "Group not found", 
                             "detail": f"There is no group with the key {group_key}.", 
                             "status": 404}, status=404)
   