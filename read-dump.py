import csv
import json

# max_rows = 10000
objRefs = [
    "hgonif#031fd274-5f34-46b6-9063-8c9eb4e36ed2##",
    "hgonif#031fd274-5f34-46b6-9063-8c9eb4e36ed2##",
    "hgonif#3ffaf3e1-a9df-4e88-aff2-d400d68138a4##",
    "hgonif#5d5da104-ef46-4855-bd02-6474970d75af##",
    "hgonif#68cce40d-e7c9-49a5-bbc8-fcaa2f90f649##",
    "hgonif#73564456-535e-4c33-8edc-cb8da7a73250##",
    "hgonif#84141883-d8e0-40ea-a74d-b92c99029a7d##",
    "hgonif#9b0897a1-5b77-4ad4-a8c4-c0ed46938c28##",
    "hgonif#a0a3f34d-5390-43c4-b91e-af36be84de3a##",
    "hgonif#a78f37af-8796-4001-8370-8ff0d8fa88fa##",
    "hgonif#e80c4741-b0a4-4a1d-b131-79f3235b332f##"
]

with open('dump.csv') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        try:
            if i == 0:
                continue
            # if i > max_rows:
            #     break
            if len(row) == 1:
                continue
            if row[1] == "":
                # print("no listing", row)
                continue
            # if row[3] != "":
            #     # print("expires", row)
            #     continue
            listing = json.loads(row[1])
            objRef = listing.get('externalIds', {}).get('propertyReferenceId', '')
            listingId = listing.get('id')
            isFromNewInsertionFunnel = listing.get("meta", {}).get("isFromNewInsertionFunnel", False)
            isFromNewInsertionFunnel = listing.get("lister", {}).get("id") == 'hgonew'
            createdAt = listing.get('meta', {}).get('createdAt', '')
            billingEmail = listing.get('lister', {}).get('billing', {}).get("email")
            isDeleted = row[3] != ""
            if objRef in objRefs:
                print("found:", objRef)
            # if "hgonif" in objRef:
            #     # print("starts with:", objRef, "url: http://homegate.ch/rent/{0}".format(listingId))
            #     print(row[1])
            #     break
            if isFromNewInsertionFunnel:
                print(objRef, listingId, createdAt, billingEmail, "deleted" if isDeleted else "")
                # break

        except Exception as e:
            print(row)
            raise e
