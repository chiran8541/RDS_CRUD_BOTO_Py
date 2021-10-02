from src.Client_Factory import EC2Client
from src.ec2 import EC2
RDS_DB_SUBNET_NAME = 'my-rds-subnet-group'
class RDS:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.rds """

    def create_postgres_instance(self):
        print('creating Postgres Sql instance .....')

        security_group_id = self.create_db_security_group_and_add_rules()

        #create subnet group
        self.create_rds_subnet()
        print('creating DB subnet')

        self._client.create_db_instance(
            DBName='MyPostgreSqlDB',
            DBInstanceIdentifier='mypostgresql',
            MasterUsername='postgresql',
            MasterUserPassword='postgresqlpassword',
            DBInstanceClass='db.t2.micro',
            StorageType='gp2',
            Engine='postgres',
            EngineVersion='9.6.9',
            Port=5432,

            AllocatedStorage=20,
            MultiAZ=False,
            PubliclyAccessible=True,
            VpcSecurityGroupIds=[security_group_id],
            DBSubnetGroupName=RDS_DB_SUBNET_NAME,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'My_RDS_Postgres_Instance'
                }
            ]
        )

    def create_rds_subnet(self):
        print('creating the subnet group for RDS')
        self._client.create_db_subnet_group(
            DBSubnetGroupName=RDS_DB_SUBNET_NAME,
            DBSubnetGroupDescription='My first subnet group for RDS',
            SubnetIds=['subnet-5bc4a67a', 'subnet-467e1920', 'subnet-91722b9f', 'subnet-38268d09', 'subnet-e2eed9af', 'subnet-05b2d25a']

        )

    def create_db_security_group_and_add_rules(self):
        ec2_client = EC2Client().get_client()
        ec2 = EC2(ec2_client)

        # create security group
        security_group = ec2.create_security_group()

        # get id of Security group
        security_group_id = security_group['GroupId']
        print(security_group_id)
        print(type(security_group_id))
        print('created RDS security group with ID ' + security_group_id)

        # add public access rule to sg
        ec2.add_inbound_rule_to_SG(security_group_id)
        print('added inbound public access rule to SG with ID' + security_group_id)

        return security_group_id

