import csv


def parse(input_file):
    """
    function to parse and fix csv file. The output will be saved in the script's dir as newlog.csv
    
    :param input_file: csv source
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

    with open("newlog.csv", 'w+') as csv_file:
        writer = csv.DictWriter(csv_file,  delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, fieldnames=fields)
        writer.writeheader()

        for row in rows:
            writer.writerow(dict(zip(fields, row)))
    return [fields, rows]



def time2secs(t):
    """
    convert timestamp to seconds (starting from 1)

    :param t: timestamp HH:MM:SS
    """
    return sum(int(x)*60**pow for pow, x in enumerate(t.split(':')[::-1]))



def parse_date(input_file, date, sel_fields=[], sel_machines=[]):
    """
    parse and fix csv. Select by Date and attributes

    :param input_file: csv source
    :param date: date to parse
    :param sel_fields: list of attributes which should be selected (default value ALL)
    :param sel_machiens: list of machines which should be selected (default value ALL)

    """
    [fields, rows] = parse(input_file)

    with open("log" + date + ".csv", "w") as csv_file:
        writer = csv.DictWriter(csv_file,  delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, fieldnames=fields)
        writer.writeheader()

        for row in rows:
            if((not sel_fields or row[1] in sel_fields) and (not sel_machines or row[0] in sel_machines)):
                [r_date, r_time] = row[2].split(' ')
                if(r_date == date):
                    writer.writerow({fields[0]: row[0], fields[1]:row[1], fields[2]:int(time2secs(r_time)), fields[3]: int(row[3])})        


# main
if __name__ == '__main__':
    parse_date("../data/fplog.csv", "2018-11-19", ['STATISTIC_VEL_ACTUAL'], ['0001'])
