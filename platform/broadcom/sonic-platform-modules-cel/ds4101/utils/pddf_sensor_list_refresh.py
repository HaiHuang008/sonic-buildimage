#!/usr/bin/python
# -*- coding: utf-8 -*-#

# @Time   : 2023/4/13 9:46
# @Mail   : yajiang@celestica.com
# @Author : jiang tao

import os
import subprocess
import time

try:
    from sonic_platform import sensor_list_config
    from sonic_py_common import logger
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

sensor_info_path = sensor_list_config.Sensor_List_Info
refresh_interval = sensor_list_config.Sensor_Info_Update_Period_Secs

log = logger.Logger()


def write_sensor_list_info():
    """
    Write the log of the command 'ipmitool sensor list' in sensor_info.log
    """
    try:
        info = os.popen("ipmitool sensor list").read()
        if "System Event" in info:
            with open(sensor_info_path, "w") as f:
                f.write(info)
    except Exception as E:
        log.log_error(str(E))


def sync_sensor_list_info():
    """
    Sync the log sensor_info.log into docker pmon
    """
    try:
        cmd = "docker cp {} pmon:{}".format(sensor_info_path, sensor_info_path)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as E:
        pass


if __name__ == '__main__':
    while 1:
        write_sensor_list_info()
        sync_sensor_list_info()
        time.sleep(refresh_interval)
