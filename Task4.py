import json
import psutil
import datetime
import configparser
import time
import schedule

config = json.loads(open("cfg.ini").read())
file_type = config['common']['output']
period = config['common']['interval']
counter = 1


class ConvertToDict(object):
    def converttodict(self, psutil_info):
        """Converts psutil format into dictionary"""
        value = list(psutil_info)
        key = psutil_info._fields
        dict0 = dict(zip(key, value))
        return dict0


class TxtData(ConvertToDict):
    def txt_to_file(self):
        # writing info to output.txt file
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        global counter
        txt = open("output.txt", "a")
        txt.write("\n###Snapshot {0} : {1} ###\n".format(counter, timestamp))
        txt.write("===== System-wide CPU utilization per cpu=====\n{0}\n".format(psutil.cpu_times()))
        txt.write("===== System-wide Memory usage=====\n{0}\n".format(psutil.virtual_memory()))
        txt.write("===== System-wide Swap memory statistics=====\n{0}\n".format(psutil.swap_memory()))
        txt.write("===== System-wide Disk I/O statistics=====\n{0}\n".format(psutil.disk_io_counters()))
        txt.write("===== System-wide Network I/O statistics=====\n{0}\n".format(psutil.net_io_counters(pernic=True)))
        counter += 1
        txt.close()
        print(timestamp)


class JsonData(ConvertToDict):
    def json_to_file(self):
        # writing info to output.json file
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        global counter
        json_file = open("output.json", "a")
        json_file.write('\n{{\n"Snapshot {0}":"{1}",\n'.format(counter, timestamp))
        json_file.write('\n"System-wide CPU utilization per cpu":\n')
        json.dump(super().converttodict((psutil.cpu_times())),json_file, indent=4)
        json_file.write('\n, "System Memory usage":\n')
        json.dump(super().converttodict(psutil.virtual_memory()), json_file, indent=4)
        json_file.write('\n, "System-wide Swap memory statistics":\n')
        json.dump(super().converttodict(psutil.swap_memory()), json_file, indent=4)
        json_file.write('\n, "System-wide Disk I/O statistics":\n')
        json.dump(super().converttodict(psutil.disk_io_counters()), json_file, indent=4)
        json_file.write('\n ,"System-wide Network I/O statistics":\n')
        json.dump(psutil.net_io_counters(pernic=True), json_file, indent=4)
        json_file.write('\n}')
        counter += 1
        json_file.close()
        print(timestamp)

json0 = JsonData()
txt0 = TxtData()


def main():
    if file_type == "txt":
        print('Output file type = {}, interval = {} seconds'.format(file_type, period))
        txt0.txt_to_file()
    elif file_type == "json":
        print('Output file type = {}, interval = {} seconds'.format(file_type, period))
        json0.json_to_file()
    else:
        print("Bad filetype in config file")
        quit()


schedule.every(int(period)).seconds.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
