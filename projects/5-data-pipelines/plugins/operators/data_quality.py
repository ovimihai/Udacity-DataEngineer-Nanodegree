from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 checks=[],
                 redshift_conn_id="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.checks = checks
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        if len(self.checks) <= 0:
            raise ValueError('No data quality checks')
        
        redshift_hook = PostgresHook(self.redshift_conn_id)
        error_count = 0
        failing_tests = []
        
        for check in self.checks:
            sql = check.get('sql_check')
            expected_result = check.get('expected_result')
            operation = check.get('operation', 'eq')

            try:
                self.log.info(f"Running query: {sql}")
                records = redshift_hook.get_records(sql)[0]
            except Exception as e:
                self.log.info(f"Query failed with exception: {e}")
            
            print(records[0])
            
            if operation == 'eq': # result has to be equal to the expected_result
                if not (expected_result == records[0]):
                    error_count += 1
                    failing_tests.append(sql)
            elif operation == 'gt': # result has to be greater than ecpected_result
                if not (records[0] > expected_result):
                    error_count += 1
                    failing_tests.append(sql)

        if error_count > 0:
            self.log.info('Tests failed')
            self.log.info(failing_tests)
            raise ValueError('Data quality check failed')
        else:
            self.log.info("All data quality checks passed")