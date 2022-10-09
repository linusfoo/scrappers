import os
import json
import csv
import itertools
import googleapiclient.discovery

cities= [ "singaporean" ," singaporean youtuber" , "xiaxue" ,"deekosh" , "ah boys to men" ] #"jianhao tan", "tsl", "straits time singapore", "night owl cinemetics"
keywords=[ "youtuber" ,"teacher", "lifestyle"]

def scraper(search, ids, file, DEVELOPER_KEY):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    with open(file, mode='a', encoding = "utf-8") as cfile:
        cwriter = csv.writer(cfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        request = youtube.search().list(
            part="snippet",
            maxResults=50,
            type="video,list",
            q=search,
        )
        search_response = request.execute()

        print("Youtube Results for "+ search +": " + str(search_response["pageInfo"]["totalResults"]))

        for video in search_response["items"]:
            cwriter.writerow([video['id']['videoId'],video['snippet']['title'],video['snippet']['description'],video['snippet']['channelTitle'],video['snippet']['channelId'],video['snippet']['publishedAt']])
            ids.add(video['id']['videoId'])

        while "nextPageToken" in search_response:
            request = youtube.search().list(
                part="snippet",
                maxResults=50,
                type="video,list",
                q=search,
                pageToken=search_response["nextPageToken"],
            )
            search_response = request.execute()
            for video in search_response["items"]:
                cwriter.writerow([video['id']['videoId'],video['snippet']['title'],video['snippet']['description'],video['snippet']['channelTitle'],video['snippet']['channelId'],video['snippet']['publishedAt']])
                ids.add(video['id']['videoId'])

        print("Current Number of IDs: " + str(len(ids)))

def idList():
    ids=set()

    dev_keys=[] #insert dev keys here
    with open( "data/youtube/videos_to_scrape.csv", mode='a', encoding = "utf-8") as cfile:
        for (city, key) in zip(cities, dev_keys):
            print("Running for "+city+" with key: "+key)
            cwriter = csv.writer(cfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            cwriter.writerow(["ID","Title","Description","Channel Title","Channel ID","Published Date"])
            # for keyword in keywords:
            scraper(city, ids,  "data/youtube/videos_to_scrape.csv",key)

    return ids

## END ID LIST METHOD

if __name__ == "__main__":
    idList()