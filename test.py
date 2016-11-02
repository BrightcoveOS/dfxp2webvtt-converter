import requests
import json
import caption_converter
import subprocess
import urllib
import sys
import requests
import json
import argparse

# enter Videocloud Account ID
pub_id = "5092057275001"
# Enter Client ID
client_id = "cd6fd6b0-e40f-468b-8f35-44399c37c461"
# Enter Client Secret
client_secret = "B9CpltrfRokv4qJBQxP0yASHJcrTSu9PsLWSbVFlyIH1d3Ayuk5cPIvn7Ea5rGWfNix8gUsEGIxw8LsRFY_tKQ"
#default URL for oAuth token generation
access_token_url = "https://oauth.brightcove.com/v3/access_token"
# enter MAPI token
MAPItoken= "Tvrz38jBhbSv0rInBzytXVOduGEyZNOsA3kzoi6lupv4NtVOB7VAQw.."
vidId={}

#get token and return in header syntax for furture API calls
def get_authorization_headers():
    access_token = None
    r = requests.post(access_token_url, params="grant_type=client_credentials", auth=(client_id, client_secret), verify=False)
    if r.status_code == 200:
        access_token = r.json().get('access_token')
        print(access_token)
    return { 'Authorization': 'Bearer ' + access_token, "Content-Type": "application/json" }


def get_upload_location_and_upload_file(account_id, video_id, source_filename):

    # Perform an authorized request to obtain a file upload location
    url = ("https://cms.api.brightcove.com/v1/accounts/{pubid}/videos/{videoid}/upload-urls/{sourcefilename}").format(pubid=pub_id, videoid=video_id, sourcefilename=source_filename)
    r = requests.get(url, headers=get_authorization_headers())
    upload_urls_response = r.json()

    # Upload the contents of our local file to the location provided via HTTP PUT
    # This is not recommended for large files
    with open(source_filename) as fh:
        s = requests.put(upload_urls_response['signed_url'], data=fh.read())

    return upload_urls_response

# di_request makes the Ingest API call to populate a video with transcoded renditions
# from the source file that was uploaded in the previous step
def di_request(video_id, upload_urls_response):
    url = ("https://ingest.api.brightcove.com/v1/accounts/{pubid}/videos/{videoid}/ingest-requests").format(pubid=pub_id, videoid=video_id)
    data = '''{"text_tracks": [{ "url": "''' + upload_urls_response['api_request_url'] + '''","srclang": "en","kind": "captions","label": "EN","default": true }]}'''
    r = requests.post(url, headers=get_authorization_headers(), data=data)
    return r.json()

def get_old_captions():
    url = ('http://api.brightcove.com/services/library?command=search_videos&page_size=1000&video_fields=id%2Ccaptioning&media_delivery=default&sort_by=DISPLAY_NAME%3AASC&page_number=0&get_item_count=true&token={token}').format(token=MAPItoken)
    #get videos that have old captions
    response = requests.get(url)
    data = dict(json.loads(response.content))
    data = data["items"]
    data1 = {}
    #for each video that has old style captions
    for item in data:
        Id = item.get("id")
        caption = item.get("captioning")
        if caption is not None:
            #get specific video ID
            data1['id']=Id
            data1['caption']=caption['captionSources'][0]['url']
            #get caption url
            url=caption['captionSources'][0]['url']
            n=json.dumps(data1)
            data1.clear()
            data1 = json.loads(n)
            #print(data1)
            #dump old caption into local file
            testfile = urllib.URLopener()
            testfile.retrieve(url, "file.dfxp")
            vidId=str(Id)
            file1=str(Id)+".vtt"
            #run pycaption to convert to webvtt
            command = ["pycaption", "file.dfxp", "--webvtt"]
            with open(file1, 'a+') as f:
                subprocess.call(command, stdout=f);
            #get url to push new caption file to
            upload_urls = get_upload_location_and_upload_file(pub_id, vidId, file1)
            #push caption to video
            print di_request(vidId, upload_urls)

if __name__ == '__main__':
    #run the process
    get_old_captions()
