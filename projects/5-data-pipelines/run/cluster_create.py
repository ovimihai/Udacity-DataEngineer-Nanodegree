import pandas as pd
import boto3
import json
import time
import configparser
from botocore.exceptions import ClientError


def create_role(iam, DWH_IAM_ROLE_NAME):
    """Create iam role for Redshift and allow it to use AWS
    
    Args:
        iam: The AWS iam resource
        DWH_IAM_ROLE_NAME: The iam role name string
    
    Returns:
        An iam role ARN used in the cluster start procedure
    """

    #1.1 Create the role, 
    try:
        print("1.1 Creating a new IAM Role") 
        dwhRole = iam.create_role(
            Path='/',
            RoleName=DWH_IAM_ROLE_NAME,
            Description = "Allows Redshift clusters to call AWS services on your behalf.",
            AssumeRolePolicyDocument=json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                   'Effect': 'Allow',
                   'Principal': {'Service': 'redshift.amazonaws.com'}}],
                 'Version': '2012-10-17'})
        )    
    except Exception as e:
        print(e)


    print("1.2 Attaching Policy")

    iam.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME,
                           PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                          )['ResponseMetadata']['HTTPStatusCode']

    print("1.3 Get the IAM role ARN")
    roleArn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']
    
    return roleArn

def create_redshift_cluster(redshift, roleArn, DWH_CLUSTER_IDENTIFIER, DWH_CLUSTER_TYPE, 
                            DWH_NODE_TYPE, DWH_NUM_NODES, DWH_DB, DWH_DB_USER, DWH_DB_PASSWORD):
    """Create the Redshift Cluster
    
    Args:
        redshift: Redshift AWS resource
        roleArn: IAM role ARN
        DWH_CLUSTER_IDENTIFIER: The cluster identifier string
        DWH_CLUSTER_TYPE: The cluster type
        DWH_NODE_TYPE: The node tyoe
        DWH_NUM_NODES: The cluster number of nodes
        DWH_DB: The database name
        DWH_DB_USER: The datbase username
        DWH_DB_PASSWORD: The database password
    
    Returns:
        The Redshift cluster properties
    """
    print("2.1 Creating Redshift cluster")

    try:
        response = redshift.create_cluster(        
            #HW
            ClusterType=DWH_CLUSTER_TYPE,
            NodeType=DWH_NODE_TYPE,
            NumberOfNodes=int(DWH_NUM_NODES),

            #Identifiers & Credentials
            DBName=DWH_DB,
            ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
            MasterUsername=DWH_DB_USER,
            MasterUserPassword=DWH_DB_PASSWORD,

            #Roles (for s3 access)
            IamRoles=[roleArn]  
        )
    except Exception as e:
        print(e)
    
    print("2.2 Waiting for cluster to be available")
    myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
    while myClusterProps['ClusterStatus'] != 'available':
        time.sleep(5)
        myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
        print('.', end='', flush=True)

    print("")
    print("2.3 Redshift cluster is ready")
    
    return myClusterProps
    
def update_local_config(myClusterProps):
    """Update local config with Cluster host, iamrole and vpc_id
    
    Args:
        myClusterProps: Redshift cluster properties
    """

    print("3.1 Updating config with new cluster")
    # update config file with cluster data
    config = configparser.ConfigParser()
    config.read("dwh.cfg")

    config.set("CLUSTER","HOST", myClusterProps['Endpoint']['Address'])
    config.set("IAM_ROLE","ARN", myClusterProps['IamRoles'][0]['IamRoleArn'])
    config.set("DWH","VPC_ID", myClusterProps['VpcId'])

    cfgfile = open("dwh.cfg",'w+')
    config.write(cfgfile)
    cfgfile.close()

def open_ports(ec2, myClusterProps, DWH_PORT):
    
    print("3.2 Open ports")
    try:
        vpc = ec2.Vpc(id=myClusterProps['VpcId'])
        defaultSg = list(vpc.security_groups.all())[0]

        defaultSg.authorize_ingress(
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
    DWH_IAM_ROLE_NAME      = config.get("DWH", "DWH_IAM_ROLE_NAME")


    #Create all needed resources
    ec2 = boto3.resource('ec2', region_name="us-west-2", aws_access_key_id=KEY, aws_secret_access_key=SECRET )
    s3 = boto3.resource('s3', region_name="us-west-2", aws_access_key_id=KEY, aws_secret_access_key=SECRET )
    iam = boto3.client('iam',aws_access_key_id=KEY, aws_secret_access_key=SECRET, region_name='us-west-2' )
    redshift = boto3.client('redshift', region_name="us-west-2", aws_access_key_id=KEY, aws_secret_access_key=SECRET )
    
    roleArn= create_role(iam, DWH_IAM_ROLE_NAME)
    
    myClusterProps = create_redshift_cluster(redshift, roleArn, DWH_CLUSTER_IDENTIFIER, DWH_CLUSTER_TYPE, 
                            DWH_NODE_TYPE, DWH_NUM_NODES, DWH_DB, DWH_DB_USER, DWH_DB_PASSWORD)
    
    update_local_config(myClusterProps)
    
    open_ports(ec2, myClusterProps, DWH_PORT)
    
    
if __name__ == "__main__":
    main()