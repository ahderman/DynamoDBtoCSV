import csv
import json
import sys

def find(d, key_path):
    keys = key_path.split('.')
    rv = d
    for key in keys:
        if type(rv) is dict:
            rv = rv.get(key, "")
        else:
            rv = ""
    return rv

max_rows = 1000000000

with open("dump-2020-07-21.csv") as f:
    reader = csv.reader(f)
    writer = csv.writer(sys.stdout)
    fields = [
        ["listingId", "id"],
        ["inquiry_givenName", "lister.contacts.inquiry.givenName"],
        ["inquiry_familyName", "lister.contacts.inquiry.familyName"],
        ["inquiry_phone", "lister.contacts.inquiry.phone"],
        ["inquiry_mobile", "lister.contacts.inquiry.mobile"],
        ["lister_name", "lister.name"],
        # ["lister_legalName", "lister.legalName"],
        ["lister_phone", "lister.phone"],
        ["lister_mobile", "lister.mobile"],
        ["lister_email", "lister.email"],
        ["inquiry_email", "lister.contacts.inquiry.email"],
        ["viewing_email", "lister.contacts.viewing.email"],
    ]
    field_names = [field[0] for field in fields]
    writer.writerow(field_names)

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
            out_row = {}

            out_row = dict([[field[0], find(listing, field[1])] for field in fields])
            writer.writerow([out_row[field_name] for field_name in field_names])

            # objRef = listing.get('externalIds', {}).get('propertyReferenceId', '')

            # isFromNewInsertionFunnel = listing.get("meta", {}).get("isFromNewInsertionFunnel", False)
            # isFromNewInsertionFunnel = listing.get("lister", {}).get("id") == 'hgonew'
            # createdAt = listing.get('meta', {}).get('createdAt', '')
            # billingEmail = listing.get('lister', {}).get('billing', {}).get("email")
            # isDeleted = row[3] != ""
            # if objRef in objRefs:
            #     print("found:", objRef)
            # # if "hgonif" in objRef:
            # #     # print("starts with:", objRef, "url: http://homegate.ch/rent/{0}".format(listingId))
            # #     print(row[1])
            # #     break
            # if isFromNewInsertionFunnel:
            #     print(objRef, listingId, createdAt, billingEmail, "deleted" if isDeleted else "")
            #     # break

        except Exception as e:
            print(row)
            raise e
