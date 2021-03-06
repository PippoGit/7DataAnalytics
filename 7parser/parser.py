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
            rows.append(dict(zip(fields, [machine, metric, row[1], int(row[2])])))
    return sorted(rows, key=lambda k: k['timestamp'])


def should_write(row, sel_dates=None, sel_fields=None, sel_machines=None):
    """
    Returns true if the row should be written on the new log
    """
    # [r_date, r_time] = row[2].split(' ')
    return ((sel_fields is None or row['metric'] in sel_fields) and
           (sel_machines is None or row['machine'] in sel_machines) and
           (sel_dates is None or row['timestamp'].split(' ')[0] in sel_dates))


def parse(input_file, sel_dates=None, sel_fields=None, sel_machines=None):
    """Returns a list of dictionaries, each containing a selected row.
    Each element of the list has the following fields: "machine", "timestamp", "metric", "value"
    

    :param input_file: csv source
    :param date: date to parse, yyyy-MM-dd format required. (To select All set it as 'None')
    :param sel_fields: list of attributes which should be selected (To select All set it as 'None')
    :param sel_machiens: list of machines which should be selected (To select All set it as 'None')

    """
    # load original dataset fplog.csv
    output_file = "selected_log.csv"
    fplog = load_fplog(input_file)

    # select the rows that should be written (from fplog)
    selected_rows = [row for row in fplog if should_write(row, sel_dates, sel_fields, sel_machines)]

    if(not selected_rows):
        raise Exception("No data found. Maybe you should check your filters.")

    # crete new csv file
    with open(output_file, "w") as csv_file:
        writer = csv.DictWriter(csv_file, quoting=csv.QUOTE_NONNUMERIC, fieldnames=selected_rows[0].keys())
        writer.writeheader()
        writer.writerows(selected_rows)

    print("\nLog created!\nPath: " + os.getcwd() + os.sep + output_file + "\n")
    return selected_rows


# main
def main():
    # filters to select only a subset of the whole dataset
    filters = {
        'sel_dates':    None,
        'sel_fields':   ["STATUS_CLOCK"],
        'sel_machines': ["0001"]
    }

    # parse output
    log = parse("../data/fplog.csv", **filters)
    
    # testing...
    print("First row:")
    print(*log[0].values(), sep=', ')

    print("\nExample: \n\tmachine => " + log[0]['machine'] + "\n\ttimestamp => " + log[0]['timestamp'])
    print("\n")
    return 0


if __name__ == '__main__':
    main()