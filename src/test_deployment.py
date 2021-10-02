from src.Client_Factory import RDSClient
from src.rds import RDS

def get_RDS():
    rds_client = RDSClient().get_client()
    rds = RDS(rds_client)
    return rds

def deploy_resource():
    get_RDS().create_postgres_instance()
    print('RDS instances created ')

if __name__ == '__main__':
    deploy_resource()

