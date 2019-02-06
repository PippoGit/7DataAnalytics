import csv
import os
import datetime

def load_with_shift(machine_id, first_year=2018, first_month=11, first_day=15):
    """Function to parse status log of machine (log file must be in data/status_log/biweekly/machineID.csv)
    and to append two columns: DATE and SHIFT. Default first date is 2018-11-15

    :param machine_id: number of machine
    """
    input_file = "../data/status_log/biweekly/machine" + machine_id + ".csv"
    fields = ["TIMESTAMP", "VELOCITY", "STATUS", "DATE_SHIFT"]
    rows = []

    # first date used to evaluate working_date
    first_date = datetime.datetime(first_year, first_month, first_day)

    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
            # Get date for i-th entry
            currdate = datetime.datetime.strptime(row[0], "%d-%b-%Y %H:%M:%S")
            # evaluate the right shift value (1 => 06->14, 2 => 14->22, 3 => 22->06)
            shift = 1 if (currdate.hour in range(6,14)) else (2 if currdate.hour in range(14,22) else 3)
            # evaluate the working date (first day is number 0)
            working_date = abs(currdate - first_date).days + (0 if (shift == 3 and currdate.hour < 22) else 1)
            # add the extended row to the dictionary
            rows.append(dict(zip(fields, [*row, str(working_date).zfill(3)+ "_" +str(shift)])))

    return rows


def write_log(machine_id, log):
    """Create the new log for machine number machine_id    

    :param machine id: number of machine
    :param log: log file extended with shift and date

    """
    output_file = "machine" + machine_id + ".csv"

    # crete new csv file
    with open(output_file, "w") as csv_file:
        writer = csv.DictWriter(csv_file, quoting=csv.QUOTE_NONNUMERIC, fieldnames=log[0].keys())
        writer.writeheader()
        writer.writerows(log)

    print("\nLog created!\nPath: " + os.getcwd() + os.sep + output_file + "\n")
    return

# main
def main():
    # we are not going to use machine 3
    machines = ["1", "2", "4"]

    for machine in machines:
      log = load_with_shift(machine)
      write_log(machine, log)
      
    return 0


if __name__ == '__main__':
    main()