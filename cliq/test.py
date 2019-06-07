def explicit_app_engine(project):
    from google.auth import app_engine
    import googleapiclient.discovery

    # Explicitly use App Engine credentials. These credentials are
    # only available when running on App Engine Standard.
    credentials = app_engine.Credentials()

    # Explicitly pass the credentials to the client library.
    storage_client = googleapiclient.discovery.build(
        'storage', 'v1', credentials=credentials)

    # Make an authenticated API request
    buckets = storage_client.buckets().list(project=project).execute()
    print(buckets)

explicit_app_engine("zinc-advice-242819");
