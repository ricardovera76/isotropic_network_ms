from helpers._parser_1 import parse_data_stream


def worker():
    data = parse_data_stream()
    for d in data:
        print(d)


worker()
