import os
import uuid
import oci

def get_oci_client():
    config = {
        "user": os.environ["OCI_USER_OCID"],
        "tenancy": os.environ["OCI_TENANCY_OCID"],
        "fingerprint": os.environ["OCI_FINGERPRINT"],
        "key_file": os.environ["OCI_PRIVATE_KEY_PATH"],
        "region": os.environ["OCI_REGION"],
    }
    return oci.object_storage.ObjectStorageClient(config), config

object_storage_client, oci_config = get_oci_client()

def upload_book_image(file, book_id):
    namespace = os.environ["OCI_NAMESPACE"]
    bucket = os.environ["OCI_BUCKET_NAME"]

    object_name = f"books/{book_id}/{uuid.uuid4()}_{file.filename}"

    object_storage_client.put_object(
        namespace_name=namespace,
        bucket_name=bucket,
        object_name=object_name,
        put_object_body=file.stream,
        content_type=file.content_type
    )

    object_url = (
        f"https://objectstorage.{oci_config['region']}.oraclecloud.com"
        f"/n/{namespace}/b/{bucket}/o/{object_name}"
    )

    return object_name, object_url
