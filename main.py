from googleapiclient.discovery import build
from requests import post
import time


# ? variables for api key and webhook url
API_KEY = "---" # TODO: add your api-key
WEBHOOK_URL = "---" # TODO: add your video-id


# ? empty list for storing comment id
ids = []    


# ? main function
def main():
    api_service_name = "youtube"
    api_version = "v3"

    # ? loading credentials for Youtube API
    youtube = build(
        api_service_name, api_version, developerKey = API_KEY)

    # ? infinite loop
    while True:
        # ? calling Youtube API's to fetch information
        request = youtube.commentThreads().list(
            part="snippet",
            videoId="---", # TODO: add video's id
            maxResults=1
        )
        # ? storing the response from API in a variable
        response = request.execute()
        comment = response["items"][0]

        # ? locating required items in the response JSON and storing them in a variable
        cmt_id = comment["id"]
        cmt_author = comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        cmt_author_icon = comment["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"]
        cmt_author_channel = comment["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"]
        cmt = comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        like_count = comment["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        cmt_time = comment["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
        cmt_replies = comment["snippet"]["totalReplyCount"]

        # ? check if the comment id is not present in out ids list
        if cmt_id not in ids:
            # ? if false, create a discord webhook and send it
            data = { "content": "<@--->" } # TODO: add your discord-id
            data["embeds"] = [
                {
                    "title": f"{cmt_author} just commented!",
                    "description": cmt,
                    "fields": [
                        {
                            "name": "Number of likes",
                            "value": like_count,
                            "inline": True
                        },
                        {
                            "name": "Number of replies",
                            "value": cmt_replies,
                            "inline": True
                        },
                        {
                            "name": "Their channel",
                            "value": cmt_author_channel
                        },
                        {
                            "name": "Commented at",
                            "value": cmt_time
                        }
                    ],
                    "thumbnail": {
                        "url": cmt_author_icon
                    },
                    "color": "590610",
                }
            ]
            print(f"{cmt_author} just commented!")
            post(url=WEBHOOK_URL, json=data)
        else:
            # ? if true, continue with the loop
            continue

        # ? append the comment id into our ids list so that comments don't get repeated
        ids.append(cmt_id)

        # ? delay of 10s
        time.sleep(10)

if __name__ == "__main__":
    main()