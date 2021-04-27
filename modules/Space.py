from botocore.exceptions import ClientError
import boto3
import os


# All Digital ocean space related data and functionalities will be found here.

class Space:

    def __init__(self):

        self.secret_key = "N5a/WYshxYJhx3oO++9SKbPvZYV9ECFo5u1ghTPXTU0"
        self.access_key = "MJVCPSNGJL4DXCI53TRL"
        self.endpoint = "https://divitemplates.nyc3.digitaloceanspaces.com"
        self.bucket = "divi_templates"
        self.proxy = f"https://divitemplates.nyc3.digitaloceanspaces.com/{self.bucket}/"

        # creating an space session when the class initiates
        self.client = self.create_session()

    # Will create a space session and provide client object
    # to interact with - if needed
    def upload(self, path, public_id, c_type) -> bool:

        try:

            response = self.client.upload_file(
                path,
                self.bucket,
                public_id,
                ExtraArgs={'ACL': 'public-read', 'ContentType': c_type}
            )

        except ClientError:
            return False

        return True

    # will upload the file on the given path in space
    # name of the file refer-ed to the CDN
    def create_session(self):

        # creating a session
        space_session = boto3.session.Session()
        client = space_session.client('s3',
                                      region_name="nyc3",
                                      endpoint_url='https://divitemplates.nyc3.digitaloceanspaces.com',
                                      aws_access_key_id=self.access_key,
                                      aws_secret_access_key=self.secret_key
                                      )
        return client
