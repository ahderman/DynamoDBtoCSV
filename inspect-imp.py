import csv
import sys
import json
from datetime import datetime, timedelta, timezone
from dateutil import tz

max_rows = 10

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        try:
            if i == 0:
                print("skipping", row)
                continue
            if i > max_rows:
                break
            if len(row) < 12:
                print("skipping", row)
                continue
            # if row[1] == "":
                # print("no listing", row)
                # continue
            # if row[3] != "":
                # print("expires", row)
                # continue
            if row[1] == "LISTING_ENRICHED" or row[1] == 'LISTING':
                print("skipping", row)
                continue
            # listing = json.loads(row[1])
            # listing = json.loads(row[13])

            # isDeleted = (row[11] == 'true')
            # wasPublished = (row[6] == 'false')

            # try:
            #     createdAt = datetime.fromisoformat(row[1])
            # except ValueError as e:
            #     createdAt = datetime.strptime(row[1], '%Y-%m-%dT%H:%M:%S.%fZ')
            #     createdAt = createdAt.replace(tzinfo=timezone.utc)

            # try:
            #     updatedAt = datetime.fromisoformat(row[5])
            # except ValueError as e:
            #     updatedAt = datetime.strptime(row[5], '%Y-%m-%dT%H:%M:%S.%fZ')
            #     updatedAt = updatedAt.replace(tzinfo=timezone.utc)

            # timeOnline = updatedAt - createdAt

            # try:
            #     if isDeleted and wasPublished and timeOnline < timedelta(hours=1):
            #         print('listingId:', row[9], 'createdAt:', createdAt, 'updatedAt:', updatedAt, 'timeOnline:', timeOnline)
            # except TypeError as e:
            #     print('Error:', row[1], row[5])
            #     continue

        except Exception as e:
            print(row)
            raise e
