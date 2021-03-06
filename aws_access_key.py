import pulumi
import pulumi_aws as aws
import pulumi_tls as tls
import pulumi_random as random
from pulumi_vars import *

pet = random.RandomPet("key")
#pet.id.apply(lambda id: f"{id}"))
key = tls.PrivateKey(id + '_pkey',
    algorithm="RSA",
    ecdsa_curve="2048"
)

pulumi.export('public_key', key.public_key_openssh)
pulumi.export('private_key', key.private_key_pem)
pulumi.Output.all([key.private_key_pem]).apply(lambda key: f'key')
key.private_key_pem.apply(lambda key: f'key')

#private_key_pem_file = open(id + '_pkey.pem', 'w')
#private_key_pem_file.write(pulumi.Output.all([key.private_key_pem]).apply(lambda key: f'key'))
#private_key_pem_file.close()

keypair = aws.ec2.KeyPair(id + '_keypair', public_key=key.public_key_openssh)


