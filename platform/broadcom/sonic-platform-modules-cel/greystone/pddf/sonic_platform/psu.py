#!/usr/bin/env python
# @Company ：Celestica
# @Time    : 2023/3/10 10:23
# @Mail    : yajiang@celestica.com
# @Author  : jiang tao
try:
    from sonic_platform_pddf_base.pddf_psu import PddfPsu
    import re
    import os
    from . import helper
    from . import sensor_list_config
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

Change_Channel_Cmd = "0x3a 0x3e 6 0xe0 0 {}"


class Psu(PddfPsu):
    """PDDF Platform-Specific PSU class"""

    def __init__(self, index, pddf_data=None, pddf_plugin_data=None):
        PddfPsu.__init__(self, index, pddf_data, pddf_plugin_data)
        self.helper = helper.APIHelper()
        if not os.path.exists(sensor_list_config.Sensor_List_Info):
            cmd = "ipmitool sensor list > %s" % sensor_list_config.Sensor_List_Info
            self.helper.run_command(cmd)

    @staticmethod
    def get_capacity():
        return 550

    @staticmethod
    def get_type():
        return 'AC'


