import csv
import sys
import json

max_rows = 100000
listings_with_movie_attachment = []
listings_with_youtube_url = []

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        try:
            if i == 0:
                continue
            if i > max_rows:
                break
            if len(row) == 1:
                continue
            if row[1] == "":
                # print("no listing", row)
                continue
            if row[3] != "":
                # print("expires", row)
                continue
            listing = json.loads(row[1])

            attachments = listing.get('localization', {}).get('de', {}).get('attachments', [])
            has_movie_attachment = ([a for a in attachments if a['type'] == 'MOVIE']) != []
            urls = listing.get('localization', {}).get('de', {}).get('urls', [])
            has_youtube_url = ([u for u in urls if u['type'] == 'YOUTUBE']) != []
            has_youtube_url = ([u for u in urls if (u['type'] == 'YOUTUBE' and 'youtu' not in u['value'])]) != []

            if has_movie_attachment:
                listings_with_movie_attachment.append(listing['id'])
            if has_youtube_url:
                youtube_url = [u for u in urls if u['type'] == 'YOUTUBE'][0]['value']
                listings_with_youtube_url.append([listing['id'], youtube_url])

        except Exception as e:
            print(row)
            print('listings_with_movie_attachment so far:', listings_with_movie_attachment)
            print('listings_with_youtube_url so far:', listings_with_youtube_url)
            raise e

# print('listings_with_movie_attachment:', ['https://www.homegate.ch/buy/' + id for id in listings_with_movie_attachment])
print('listings_with_youtube_url:', [ ['https://www.homegate.ch/buy/' + id, url] for (id, url) in listings_with_youtube_url])
