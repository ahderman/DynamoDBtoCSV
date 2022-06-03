import csv
import sys
import json

def pick(d, keys_to_pick):
    return { k: d[k] for k in d.keys() if k in keys_to_pick }

max_rows = 1000000

# listing_types = {}
# agencies = {}

insertions_with_no_username = []

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    header = []
    for i, row in enumerate(reader):
        try:
            if i == 0:
                header = row
                continue
            if i > max_rows:
                break
            if len(row) < 30:
                continue

            row_as_map = dict(zip(header, row))
            try:
                row_as_map['listing'] = json.loads(row_as_map['listing'])
            except json.decoder.JSONDecodeError as e:
                # print('Failed to parse listing data:', row_as_map['listing'])
                continue

            listing = row_as_map['listing']

            username = listing.get('lister', {}).get('username')
            # PK = row[16]
            # SK = row[12]
            # status = row[4]

            # 

            if username is None:
                # print(insertion_data)
                insertion_data = pick(row_as_map, ['PK', 'SK', 'status'])
                insertions_with_no_username.append(insertion_data)

            # agency = listing.get('lister', {}).get('id')
            # if agency not in agencies:
            #     agencies[agency] = 0
            # agencies[agency] += 1

            # obj_ref = listing.get('externalIds', {}).get('propertyReferenceId')
            # if obj_ref == 'hgoj#hgoj3056865##':
            #     print(listing)

            # listing_type = listing.get('lister', {}).get('type')
            # if listing_type not in listing_types:
            #     listing_types[listing_type] = 0
            # listing_types[listing_type] += 1
            # if listing_type is None:
            #     print(listing['id'])

            # isFromNewInsertionFunnel = listing.get("meta", {}).get("isFromNewInsertionFunnel", False)

        except Exception as e:
            print(row)
            # print('listing_types so far:', listing_types)
            # print('agencies so far:', agencies)
            print(json.dumps(insertions_with_no_username))
            raise e

# print('listing_types:', listing_types)
# print('agencies:', agencies)
print(json.dumps(insertions_with_no_username))
