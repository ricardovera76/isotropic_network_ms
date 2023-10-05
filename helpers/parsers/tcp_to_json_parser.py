import json

def tcp_json_parser(uuid):
    """
    @param uuid (int) : unique identifier for sequence iteration
    
    @return output_filename (string) : name of output file name
    """
    out_file = f"{uuid}_out.json"
    with open('/tmp/out.json', 'r') as file:
            json_accumulator = ""
            for line in file:
                json_accumulator += line
                
                try:
                    data = json.loads(json_accumulator)
                    # if acc data is a valid JSON object, append data into legacy view
                    print(json.dumps(data, separators=(',', ':')), file=open(out_file,"a"))

                    # Reset the accumulator
                    json_accumulator = ""
                except json.JSONDecodeError as e:
                    # if acc is not a valid JSON object, continue accumulating lines
                    continue
    return out_file
