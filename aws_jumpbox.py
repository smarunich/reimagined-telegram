import pulumi
import pulumi_aws as aws
from jinja2 import Template
import base64
from pulumi_vars import *
from aws_infrastructure import *
from aws_security_groups import *
from aws_access_key import *
from aws_iam_roles import *
import provisioners
import ansible_runner
import paramiko

with open('userdata/jumpbox.userdata') as f:
    user_data_template = Template(f.read())

user_data = user_data_template.render(hostname='jumpbox.pod.lab', pubkey=key.public_key_openssh)

jumpbox = aws.ec2.Instance('jumpbox.pod.lab',
    instance_type=flavour_jumpbox,
    ami=ami_ubuntu,
    availability_zone=zone_names.apply(lambda names: names[0]),
    vpc_security_group_ids=[jumpbox_sg.id], 
    subnet_id = subnet_infra.id,
    associate_public_ip_address=True,
    iam_instance_profile= jumpbox_iam_profile.id,
    source_dest_check=False,
    user_data = user_data,
    key_name=keypair.id,
    root_block_device={
    'volume_type': "standard",
    'volume_size': vol_size_ubuntu,
    'delete_on_termination': True
    },
    tags={
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack(),
    'Name': 'jumpbox.pod.lab',
    'Owner': owner
    })


# conn = provisioners.ConnectionArgs(
#     host=jumpbox.public_ip,
#     username='ubuntu',
#     private_key=key.private_key_pem
# )

# ansible_runner.run_async(playbook="provisioning/provision_jumpbox.yml", 
#                           ssh_key="aviKubernetes_pkey.pem",
#                           limit=jumpbox.public_ip,
#                           quiet=False)

pulumi.export('public_ip', jumpbox.public_ip)
pulumi.export('public_dns', jumpbox.public_dns)