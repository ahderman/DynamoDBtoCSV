import csv
import sys
import json

max_rows = 1000000

listing_types = {}
agencies = {}

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
            # listing = json.loads(row[1])
            listing = json.loads(row[13])

            agency = listing.get('lister', {}).get('id')
            if agency not in agencies:
                agencies[agency] = 0
            agencies[agency] += 1

            # listing_type = listing.get('lister', {}).get('type')
            # if listing_type not in listing_types:
            #     listing_types[listing_type] = 0
            # listing_types[listing_type] += 1
            # if listing_type is None:
            #     print(listing['id'])

            isFromNewInsertionFunnel = listing.get("meta", {}).get("isFromNewInsertionFunnel", False)

        except Exception as e:
            print(row)
            print('listing_types so far:', listing_types)
            print('agencies so far:', agencies)
            raise e

print('listing_types:', listing_types)
print('agencies:', agencies)
