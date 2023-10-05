def get_flows(dig_flow_app, pkts):
    """
    @param dig_flow_app (list[dicts])   : list of dictionaries of all flows pkts with type === "flow"
    @param pkts         (list[dicts])   : list of dictionaries of all pkts statistics
    @return apps        (list[dicts])   : list of dictionaries of all apps traffic for this iteration
    """
    apps = []
    digest_last_seen = {}  # A dictionary to keep track of the last seen timestamp for each digest

    for app_flow in dig_flow_app:
        digest = app_flow["flow"]["digest"]
        application = app_flow["flow"]["detected_application_name"]
        mac = app_flow["flow"]["local_mac"]
        for pkt in pkts:
            if pkt['digest'] == digest:
                pkt["mac_addr"] = mac
                pkt["app_name"] = application
                data = pkt.copy()
                apps.append(pkt)
                # Check if the digest is already in apps and compare last seen timestamps
                if digest in digest_last_seen:
                    last_seen = digest_last_seen[digest]
                    if data["last_seen"] > last_seen:
                        # Replace the existing data with the most recent data
                        apps[:] = [app for app in apps if app.get("digest") != digest]
                        apps.append(data)
                        digest_last_seen[digest] = data["last_seen"]
                else:
                    apps.append(data)
                    digest_last_seen[digest] = data["last_seen"]
    return apps
