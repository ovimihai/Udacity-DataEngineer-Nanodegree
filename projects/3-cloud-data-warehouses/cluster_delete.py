import boto3
import configparser
import time


def delete_cluster(redshift, DWH_CLUSTER_IDENTIFIER):
    """Delete Redshift cluster
    
    Args:
        redshift: Redshift resource
        DWH_CLUSTER_IDENTIFIER: Redshift cluster identifier
        
    Returns:
        myClusterProps: Redshift cluster properties
    """
    print("Delete the cluster " + DWH_CLUSTER_IDENTIFIER)

    try:
        redshift.delete_cluster( ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,  SkipFinalClusterSnapshot=True)
    except Exception as e:
            print(e)

    print("Waiting for cluster to be deleted")
    while True:
        try:
            myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
            if (myClusterProps['ClusterStatus'] == 'deleting'):
                print('.', end='', flush=True)
            time.sleep(5)
        except Exception as e:
            break
    print("")
    print("Cluster is deleted")
    
    return myClusterProps

def cleanup(iam, DWH_IAM_ROLE_NAME, DWH_VPC_ID):
    """Cleanup IAM role
    
    Args:
        iam: IAM resource
        DWH_IAM_ROLE_NAME: IAM role name
    """

    print("Detach IAM role")
    try:
        iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME,  PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
    except Exception as e:
        print(e)

    print("Delete IAM role")
    try:
        iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
    except Exception as e:
        print(e)

        
def close_ports(ec2, DWH_VPC_ID, DWH_PORT):
    """Close ports for cluster
    
    Args:
        ec2: EC2 resource
        DWH_VPC_ID: Virtual private cloud id
        DWH_PORT: Cluster port
    """
    
    print("Delete VPC ports")
    try:
        vpc = ec2.Vpc(id=DWH_VPC_ID)
        defaultSg = list(vpc.security_groups.all())[0]
        defaultSg.revoke_ingress(
            GroupName=defaultSg.group_name,
            CidrIp='0.0.0.0/0',
            IpProtocol='TCP',
            FromPort=int(DWH_PORT),
            ToPort=int(DWH_PORT)
        )
    except Exception as e:
        print(e)

def main():
    
    ## setup configuration
    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))

    KEY                    = config.get('AWS','KEY')
    SECRET                 = config.get('AWS','SECRET')

    DWH_CLUSTER_TYPE       = config.get("DWH","DWH_CLUSTER_TYPE")
    DWH_NUM_NODES          = config.get("DWH","DWH_NUM_NODES")
    DWH_NODE_TYPE          = config.get("DWH","DWH_NODE_TYPE")
    DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
    DWH_DB                 = config.get("CLUSTER","DB_NAME")
    DWH_DB_USER            = config.get("CLUSTER","DB_USER")
    DWH_DB_PASSWORD        = config.get("CLUSTER","DB_PASSWORD")
    DWH_PORT               = config.get("CLUSTER","DB_PORT")
    DWH_VPC_ID             = config.get("DWH","vpc_id")
    DWH_IAM_ROLE_NAME      = config.get("DWH", "DWH_IAM_ROLE_NAME")

    #Create all needed resources
    ec2 = boto3.resource('ec2', region_name="us-west-2", aws_access_key_id=KEY, aws_secret_access_key=SECRET )

    iam = boto3.client('iam',aws_access_key_id=KEY, aws_secret_access_key=SECRET, region_name='us-west-2' )

    redshift = boto3.client('redshift',
                           region_name="us-west-2",
                           aws_access_key_id=KEY,
                           aws_secret_access_key=SECRET
                           )
    
    delete_cluster(redshift, DWH_CLUSTER_IDENTIFIER)
        
    cleanup(iam, DWH_IAM_ROLE_NAME, DWH_VPC_ID)
    
    close_ports(ec2, DWH_VPC_ID, DWH_PORT)
    
    
    
    
if __name__ == "__main__":
    main()