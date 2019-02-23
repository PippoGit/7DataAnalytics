import csv
import os
import datetime

def load_fplog_for_shift(machine_id, shift):
    input_file = "machine" + machine_id + ".csv"
    fields = ["TIMESTAMP", "NODATA", "STATUS", "DATE_SHIFT"]
    output_file = "machine" + machine_id + "best_shift_log.csv"
    rows = []

    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
            if row[3] in shift:
                rows.append(row)

    with open(output_file, "w") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(fields)
        for row in rows:
            writer.writerow(row)

    print("\nLog created!\nPath: " + os.getcwd() + os.sep + output_file + "\n")
    return rows


def status_name(id):
    if (id == 'NaN'): 
        return 'NO DATA'
    names = ['NO DATA', 'STEADY STOP', 'STOP', 'STEADY RESTART', 'RESTART', 'STEADY DELAY', 'DELAY', 'STEADY RISING', 'RISING', 'STEADY NORMAL', 'NORMAL', 'PERSISTENT NODATA', 'PERSISTENT STEADY STOP', 'PERSISTENT STOP', 'PERSISTENT STEADY RESTART', 'PERSISTENT RESTART', 'PERSISTENT STEADY DELAY', 'PERSISTENT DELAY', 'PERSISTENT STEADY RISING', 'PERSISTENT RISING', 'PERSISTENT STEADY NORMAL', 'PERSISTENT NORMAL']
    return names[int(id)-1]


def get_adjusted_status(machine_id, status_id):
    status_maps = {
        'NO DATA'                   : {'1':'NO DATA'              , '2':'NO DATA',           '4':'NO DATA'                },
        'STEADY STOP'               : {'1':'STEADY STOP'          , '2':'STEADY STOP',       '4':'STEADY STOP'            },
        'STOP'                      : {'1':'STOP'                 , '2':'STOP',              '4':'STOP'                   },
        'STEADY RESTART'            : {'1':'STEADY RESTART'       , '2':'RESTART',           '4':'STEADY RESTART'         },
        'RESTART'                   : {'1':'RESTART'              , '2':'RESTART',           '4':'RESTART'                }, 
        'STEADY DELAY'              : {'1':'STEADY DELAY'         , '2':'STEADY DELAY',      '4':'STEADY DELAY'           },
        'DELAY'                     : {'1':'DELAY'                , '2':'DELAY',             '4':'DELAY'                  },
        'STEADY RISING'             : {'1':'RISING'               , '2':'RISING',            '4':'STEADY RISING'          }, 
        'RISING'                    : {'1':'RISING'               , '2':'RISING',            '4':'RISING'                 },
        'STEADY NORMAL'             : {'1':'NORMAL'               , '2':'STEADY NORMAL',     '4':'NORMAL'                 },
        'NORMAL'                    : {'1':'NORMAL'               , '2':'NORMAL',            '4':'NORMAL'                 },
        'PERSISTENT NODATA'         : {'1':'PERSISTENT NODATA'    , '2':'PERSISTENT NODATA', '4':'PERSISTENT NODATA'      },
        'PERSISTENT STEADY STOP'    : {'1':'STEADY STOP'          , '2':'STEADY STOP',       '4':'PERSISTENT STEADY STOP' },
        'PERSISTENT STOP'           : {'1':'PERSISTENT STOP'      , '2':'STOP',              '4':'PERSISTENT STOP'        },
        'PERSISTENT STEADY RESTART' : {'1':'RESTART'              , '2':'RESTART',           '4':'STEADY RESTART'         },
        'PERSISTENT RESTART'        : {'1':'PERSISTENT RESTART'   , '2':'RESTART',           '4':'PERSISTENT RESTART'     },
        'PERSISTENT STEADY DELAY'   : {'1':'STEADY DELAY'         , '2':'STEADY DELAY',      '4':'STEADY DELAY'           },
        'PERSISTENT DELAY'          : {'1':'PERSISTENT DELAY'     , '2':'DELAY',             '4':'DELAY'                  },
        'PERSISTENT STEADY RISING'  : {'1':'RISING'               , '2':'RISING',            '4':'STEADY RISING'          },
        'PERSISTENT RISING'         : {'1':'RISING'               , '2':'RISING',            '4':'RISING'                 },
        'PERSISTENT STEADY NORMAL'  : {'1':'NORMAL'               , '2':'STEADY NORMAL',     '4':'NORMAL'                 },
        'PERSISTENT NORMAL'         : {'1':'NORMAL'               , '2':'NORMAL',            '4':'NORMAL'                 }
    }
    return status_maps[status_name(status_id)][machine_id]


def load_with_shift(machine_id, first_year=2018, first_month=11, first_day=1):
    """Function to parse status log of machine (log file must be in data/status_log/biweekly/machineID.csv)
    and to append two columns: DATE and SHIFT. Default first date is 2018-11-01

    :param machine_id: number of machine
    """
    input_file = "../data/status_log/monthly/machine" + machine_id + ".csv"
    fields = ["TIMESTAMP", "NODATA", "STATUS", "DATE_SHIFT"] # NEL CSV ORA CI SONO: TIMESTAMP,NODATA,CASE,STATUS,VELOCITY
    rows = []

    # first date used to evaluate working_date
    first_date = datetime.datetime(first_year, first_month, first_day)

    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        next(reader)
        for row in [r for r in reader if r[2] not in ['NaN', '1', '12']]: # Skip NoData
            # Get date for i-th entry
            currdate = datetime.datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%S")
            # evaluate the right shift value (1 => 06->14, 2 => 14->22, 3 => 22->06)
            shift = 1 if (currdate.hour in range(6,14)) else (2 if currdate.hour in range(14,22) else 3)
            # evaluate the working date (first day is number 0)
            working_date = abs(currdate - first_date).days + (0 if (shift == 3 and currdate.hour < 22) else 1)
            # add the extended row to the dictionary
            date_shift = str(working_date).zfill(3)+ "_" + str(shift)
            # put all together and map the status to the correct one
            rows.append(dict(zip(fields, [*row[0:2], get_adjusted_status(machine_id, row[2]), date_shift])))
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
    
    load_fplog_for_shift("1", ["004_2", "004_3", "007_3", "016_3", "023_3", "005_3", "006_3", "018_2", "021_3", "024_2"])
    load_fplog_for_shift("2", ["001_2", "006_2", "007_1", "007_2", "010_3", "014_1", "018_1", "024_3", "026_2", "030_2"])
    load_fplog_for_shift("4", ["007_1", "010_2", "012_1", "014_1", "016_2", "016_3", "019_1", "019_3", "021_1", "030_1"])
    
    return 0


if __name__ == '__main__':
    main()
