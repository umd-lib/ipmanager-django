# Create your views here.
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from ipaddress import IPv4Address, AddressValueError
from .models import Group
from urllib.parse import urlencode

class GroupsView(View):
    def get(self, request):
        request_url = request.build_absolute_uri()
        exported_groups = Group.objects.filter(export=True)
        groups = []

        for group in exported_groups:
            groups.append({
                "@id": request.build_absolute_uri(reverse("group_key", args=[group.key])),
                "key": group.key,
                "name": group.name,
            })

        body = {
            "@id": request_url,
            "groups": groups,
        }
        return JsonResponse(body)


class GroupKeyView(View):
    def get(self, request, group_key):
        try:
            group = Group.objects.get(key=group_key)

            body = {
                "@id": request.build_absolute_uri(),
                "key": group_key,
                "name": group.name
            }
            
            return JsonResponse(body)
            
        except Group.DoesNotExist:
            body = {
                "title": "Group not found",
                "detail": f"There is no group with the key {group_key}",
                "status": 404
            }
            
            return JsonResponse(body, status=404)
        

class CheckView(View):
  def get(self, request):

    # domain = request.build_absolute_uri('/')
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
                           "checks":generateChecksArray(ip, all_groups, request)})
    else:
      group_key = request.GET['group']
      try:
        db_group = Group.objects.get(key=group_key)
        return JsonResponse({"@id":request.build_absolute_uri(),
                             "group":{"@id":request.build_absolute_uri(reverse("group_key", args=[group_key])),
                                      "key":group_key,
                                      "name":db_group.name},
                             "ip_address": ip,
                             "contained": contained(ip, group_key)})
      except Group.DoesNotExist:
        return JsonResponse({"title": "Group not found", 
                             "detail": f"There is no group with the key {group_key}.", 
                             "status": 404}, status=404)

def generateChecksArray(ip_address, all_groups, request):
    result = []
    for group in all_groups:
        single_group = {}
        single_group["@id"] = request.build_absolute_uri(reverse("check")) + "?" + urlencode({"group":group.key, "ip":ip_address})
        single_group["@group"] = {"@id":request.build_absolute_uri(reverse("group_key", args=[group.key])),
                                  "key":group.key,
                                  "name":group.name}
        single_group["ip_address"] = ip_address
        single_group["contained"] = contained(ip_address, group.key)
        result.append(single_group)
    return result    

def contained(ip_address, group_key):
  return True