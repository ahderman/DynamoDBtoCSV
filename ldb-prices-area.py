import csv
import sys
import json

max_rows = 100
area_values = {}

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

            area_value = listing.get('prices', {}).get('buy', {}).get('area') or listing.get('prices', {}).get('rent', {}).get('area')

            if area_value not in area_values:
                area_values[area_value] = 0
            area_values[area_value] += 1

            # listing_type = listing.get('lister', {}).get('type')
            # if listing_type not in listing_types:
            #     listing_types[listing_type] = 0
            # listing_types[listing_type] += 1
            # if listing_type is None:
            #     print(listing['id'])

        except Exception as e:
            print(row)
            print('area_values so far:', area_values)
            raise e

print('area_values:', area_values)
