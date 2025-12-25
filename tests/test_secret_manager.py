from google.cloud import secretmanager
client = secretmanager.SecretManagerServiceClient()
print(client)

def access_secret(project_id, secret_id, version_id=1):
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

secret_value = access_secret("etl-test-404717","MYSQL_PUBLIC_IP_ADDRESS",version_id=5)
print("Secret value:", secret_value)