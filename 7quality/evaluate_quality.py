import csv
import os
import datetime
from operator import itemgetter

def merge_frequency_oee(machine_id, first_year=2018, first_month=11, first_day=15):
    fields = ["DATE_SHIFT", "AVG_VELOCITY","LOG_PRODUCED","LOG_REJECTED", "OEE", "NORMAL_FREQUENCY"],

    quality_file = "../data/quality_log/machine" + machine_id + "_shiftquality.csv"
    freq_file    = "../data/quality_log/machine" + machine_id + "_shiftfrequency.csv"
    first_date = datetime.datetime(first_year, first_month, first_day, 0, 0, 0)

    list_freq = []
    list_qual = []
    rows = []

    with open(freq_file, 'r') as csv_freq:
      readerfreq = csv.reader(csv_freq, delimiter=';', quotechar='"')
      list_freq = list(readerfreq)

    with open(quality_file, 'r') as csv_quality:
        readerqual = csv.reader(csv_quality, delimiter=',', quotechar='"')
        next(readerqual)

        for row in readerqual:
          currdate = datetime.datetime.strptime(row[5], "%d-%b-%Y %H:%M:%S")
          if (currdate > first_date):
            list_qual.append([*row[0:3], *row[7:9]])

    with open("merged.csv", "w") as csv_merged:
        writer = csv.writer(csv_merged, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(*fields)

        for i in range(1, len(list_freq)-1):
          row = [list_freq[i][0], *list_qual[i-1], round(float(list_freq[i][1])/100, 4)]
          rows.append(row)
          writer.writerow(row)

    print("\nMerged log created!\nPath: " + os.getcwd() + os.sep + "merged.csv" + "\n")
    return rows


def aggregate(log):
    output_file = "aggregated_daily.csv"
    aggregated = []
    rows = []
    fields = ["DATE", "PRODUCTION", "REJECTED", "OEE", "NORMAL_FREQUENCY", "QUALITY_PERC"]
    
    # crete new csv file
    for i in range(0, len(log)-2, 3):
      aggregated.append([round(float(log[i][2]) + float(log[i+1][2]) + float(log[i+2][2]), 2),
                         round(float(log[i][3]) + float(log[i+1][3]) + float(log[i+2][3]), 2),
                         round((float(log[i][4]) + float(log[i+1][4]) + float(log[i+2][4]))/3, 2), 
                         round((float(log[i][5]) + float(log[i+1][5]) + float(log[i+2][5]))/3, 2)])
  
    with open(output_file, "w") as csv_aggregated:
        writer = csv.writer(csv_aggregated, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(fields)

        for i in range(0, len(aggregated)):
          row = [i+1, *aggregated[i], round((aggregated[i][2]+aggregated[i][3])/2, 2)]
          rows.append(row)
          writer.writerow(row)

    print("\nAggregated log created!\nPath: " + os.getcwd() + os.sep + output_file + "\n")
    return rows

def get_best_days(k, log):
  best = sorted(log, key=itemgetter(5, 4), reverse=True)
  return best[0:k]


def get_best_shift(k, indices):
  merged_file = "merged.csv"
  logs = []

  with open(merged_file, 'r') as csv_merged:
    reader = csv.reader(csv_merged, delimiter=',', quotechar='"')
    next(reader)
    
    for row in reader:
      curr_date = int(row[0].split(".")[0])
      if(curr_date in indices):
        logs.append([*row, round( (float(row[5])+float(row[4]))/2, 2)])

  best = sorted(logs, key=itemgetter(6, 5), reverse=True)

  with open("best_shift.csv", "w") as csv_output:
    writer = csv.writer(csv_output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(["DATE_SHIFT", "AVG_VELOCITY","LOG_PRODUCED","LOG_REJECTED", "OEE", "NORMAL_FREQUENCY", "QUALITY_PERC"])

    for s in best:
      writer.writerow(s)

  return best[0:k]

# main
def main():
    log = merge_frequency_oee("2")
    aggregated = aggregate(log)

    bestDays = get_best_days(5, aggregated)
    day_indices = [d[0] for d in bestDays]
    
    print("Best days: ")
    print(["DATE", "PRODUCTION", "REJECTED", "OEE", "NORMAL_FREQUENCY", "QUALITY_PERC"])
    print(*[d for d in bestDays], sep='\n')
    
    print("Best shift: ")
    print(["DATE_SHIFT", "AVG_VELOCITY","LOG_PRODUCED","LOG_REJECTED", "OEE", "NORMAL_FREQUENCY", "QUALITY_PERC"])
    bestShift = get_best_shift(200, day_indices)
    print(*[s for s in bestShift], sep='\n')

    return 0


if __name__ == '__main__':
    main()