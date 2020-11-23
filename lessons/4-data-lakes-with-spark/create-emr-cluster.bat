
aws emr create-cluster ^
--applications Name=Spark Name=Zeppelin ^
--ec2-attributes "{\"KeyName\":\"udacity-dend-spark\",\"InstanceProfile\":\"EMR_EC2_DefaultRole\"}" ^
--service-role EMR_DefaultRole ^
--enable-debugging ^
--release-label emr-5.31.0 ^
--log-uri s3n://aws-logs-633698449291-us-west-2/elasticmapreduce/ ^
--name test-spark4 ^
--instance-groups "[{\"InstanceCount\":2,\"EbsConfiguration\":{\"EbsBlockDeviceConfigs\":[{\"VolumeSpecification\":{\"SizeInGB\":32,\"VolumeType\":\"gp2\"},\"VolumesPerInstance\":1}]},\"InstanceGroupType\":\"CORE\",\"InstanceType\":\"m5.xlarge\",\"Name\":\"Core Instance Group\"},{\"InstanceCount\":1,\"EbsConfiguration\":{\"EbsBlockDeviceConfigs\":[{\"VolumeSpecification\":{\"SizeInGB\":32,\"VolumeType\":\"gp2\"},\"VolumesPerInstance\":1}]},\"InstanceGroupType\":\"MASTER\",\"InstanceType\":\"m5.xlarge\",\"Name\":\"Master Instance Group\"}]" ^
--scale-down-behavior TERMINATE_AT_TASK_COMPLETION ^
--region us-west-2

