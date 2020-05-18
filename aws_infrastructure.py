import pulumi
import pulumi_aws as aws
import ipaddress 
from pulumi_vars import *

vpc = aws.ec2.Vpc( id + '_vpc',
    cidr_block=vpc_cidr,
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack(),
    'Owner': owner, 
    'Name': id + '_vpc'
    })

list(ipaddress.ip_network(vpc_cidr).subnets(new_prefix=24))[0]

vpc_subnets = []

subnet_infra = aws.ec2.Subnet(id + '_infra_net',
    vpc_id=vpc.id,
    cidr_block=str(list(ipaddress.ip_network(vpc_cidr).subnets(new_prefix=24))[0]),
    availability_zone=zone_names.apply(lambda names: names[0]),
    map_public_ip_on_launch=True,
    tags={
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack(),
    'Owner': owner, 
    'Name': id + '_infra_net'
    })

vpc_subnets.append(subnet_infra.id)

subnet_app = aws.ec2.Subnet(id + '_app_net',
    vpc_id=vpc.id,
    cidr_block=str(list(ipaddress.ip_network(vpc_cidr).subnets(new_prefix=24))[1]),
    availability_zone=zone_names.apply(lambda names: names[0]),
    map_public_ip_on_launch=True,
    tags={
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack(),
    'Owner': owner, 
    'Name': id + '_app_net'
    })


vpc_subnets.append(subnet_app.id)

subnet_mgmt = aws.ec2.Subnet(id + '_mgmt_net',
    vpc_id=vpc.id,
    cidr_block=str(list(ipaddress.ip_network(vpc_cidr).subnets(new_prefix=24))[2]),
    availability_zone=zone_names.apply(lambda names: names[0]),
    map_public_ip_on_launch=True,
    tags={
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack(),
    'Owner': owner, 
    'Name': id + '_mgmt_net'
    })

vpc_subnets.append(subnet_mgmt.id)

igw = aws.ec2.InternetGateway(id + '_igw',
    vpc_id=vpc.id,
    tags={
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack(),
    'Owner': owner, 
    'Name': id + '_igw'
    })


route_table = aws.ec2.RouteTable(id + '_rt',
    vpc_id=vpc.id,
    routes=[{
        "cidrBlock": "0.0.0.0/0",
        "gatewayId": igw.id
    }],
    tags={
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack(),
    'Owner': owner, 
    'Name': id + '_rt'
    })

# route_table_assoc_item = {}
# #vpc_subnets = aws.ec2.get_subnet_ids(vpc_id=vpc.id)

#  for subnet_id in vpc_subnets:
#      route_table_assoc_item.update({subnet_id: aws.ec2.RouteTableAssociation(id + "_" + str(subnet_id) + "_rta",
#       subnet_id=subnet_id, 
#       route_table_id=route_table.id)})

# subnet_count = 0
# for subnet_id in vpc_subnets:
#     subnet_count += 1
#     route_table_assoc_item.update({subnet_id: aws.ec2.RouteTableAssociation(id + "_subnet" + str(subnet_count) + "_rta",
#     subnet_id=subnet_id, 
#     route_table_id=route_table.id)})

subnet_infra_rta = aws.ec2.RouteTableAssociation(id + '_infra_net' + '_rta',
     subnet_id=subnet_infra.id, 
     route_table_id=route_table.id)

subnet_app_rta = aws.ec2.RouteTableAssociation(id + '_app_net' + '_rta',
     subnet_id=subnet_app.id, 
     route_table_id=route_table.id)

subnet_mgmt_rta = aws.ec2.RouteTableAssociation(id + '_mgmt_net' + '_rta',
     subnet_id=subnet_mgmt.id, 
     route_table_id=route_table.id)

