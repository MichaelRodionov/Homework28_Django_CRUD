import csv
import json

from Homework28_Django_CRUD.settings import US_CSV, ADS_CSV, LOC_CSV, CAT_CSV, LOC_JSON, US_JSON, ADS_JSON, CAT_JSON


# ----------------------------------------------------------------
# convert csv to json function
def convert_csv_json(csv_file, json_file, model):
    data_list = []

    with open(csv_file, encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            if row.get('is_published') is not None:
                if row['is_published'] == 'TRUE':
                    row["is_published"] = True
                else:
                    row["is_published"] = False
            data_dict = {"model": model, "pk": row["id"], "fields": row}
            data_list.append(data_dict)
    with open(json_file, "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps(data_list, indent=4, ensure_ascii=False))


convert_csv_json(LOC_CSV, LOC_JSON, 'users.location')
convert_csv_json(US_CSV, US_JSON, 'users.user')
convert_csv_json(ADS_CSV, ADS_JSON, "ads.advertisement")
convert_csv_json(CAT_CSV, CAT_JSON, "ads.category")



