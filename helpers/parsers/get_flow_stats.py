def get_stats(dig_flow_pkt):
    """
    @param dig_flow_pkt (list[dicts])   : list of dictionaries of all flows pkts with type === "flow_stats" or "flow_purge"
    @return pkts         (list[dicts])   : list of dictionaries of all pkts statistics
    """
    pkt_flows = []
    [
        pkt_flows.append({
            "digest": pkt_flow["flow"]["digest"],
            "last_seen": pkt_flow["flow"]["last_seen_at"],
            "ttl_bytes": pkt_flow["flow"]["total_bytes"],
            "local_bytes": pkt_flow["flow"]["local_bytes"],
            "other_bytes": pkt_flow["flow"]["other_bytes"],
            "ttl_pkts": pkt_flow["flow"]["total_packets"],
            "local_pkts": pkt_flow["flow"]["local_packets"],
            "other_pkts": pkt_flow["flow"]["other_packets"],
            "local_rate": pkt_flow["flow"]["local_rate"],
            "other_rate": pkt_flow["flow"]["other_rate"],
        })
        for pkt_flow in dig_flow_pkt
    ]
    consolidated_data = {}

    for item in pkt_flows:
        digest = item['digest']
        if digest in consolidated_data:
            consolidated_item = consolidated_data[digest]
            consolidated_item['bytes_ttl'] = item['ttl_bytes']
            consolidated_item['bytes_up'] = item['local_bytes']
            consolidated_item['bytes_dn'] = item['other_bytes']
            consolidated_item['pkts_ttl'] = item['ttl_pkts']
            consolidated_item['pkts_up'] = item['local_pkts']
            consolidated_item['pkts_dn'] = item['other_pkts']
            if item["last_seen"] > consolidated_data[digest]["last_seen"]:
                consolidated_item['last_seen'] = item['last_seen']
                consolidated_item['rate_up'] = item['local_rate']
                consolidated_item['rate_down'] = item['other_rate']
        else:
            consolidated_data[digest] = {
                'digest': digest,
                'last_seen':item['last_seen'],
                'bytes_ttl': item['ttl_bytes'],
                'bytes_up': item['local_bytes'],
                'bytes_dn': item['other_bytes'],
                'pkts_ttl': item['ttl_pkts'],
                'pkts_up': item['local_pkts'],
                'pkts_dn': item['other_pkts'],
                'rate_up': item['local_rate'],
                'rate_dn': item['other_rate'],
            }
    return list(consolidated_data.values())