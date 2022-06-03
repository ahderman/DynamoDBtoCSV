import csv
import sys
import json
from datetime import datetime, timedelta, timezone, date
from dateutil import tz
from collections import namedtuple

max_rows = 10000000
date_limit = datetime.fromisoformat('2021-01-01').timestamp()
listing_versions_by_object_reference = {}
ListingVersionSummary = namedtuple('ListingVersionSummary',['object_reference', 'created_at','listing_id'])
ListingSummary = namedtuple('ListingSummary',['object_reference', 'publishing_count', 'first_published_at', 'last_published_at', 'last_listing_id'])

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        try:
            if i == 0:
                # print("SKIPPING HEADER", row)
                continue
            if i > max_rows:
                break
            if len(row) < 12:
                # print("SKIPPING TOO SHORT", row)
                continue
            # if row[1] == "":
                # print("no listing", row)
                # continue
            # if row[3] != "":
                # print("expires", row)
                # continue
            if row[1] == "LISTING_ENRICHED" or row[1] == 'LISTING':
                # print("SKIPPING NOT A LISTING", row)
                continue
            # listing = json.loads(row[2])
            object_reference = row[0]
            created_at = row[1]
            listing_id = row[10]

            # isDeleted = (row[11] == 'true')
            # wasPublished = (row[6] == 'false')

            # try:
            #     createdAt = datetime.fromisoformat(row[1])
            # except ValueError as e:
            #     createdAt = datetime.strptime(row[1], '%Y-%m-%dT%H:%M:%S.%fZ')
            #     createdAt = createdAt.replace(tzinfo=timezone.utc)

            # if not row[1].startswith('2021-06'):
            #     continue

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

            if object_reference not in listing_versions_by_object_reference:
                listing_versions_by_object_reference[object_reference] = []

            listing_versions_by_object_reference[object_reference].append(ListingVersionSummary(object_reference, created_at, listing_id))

        except Exception as e:
            # print(row)
            # sorted_listings = sorted(list(listing_versions_by_object_reference.items()), key=lambda x: x[1], reverse=True)
            # for (k, v) in sorted_listings:
            #     print(k, v)
            raise e

# start with listing_versions_by_object_reference
# only keep listings with:
# - at least one version before 2021-04
# - at least version in 2021-06
# - at least 5 versions
# convert each list to ListingSummary
# print as CSV

def has_many_versions(nb_versions):
    def impl(listing_versions):
        return len(listing_versions) > nb_versions
    return impl

def has_versions_in(date_string, nb_versions):
    def impl(listing_versions):
        return len(list(filter(lambda listing_version: listing_version.created_at.startswith(date_string), listing_versions))) >= nb_versions
    return impl

def was_first_published_before(date_string):
    def impl(listing_versions):
        return any(map(lambda listing_version: listing_version.created_at < date_string, listing_versions))
    return impl

def to_listing_summary(listing_versions):
    object_reference = listing_versions[0].object_reference
    publishing_count = len(listing_versions)
    first_published_at = min(map(lambda listing_version: listing_version.created_at, listing_versions))
    last_published_at = max(map(lambda listing_version: listing_version.created_at, listing_versions))
    last_listing_id = max(map(lambda listing_version: listing_version.listing_id, listing_versions))
    return ListingSummary(object_reference, publishing_count, first_published_at, last_published_at, last_listing_id)

# listings_with_many_versions = filter(has_many_versions(5), listing_versions_by_object_reference.values())
listings_with_versions_in_2021_06 = filter(has_versions_in('2021-06', 5), listing_versions_by_object_reference.values())
listings_first_published_more_than_3_months_ago = filter(was_first_published_before('2021-04'), listings_with_versions_in_2021_06)
listing_summaries = map(to_listing_summary, listings_first_published_more_than_3_months_ago)
sorted_listing_summaries = sorted(listing_summaries, key=lambda ls: ls.publishing_count, reverse=True)
# listings_with_many_versions = filter(lambda versions: len(versions) > 5, listing_versions_by_object_reference.values())
# listings_with_versions_in_2021_06 = filter(has_version_in_2021_06, listings_with_many_versions if any(map(lambda a: a.created_at.startswith('2021-06'), versions))]
# listings_first_published_more_than_3_months_ago = [versions for versions in listings_with_many_versions if any(map(lambda a: a.created_at.startswith('2021-06'), versions))]

print(', '.join(ListingSummary._fields))
for ls in sorted_listing_summaries:
    print(', '.join(map(str, ls)))
