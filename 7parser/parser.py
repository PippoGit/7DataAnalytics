import csv
#import time

#parse function
# input_file: csv source
# output_file: modified file with fixed columns (should be sorted by timestamp)

def parse(input_file, output_file):
  fields = ["machine", "metric", "timestamp", "value"]
  rows = []

  with open(input_file, 'rb') as csv_file:
    reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    next(reader, None)

    for row in reader:
      id, metric = row[0].split('.')
      rows.append([id, metric, row[1], row[2]])

    #rows.sort(key=lambda x: time.mktime(time.strptime(x[2],"%Y-%m-%d %H:%M:%S")))
    #i think this is kinda useless, timestamps are just ISO strings, so it should be possible to sort em only
    #by doing dates.sort(), there is no need to parse date.
    rows.sort(key=lambda x: x[2]) #as long as timestamps are standard strings, i just sort em as strings (alotfaster)

  with open(output_file, 'w+') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()
    
    for row in rows:
      writer.writerow(dict(zip(fields, row)))

# main
if __name__ == '__main__':
  parse("csv/fplog.csv", "csv/newlog.csv")