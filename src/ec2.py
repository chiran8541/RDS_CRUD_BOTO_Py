RDS_Security_group_name = 'my-rds-public-sg'
class EC2:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ec2 """

    def create_security_group(self):
        print('creating the security group with name : ', RDS_Security_group_name)
        return self._client.create_security_group(
            GroupName=RDS_Security_group_name,
            Description='RDS security got public access',
            VpcId='vpc-cdd261b0'
        )

    def add_inbound_rule_to_SG(self, security_group_id):
        print('adding inbound access rule to security group: ' + security_group_id)
        self._client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 5432,
                    'ToPort': 5432,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]

                }
            ]
        )
