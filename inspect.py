import csv
import sys
import json

max_rows = 10

listing_types = {}
agencies = {}
listings_with_no_username = set()

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        try:
            if i == 0:
                continue
            if i > max_rows:
                break
            if len(row) < 8:
                print("row too short", row)
                continue
            if row[1] == "":
                print("no listing", row)
                continue
            # if row[3] != "":
            #     # print("expires", row)
            #     continue
            listing = json.loads(row[1])

            listing_id = listing.get('id')
            username = listing.get('lister', {}).get('username')
            print('listing_id:', listing_id)
            print('username:', username)
            if username is None:
                listings_with_no_username.add(listing_id)

        except Exception as e:
            print(row)
            print('listings_with_no_username so far:', listings_with_no_username)
            raise e

print('listings_with_no_username:', listings_with_no_username)
