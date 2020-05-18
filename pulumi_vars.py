import pulumi
import pulumi_aws as aws

config = pulumi.Config()    

zones = pulumi.Output.from_input(aws.get_availability_zones())
zone_names = zones.apply(lambda zs: zs.names)


print(f"vpc_cidr: {config.require('vpc_cidr')}")
vpc_cidr = config.require('vpc_cidr')

print(f"flavour_master: {config.require('flavour_master')}")
flavour_master = config.require('flavour_master')

print(f"flavour_server: {config.require('flavour_server')}")
flavour_server = config.require('flavour_server')

print(f"flavour_jumpbox: {config.require('flavour_jumpbox')}")
flavour_jumpbox = config.require('flavour_jumpbox')

print(f"flavour_avi: {config.require('flavour_avi')}")
flavour_avi = config.require('flavour_avi')

print(f"ami_ubuntu: {config.require('ami_ubuntu')}")
ami_ubuntu = config.require('ami_ubuntu')

print(f"vol_size_ubuntu: {config.require('vol_size_ubuntu')}")
vol_size_ubuntu = config.require('vol_size_ubuntu')

print(f"vol_size_avi: {config.require('vol_size_avi')}")
vol_size_avi = config.require('vol_size_avi')

print(f"Owner: {config.require('owner')}")
owner = config.require('owner')

print(f"Id: {config.require('id')}")
id = config.require('id')