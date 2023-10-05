from helpers.handlers.vendor_handler import get_vendor
from helpers.handlers.device_name_handler import get_device_name

def get_user(dig_flow_app):
    """
    @param dig_flow_app (list[dicts])   : list of dictionaries of all flows pkts with type === "flow"
    
    @return result_list (list[dicts])   : list of dictionaries of all current users in network
    """
    result_dict = {}
    for app_flow in dig_flow_app:
        ip = app_flow["flow"]["local_ip"]
        mac = app_flow["flow"]["local_mac"]
        result_dict[mac] = {
            "ip": ip,
            "mac": mac
        }

    result_list = list(result_dict.values())
    for result in result_list:
        result['device_name'] = get_device_name(result['ip'])
        result['device_vendor'] = get_vendor(result['mac'])

    return result_list