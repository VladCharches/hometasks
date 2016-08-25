import psutil
import datetime
import json
import schedule
import time
import logging

config = json.loads(open("cfg.ini").read())
file_type = config['common']['output']
period = config['common']['interval']
counter = 1
file_txt0 = "output.txt"
file_json0 = "output.json"


handler = logging.FileHandler('test.log')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def logger(function0):
    """
    ###The decorator prints number of calls of the decorated function###
    """
    def wrapper(self, file_name):
        wrapper.counter += 1
        print("\nStart logging of {} function".format(function0.__name__))
        result = function0(self, file_name)
        print("{} has been called {} times with parameters {}\n".format(function0.__name__, wrapper.counter, file_name))
        logging.info("Wrapper run")
        return result
    wrapper.counter = 0
    return wrapper


class ConvertToDict(object):
    def converttodict(self, psutil_info):
        """Converts psutil format into dictionary"""
        value = list(psutil_info)
        key = psutil_info._fields
        dict0 = dict(zip(key, value))
        return dict0


class TxtData(ConvertToDict):
    @logger
    def txt_to_file(self, file_txt):
        # writing info to output.txt file
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        global counter
        txt = open(file_txt, "a")
        txt.write("\n###Snapshot {0} : {1} ###\n".format(counter, timestamp))
        txt.write("===== System-wide CPU utilization per cpu =====\n{0}\n".format(psutil.cpu_times()))
        txt.write("===== System-wide Memory usage =====\n{0}\n".format(psutil.virtual_memory()))
        txt.write("===== System-wide Swap memory statistics =====\n{0}\n".format(psutil.swap_memory()))
        txt.write("===== System-wide Disk I/O statistics =====\n{0}\n".format(psutil.disk_io_counters()))
        txt.write("===== System-wide Network I/O statistics =====\n{0}\n".format(psutil.net_io_counters(pernic=True)))
        counter += 1
        txt.close()
        print(timestamp)
        logging.info("{} file was written successfully".format(file_txt))


class JsonData(ConvertToDict):
    @logger
    def json_to_file(self, file_json):
        # writing info to output.json file
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        global counter
        json_file = open(file_json, "a")
        json_file.write('{{\n"Snapshot {0}": "{1}",'.format(counter, timestamp))
        json_file.write('\n"System-wide CPU utilization per cpu":\n')
        json.dump(super().converttodict((psutil.cpu_times())),json_file, indent=4)
        json_file.write('\n, "System Memory usage":\n')
        json.dump(super().converttodict(psutil.virtual_memory()), json_file, indent=4)
        json_file.write('\n, "System-wide Swap memory statistics":\n')
        json.dump(super().converttodict(psutil.swap_memory()), json_file, indent=4)
        json_file.write('\n, "System-wide Disk I/O statistics":\n')
        json.dump(super().converttodict(psutil.disk_io_counters()), json_file, indent=4)
        json_file.write('\n , "System-wide Network I/O statistics":\n')
        json.dump(psutil.net_io_counters(pernic=True), json_file, indent=4)
        json_file.write('\n}\n\n')
        counter += 1
        json_file.close()
        print(timestamp)
        logging.info("{} file was written successfully".format(file_json))


try:
    json0 = JsonData()
    logging.info("Object {} was created successfully".format(json0))
except Exception as e:
    logging.exception("Can not create object, {}".format(e))

try:
    txt0 = TxtData()
    logging.info("Object {} was created successfully".format(txt0))
except Exception as e:
    logging.exception("Can not create object, {}".format(e))


def main():
    if file_type == "txt":
        txt0.txt_to_file(file_txt0)
    elif file_type == "json":
        json0.json_to_file(file_json0)
    else:
        print("Unknown type of file in config")
        quit()


try:
    schedule.every(int(period)).seconds.do(main)
    logging.info("Scheduler started")
except Exception as e:
    logging.exception("Problem with starting scheduler, {}".format(e))


while True:
    schedule.run_pending()
    time.sleep(0)