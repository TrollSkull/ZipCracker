#import time
from fast_zip import bruteforce_zip

def bruteforce_zip(zip_file, password_list):
    #start = time.perf_counter()
    
    result = bruteforce_zip(zip_file, password_list)

    #end = time.perf_counter()
    
    #print(f"Resultado: {result}")
    #print(f"Tiempo total: {end - start:.3f} segundos")

    return result
