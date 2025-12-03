"""AWS S3 operations plugin."""
from ..base import PluginBase
import boto3
from pathlib import Path

class AWSS3Plugin(PluginBase):
    """AWS S3 storage operations."""
    
    name = "aws_s3"
    
    def __init__(self, params: dict, audit=None):
        super().__init__(params, audit=audit)
        self.bucket = params.get("bucket")
        self.operation = params.get("operation")  # upload, download, list, delete
        self.local_path = params.get("local_path")
        self.s3_key = params.get("s3_key")
        self.aws_access_key = params.get("aws_access_key_id")
        self.aws_secret_key = params.get("aws_secret_access_key")
        self.region = params.get("region", "us-east-1")
    
    def plan(self) -> list:
        return [{"action": f"s3_{self.operation}", "bucket": self.bucket, "key": self.s3_key}]
    
    def execute(self) -> dict:
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.region
            )
            
            if self.operation == "upload":
                s3_client.upload_file(self.local_path, self.bucket, self.s3_key)
                result = {"uploaded": self.s3_key}
            
            elif self.operation == "download":
                s3_client.download_file(self.bucket, self.s3_key, self.local_path)
                result = {"downloaded": self.local_path}
            
            elif self.operation == "list":
                response = s3_client.list_objects_v2(Bucket=self.bucket)
                result = {"objects": [obj['Key'] for obj in response.get('Contents', [])]}
            
            elif self.operation == "delete":
                s3_client.delete_object(Bucket=self.bucket, Key=self.s3_key)
                result = {"deleted": self.s3_key}
            
            if self.audit:
                self.audit.record({
                    "plugin": self.name,
                    "operation": self.operation,
                    "bucket": self.bucket
                })
            
            return {"status": "ok", "result": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}
