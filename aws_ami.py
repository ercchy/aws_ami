from argparse import ArgumentParser


parser = ArgumentParser(description='Process data to make new ec2 instance for the purpose of creating ami')


parser.add_argument('-k', '--access-key', dest='key_id', action='store',
                   default=None, type=str, required=True,
                   help='Get the aws access key value')

parser.add_argument('-w', '--secret-key', dest='secret_key', action='store',
                   default=None, type=str,  required=True,
                   help='Get the aws secret key value')

parser.add_argument('-r', '--region', dest='region', action='store',
                   default='eu-west-1', type=str,
                   help='Set the region (default: eu-west-1)')

parser.add_argument('-a', '--ami-id', dest='ami_id', action='store',
                   default='ami-c37474b7', type=str,
                   help='Set the ami-id (default: ami-c37474b7)')

parser.add_argument('-n', '--key-name', dest='key_name', action='store',
                   default=None, type=str, required=True,
                   help='Set the <key_name>.pem key name (default: None)')

parser.add_argument('-t', '--type', dest='type', action='store',
                   default='m1.micro', type=str,
                   help='Set the instance type (default: m1.micro)')

parser.add_argument('-s', '--security', dest='security', action='store',
                   default=[], nargs='+', type=str,
                   help='Set the security list (default: empty list)')

parser.add_argument('--file', '-f',
                     dest='user_data',  required=True,
                     help='The content of a message.')


args = parser.parse_args()

print
print 'AWS_ACCESS_KEY_ID:     ', args.key_id
print 'AWS_SECRET_ACCESS_KEY: ', args.secret_key
print 'AWS_REGION:            ', args.region
print 'AMI_ID:                ', args.ami_id
print 'KEY_NAME:              ', args.key_name
print 'INSTANCE_TYPE:         ', args.type
print 'SECURITY_GROUPS:       ', args.security
print 'USER_DATA:             ', args.user_data

file = open(args.user_data).read()
conn = boto.ec2.connect_to_region(args.region,
    aws_access_key_id=args.key_id,
    aws_secret_access_key=args.secret_key)

print 'Creating instance ...'

reservation = conn.run_instances(
    args.ami_id,
    key_name=args.key_name,
    instance_type=args.type,
    security_groups=args.security,
    user_data=file)

print 'Instance created ...'

instance = reservation.instances[0]

status = instance.update()
while status == 'pending':
    print 'Waiting for instance to start ...'
    time.sleep(10)
    status = instance.update()

print 'Instance up and running ...'

instance.add_tag('Name', 'new-ami')

print 'Tag applied to instance ...'
print 'Connect to instance %s and check cloud-init.log' % instance.public_dns_name
