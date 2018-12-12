import csv
import os

def load_fplog(input_file):
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
            rows.append([machine, metric, row[1], int(row[2])])

        # rows.sort(key=lambda x: time.mktime(time.strptime(x[2],"%Y-%m-%d %H:%M:%S")))
        rows.sort(key=lambda x: x[2])

    # with open("newlog.csv", 'w+') as csv_file:
    #     writer = csv.DictWriter(csv_file,  delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, fieldnames=fields)
    #     writer.writeheader()

    #     for row in rows:
    #         writer.writerow(dict(zip(fields, row)))
    return [fields, rows]



def time2secs(t):
    """
    convert timestamp to seconds (starting from 1)

    :param t: timestamp HH:MM:SS
    """
    return sum(int(x)*60**pow for pow, x in enumerate(t.split(':')[::-1]))



def should_write(row, sel_dates=None, sel_fields=None, sel_machines=None):
    # [r_date, r_time] = row[2].split(' ')
    return ((sel_fields is None or row[1] in sel_fields) and
           (sel_machines is None or row[0] in sel_machines) and
           (sel_dates is None or row[2].split(' ')[0] in sel_dates))


def parse(input_file, sel_dates=None, sel_fields=None, sel_machines=None):
    """
    parse and fix csv. Select by Date and attributes

    :param input_file: csv source
    :param date: date to parse (if None == ALL)
    :param sel_fields: list of attributes which should be selected (if None == ALL)
    :param sel_machiens: list of machines which should be selected (if None == ALL)

    """

    [fields, rows] = load_fplog(input_file)

    with open("selected_log.csv", "w") as csv_file:
        writer = csv.DictWriter(csv_file, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fields)

        writer.writeheader()
        for row in rows:    
            if(should_write(row, sel_dates, sel_fields, sel_machines)):
                writer.writerow(dict(zip(fields, row)))     

    print("New log at: " + os.getcwd() + "/selected_log.csv\n\n")
    return


# main
if __name__ == '__main__':
    parse("../data/fplog.csv",      # original file fplog.csv
          ["2018-11-20"],                     # dates list
          ['STATISTIC_VEL_ACTUAL'], # vars list
          ['0001'])                 # machines list
