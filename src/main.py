from cidr.cidr import Cidr, CidrSet

# IP ADDRESS
# 2 -> 00000010

# Create a CidrSet for the address 192.168.0.0/23, where the first 23 bits refer to the network.
# Then, the addresses 192.168.1.0 and 192.168.0.0 should be a part of the set 
# since they share the same network (first 23 bits).

# 0.0.0.0/24

ip1 = Cidr("0.0.0.0/24")
# With /24, the network block of ip1 is its first 24 bits: i.e. the first 3 sections
ip2 = Cidr("0.0.0.90")
ip3 = Cidr("0.0.0.1")
ip4 = Cidr("1.0.0.0")

print("--- Learning about CidrSet ---")
cidrset = CidrSet(ip1)
# Any IP address that has the same first 24 bits will be a part of this network.
print(ip1 in cidrset)
print(ip2 in cidrset)
print(ip3 in cidrset)
print(ip4 in cidrset)

print("--- Testing Set Differences ---")
empty_cidrset = CidrSet()
single_cidrset = CidrSet(Cidr("129.4.13.25"))
result = empty_cidrset - single_cidrset
print(f"{{}} - {{129.4.13.25}} = {result}")
print(len(result))

print("--- Testing Something ---")
set1 = CidrSet(Cidr("10.10.10.10"))
set2 = CidrSet(Cidr("10.10.10.10"))
print(set1 + set2)
print((set1 + set2) - empty_cidrset)