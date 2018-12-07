import csv

def parse():
    file = "csv/fplog.csv"

    with open(file, 'rb') as csvFile:
        spamreader = csv.reader(csvFile, delimiter=',', quotechar='"')
        next(spamreader, None)
        nrow = []
        for row in spamreader:
            print row[0]
            id, metric = row[0].split('.')
            nrow.append([id, metric, row[1], row[2]])
            print nrow
            return

if __name__ == '__main__':
    parse()
