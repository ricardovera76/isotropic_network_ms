import json

def cache_diff(cache_file, stream_file, diff_file):
    with open(cache_file, 'r') as file1:
        file1_data = file1.read()

    with open(stream_file, 'r') as file2:
        file2_data = file2.read()

    with open(diff_file, "w") as file:
        pass

    file1_objects = [json.loads(line) for line in file1_data.split('\n') if line.strip()]
    file2_objects = [json.loads(line) for line in file2_data.split('\n') if line.strip()]

    updated_objects = []

    for obj2 in file2_objects:
        if obj2 not in file1_objects:
            updated_objects.append(obj2)

    for updated_obj in updated_objects:
        print(json.dumps(updated_obj), file=open(diff_file, "a"))