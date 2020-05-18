import pulumi
import pulumi_aws as aws
import ipaddress 

config = pulumi.Config()    

zones = pulumi.Output.from_input(aws.get_availability_zones())
zone_names = zones.apply(lambda zs: zs.names)

id = config.require('id')
vpc_cidr = config.require('vpc_cidr')

vpc = aws.ec2.Vpc( id + '_vpc',
    cidr_block=vpc_cidr,
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack(),
    'Owner': config.require('owner'),   
    })

list(ipaddress.ip_network(vpc_cidr).subnets(new_prefix=24))[0]

subnet_infra = aws.ec2.Subnet(id + '_infra_net',
    vpc_id=vpc.id,
    cidr_block=str(list(ipaddress.ip_network(vpc_cidr).subnets(new_prefix=24))[0]),
    availability_zone=zone_names.apply(lambda names: names[0]),
    map_public_ip_on_launch=True,
    tags={
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack(),
    'Owner': config.require('owner'),
    })

subnet_app = aws.ec2.Subnet(id + '_app_net',
    vpc_id=vpc.id,
    cidr_block=str(list(ipaddress.ip_network(vpc_cidr).subnets(new_prefix=24))[1]),
    availability_zone=zone_names.apply(lambda names: names[0]),
    map_public_ip_on_launch=True,
    tags={
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack(),
    'Owner': config.require('owner'),
    })

subnet_mgmt = aws.ec2.Subnet(id + '_mgmt_net',
    vpc_id=vpc.id,
    cidr_block=str(list(ipaddress.ip_network(vpc_cidr).subnets(new_prefix=24))[2]),
    availability_zone=zone_names.apply(lambda names: names[0]),
    map_public_ip_on_launch=True,
    tags={
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack(),
    'Owner': config.require('owner'),
    })

vpc_subnets = [ subnet_infra, subnet_app, subnet_mgmt]

igw = aws.ec2.InternetGateway(id + '_igw',
    vpc_id=vpc.id,
    tags={
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack(),
    'Owner': config.require('owner'),
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
    'Owner': config.require('owner'),
    })

#ec2.get_subnet_ids(vpc_id=vpc.id)
# route_table_assoc_item = {}
# for subnet in vpc_subnets:
#     route_table_assoc_item.update({ subnet: ec2.RouteTableAssociation(id + subnet.resource_name + '_rt',
#     subnet_id=subnet.id, 
#     route_table_id=route_table.id)})

#? subnet_infra.resource_name

subnet_infra = aws.ec2.RouteTableAssociation(id + '_infra_net' + '_rta',
     subnet_id=subnet_infra.id, 
     route_table_id=route_table.id)

subnet_app = aws.ec2.RouteTableAssociation(id + '_app_net' + '_rta',
     subnet_id=subnet_app.id, 
     route_table_id=route_table.id)

subnet_mgmt = aws.ec2.RouteTableAssociation(id + '_mgmt_net' + '_rta',
     subnet_id=subnet_mgmt.id, 
     route_table_id=route_table.id)