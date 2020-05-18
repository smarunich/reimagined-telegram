import pulumi
from pulumi_aws import ec2, get_availability_zones
import ipaddress 

import aws_iam_roles
import aws_infrastructure


config = pulumi.Config()    
print(f"vpc_cidr: {config.require('vpc_cidr')}")
print(f"flavour_master: {config.require('flavour_master')}")
print(f"flavour_server: {config.require('flavour_server')}")
print(f"flavour_jumpbox: {config.require('flavour_jumpbox')}")
print(f"flavour_avi: {config.require('flavour_avi')}")
print(f"vol_size_ubuntu: {config.require('vol_size_ubuntu')}")
print(f"vol_size_avi: {config.require('vol_size_avi')}")

print(f"Owner: {config.require('owner')}")
print(f"Id: {config.require('id')}")
