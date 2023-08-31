import json

def flow_parser(source_file, unique_digests, flow_type):
    """
    flow_type = flow | st_pr
    """
    
    flow = {"flow":["flow"], "st_pr": ["flow_purge", "flow_stats"]}

    data = open(source_file).read()
    lines = data.strip().split("\n")

    result = []
    for line in lines:
            json_data = json.loads(line)
            for digest in unique_digests:
                if json_data.get("flow") != None and json_data["flow"]["digest"] == digest:
                    if json_data["type"] in flow[flow_type]:
                        result.append(json_data)

    return result