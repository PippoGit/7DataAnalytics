import csv

#parse function
# input_file: csv source
# output_file: modified file with fixed columns

def parse(input_file, output_file):
    fieldnames = ["machine", "metric", "timestamp", "value"];
    rows = []

    with open(input_file, 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        next(reader, None)

        for row in reader:
            id, metric = row[0].split('.')
            rows.append([id, metric, row[1], row[2]])

    with open(output_file, 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in rows:
            writer.writerow({"machine":row[0], "metric":row[1], "timestamp":row[2], "value":row[3]})

# main
if __name__ == '__main__':
    parse("csv/fplog.csv", "csv/newlog.csv")
