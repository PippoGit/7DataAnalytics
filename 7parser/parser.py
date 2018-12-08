import csv
# import time


def parse(input_file, output_file):
    """

    :param input_file: csv source
    :param output_file: modified file with fixed columns (should be sorted by timestamp)
    """
    fields = ["machine", "metric", "timestamp", "value"]
    rows = []

    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        next(reader)

        for row in reader:
            machine, metric = row[0].split('.')
            rows.append([machine, metric, row[1], row[2]])

        # rows.sort(key=lambda x: time.mktime(time.strptime(x[2],"%Y-%m-%d %H:%M:%S")))
        rows.sort(key=lambda x: x[2])

    with open(output_file, 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()

        for row in rows:
            writer.writerow(dict(zip(fields, row)))


# main
if __name__ == '__main__':
    parse("./csv/fplog.csv", "./csv/newlog.csv")
