import pulumi
import pulumi_aws as aws
from pulumi_vars import *
from aws_infrastructure import *

ctrl_sg = aws.ec2.SecurityGroup(id + "_ctrl_sg",
    description= "Allow incoming connections to the Avi GUI",
    vpc_id=vpc.id,
    ingress=[
    {
    "fromPort": 80,
    "toPort": 80,
    "protocol": "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 443,
    "toPort":  443,
    "protocol":  "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 22,
    "toPort": 22,
    "protocol": "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 0,
    "toPort": 0,
    "protocol":  "-1",
    "cidrBlocks": ["0.0.0.0/0"],
    }
    ],
    egress=[
    {
        "fromPort": 0,
        "toPort": 0,
        "protocol": "-1",
        "cidrBlocks": ["0.0.0.0/0"],
    }
    ],
    tags={
        "Name": id + '_ctrl_sg',
    })

jumpbox_sg = aws.ec2.SecurityGroup(id + "_jumpbox_sg",
    description= "Allow incoming connections to the lab jumpbox",
    vpc_id=vpc.id,
    ingress=[
    {
    "fromPort": 53,
    "toPort": 53,
    "protocol":  "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 53,
    "toPort": 53,
    "protocol":  "udp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 22,
    "toPort": 22,
    "protocol": "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 8443,
    "toPort": 8443,
    "protocol": "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 0,
    "toPort": 0,
    "protocol":  "-1",
    "cidrBlocks": [vpc_cidr]
    }
    ],
    egress=[
    {
        "fromPort": 0,
        "toPort": 0,
        "protocol": "-1",
        "cidrBlocks": ["0.0.0.0/0"],
    }
    ],
    tags={
        "Name": id + '_jumpbox_sg',
    })

k8s_sg = aws.ec2.SecurityGroup(id + "_k8s_sg",
    description= "Allow incoming connections to the K8s env",
    vpc_id=vpc.id,
    ingress=[
    {
    "fromPort": 53,
    "toPort": 53,
    "protocol":  "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 53,
    "toPort": 53,
    "protocol":  "udp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 22,
    "toPort": 22,
    "protocol": "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 80,
    "toPort": 80,
    "protocol": "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 443,
    "toPort": 443,
    "protocol": "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 6443,
    "toPort": 6443,
    "protocol": "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 8080,
    "toPort": 8080,
    "protocol": "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 8443,
    "toPort": 8443,
    "protocol": "tcp",
    "cidrBlocks": ["0.0.0.0/0"],
    },
    {
    "fromPort": 0,
    "toPort": 0,
    "protocol":  "-1",
    "cidrBlocks": [vpc_cidr]
    }
    ],
    egress=[
    {
        "fromPort": 0,
        "toPort": 0,
        "protocol": "-1",
        "cidrBlocks": ["0.0.0.0/0"],
    }
    ],
    tags={
        "Name": id + '_k8s_sg',
    })

