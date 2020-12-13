from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'    
    copy_sql = """
        COPY {} FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        REGION AS '{}'
        FORMAT AS {}
        {}
        ;
    """

    @apply_defaults
    def __init__(self,
                 table="",
                 s3_bucket="",
                 s3_path="",
                 input_format="",
                 extra_params="",
                 redshift_conn_id="redshift",
                 aws_credentials_id="aws_credentials",
                 region="us-west-2",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_path = s3_path
        self.input_format = input_format
        self.extra_params = extra_params
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.region = region
        
    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info(f"Copying data from S3 to Redshift staging {self.table} table")
        
        s3_path = f"s3://{self.s3_bucket}/{self.s3_path}"

        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.region,
            self.input_format,
            self.extra_params
        )
        
        self.log.info(f"Executing query to copy data from '{s3_path}' to '{self.table}'")
        
        redshift.run(formatted_sql)
