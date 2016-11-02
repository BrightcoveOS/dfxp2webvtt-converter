# DFXP to WebVTT Caption Migration Tool

This Python script uses Media API to find all videos that have old style captions (ttml, dfxp) downloads the caption files and uses pycaption to convert them to WebVTT captions. It then uses the [Source File Upload API for Dynamic Ingest](http://docs.brightcove.com/en/video-cloud/di-api/guides/push-based-ingest.html) to get an S3 bucket, push the webvtt files to to the S3 bucket, and then makes Dynamic Ingestion calls to add the WebVTT captions to the correct video.

## Installation

1. Python 2.7 must be installed
2. Use the same process for installing that is detailed in https://docs.brightcove.com/en/video-cloud/brightcove-player/guides/webvtt-converter.html
3. Copy **test.py** into the same directory as the **caption-converter.py** file.
4. In **test.py** Replace the following User Variables: 
	* **pub_id** (your account id)
	* **client_id** (see step 5)
	* **client_secret** (see step 5)
	* **MAPItoken** (a Media API READ token for the account)
5. You must enable these operations for the client credentials:
![API Operations](http://learning-services-media.brightcove.com/doc-assets/video-cloud-apis/di-api/guides/push-based-ingest/api-credentials-studio2.png)

See https://support.brightcove.com/en/video-cloud/docs/managing-api-authentication-credentials for details of obtaining client credentials.