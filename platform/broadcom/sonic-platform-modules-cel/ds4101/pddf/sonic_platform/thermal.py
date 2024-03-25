#!/usr/bin/env python
# @Company ：Celestica
# @Time    : 2023/3/6 09:32
# @Mail    : yajiang@celestica.com
# @Author  : jiang tao

try:
    from sonic_platform_pddf_base.pddf_thermal import PddfThermal
    from . import helper

except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

sensor_info_path = "/var/log/sensor_info.log"

class Thermal(PddfThermal):
    """PDDF Platform-Specific Thermal class"""

    def __init__(self, index, pddf_data=None, pddf_plugin_data=None, is_psu_thermal=False, psu_index=0):
        self.helper = helper.APIHelper()
        PddfThermal.__init__(self, index, pddf_data, pddf_plugin_data, is_psu_thermal=is_psu_thermal,
                             psu_index=psu_index)

    def get_high_critical_threshold(self):
        """
        Rewrite the method of obtaining PSU high critical in pddf_thermal

        Returns:
            A float number, the high critical threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        if not self.is_psu_thermal:
            output = self.pddf_obj.get_attr_name_output(self.thermal_obj_name, "temp1_high_crit_threshold")
            if not output:
                return None

            if output['status'].isalpha():
                attr_value = None
            else:
                attr_value = float(output['status'])

            if output['mode'] == 'bmc':
                return attr_value
            else:
                return float(attr_value / 1000)
        else:
            with open(sensor_info_path, "r") as f:
                info = f.readlines()
            for line in info:
                if "PSU%d_TEMP1" % self.thermals_psu_index in line:
                    return float(line.split("|")[8])

    def get_temperature(self):
        """
        Rewrite the method of obtaining temperature in pddf_thermal
        Avoid changing the value to 0 when the psu temperature value obtained 
        from BMC is character 'na'

        Returns:
            A float number, the temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        if self.is_psu_thermal:
            device = "PSU{}".format(self.thermals_psu_index)
            output = self.pddf_obj.get_attr_name_output(device, "psu_temp1_input")
            if not output:
                return None

            if output['status'].isalpha():
                attr_value = None
            else:
                attr_value = float(output['status'])

            if output['mode'] == 'bmc':
                return attr_value
            else:
                return (attr_value/float(1000))
        else:
            output = self.pddf_obj.get_attr_name_output(self.thermal_obj_name, "temp1_input")
            if not output:
                return None

            if output['status'].isalpha():
                attr_value = None
            else:
                attr_value = float(output['status'])

            if output['mode'] == 'bmc':
                return attr_value
            else:
                return (attr_value/float(1000))