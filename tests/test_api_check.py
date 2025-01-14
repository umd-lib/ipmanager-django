import pytest

# from src.ipmanager.api.views import APICheckView

def test_missing_ip(client):
  response = client.get("/check", {"notIP":"123.123.1"}, follow=True)
  assert response.status_code == 400

def test_group_present_ip_absent(client):
  response = client.get("/check", {"group":"A","notIP":"123.123.1"}, follow=True)
  assert response.status_code == 400

def test_unparseable_ip(client):
  response = client.get("/check", {"ip":"192.8888999"}, follow=True)
  assert response.status_code == 400

def test_group_not_found(client):
  response = client.get("/check", {"group":"notFound", "ip":"192.168.0.1"}, follow=True)
  assert response.status_code == 404

def test_correct_group_and_ip(client):
  response = client.get("/check", {"group":"A", "ip":"192.168.0.1"}, follow=True)
  assert response.status_code == 200

  # Checking if the response has the group key and ip_address that was passed 
  # in as query parameter
  assert response.json()['group']['key']=='A'
  assert response.json()['ip_address'] =='192.168.0.1'

  # To check if the contained function works as intended
  assert response.json()["contained"]==True

def test_correct_ip_only(client):
  response = client.get("/check", {"ip":"192.168.0.1"}, follow=True)
  assert response.json()['ip']=="192.168.0.1"

