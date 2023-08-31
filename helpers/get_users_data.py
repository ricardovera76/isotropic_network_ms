from helpers.vendor_handler import get_vendor
from helpers.device_name_handler import get_device_name

def get_users(dig_flow_app, app_list):
    result_dict = {}
    for app_flow in dig_flow_app:
        ip = app_flow["flow"]["local_ip"]
        mac = app_flow["flow"]["local_mac"]
        digest = app_flow["flow"]["digest"]
        application = app_flow["flow"]["detected_application_name"]
        app_name = ""
        for app in app_list:
            if app['tag'] == application:
                app_name = app['label']
            else:
                app_name = application

        key = (ip, mac)

        if key in result_dict:
            result_dict[key]["apps"].append([digest, app_name])
        else:
            result_dict[key] = {
                "ip": ip,
                "mac": mac,
                "apps": [[digest, app_name]],
            }

    result_list = list(result_dict.values())
    for result in result_list:
        result['device_name'] = get_device_name(result['ip'])
        result['device_vendor'] = get_device_name(result['mac'])
        
    return result_list