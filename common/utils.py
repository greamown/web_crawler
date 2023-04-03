import json, os
import concurrent.futures

CSV_PATH = "./data/gpu_price.csv"

def read_json(path:str):
    with open(path) as f:
        return json.load(f)
    
def thread_pool(function, array):
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.cpu_count())*7) as executor:
        results = executor.map(function, array)
    concurrent.futures.wait(results, return_when = concurrent.futures.ALL_COMPLETED)
    return True
