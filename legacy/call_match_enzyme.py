import subprocess
import asyncio
import os

def create_arg(start, end):
    arg = ["python", "main.py", "match_enzyme", str(start), str(end),
           "-i", "../result/refseq_data/Pooled/best_blast",
           "-o", "../match_enzmye_result",
           "--quiet"]
    return arg

# async def print_process(process, idx):
#     while True:
#         if process.poll() == 0: break
#         print(f"process_{idx+1}")
#         print(process.stdout)
#         await asyncio.sleep(3)


process_1 = subprocess.Popen(create_arg(1, 6), stdout=subprocess.PIPE)
process_2 = subprocess.Popen(create_arg(6, 11), stdout=subprocess.PIPE)
process_3 = subprocess.Popen(create_arg(11, 16), stdout=subprocess.PIPE)
process_4 = subprocess.Popen(create_arg(16, 21), stdout=subprocess.PIPE)
process_5 = subprocess.Popen(create_arg(21, 26), stdout=subprocess.PIPE)
process_6 = subprocess.Popen(create_arg(26, 31), stdout=subprocess.PIPE)
process_7 = subprocess.Popen(create_arg(31, 36), stdout=subprocess.PIPE)
process_8 = subprocess.Popen(create_arg(36, 41), stdout=subprocess.PIPE)
process_9 = subprocess.Popen(create_arg(41, 46), stdout=subprocess.PIPE)
process_10 = subprocess.Popen(create_arg(46, 51), stdout=subprocess.PIPE)
process_11 = subprocess.Popen(create_arg(51, 56), stdout=subprocess.PIPE)
process_12 = subprocess.Popen(create_arg(56, 61), stdout=subprocess.PIPE)
process_13 = subprocess.Popen(create_arg(61, 66), stdout=subprocess.PIPE)
process_14 = subprocess.Popen(create_arg(66, 71), stdout=subprocess.PIPE)
process_15 = subprocess.Popen(create_arg(71, 76), stdout=subprocess.PIPE)
process_16 = subprocess.Popen(create_arg(76, 81), stdout=subprocess.PIPE)
process_17 = subprocess.Popen(create_arg(81, 86), stdout=subprocess.PIPE)
process_18 = subprocess.Popen(create_arg(86, 91), stdout=subprocess.PIPE)
process_19 = subprocess.Popen(create_arg(91, 96), stdout=subprocess.PIPE)
process_20 = subprocess.Popen(create_arg(96, 101), stdout=subprocess.PIPE)

processes = [process_1,
             process_2,
             process_3,
             process_4,
             process_5,
             process_6,
             process_7,
             process_8,
             process_9,
             process_10,
             process_11,
             process_12,
             process_13,
             process_14,
             process_15,
             process_16,
             process_17,
             process_18,
             process_19,
             process_20]

# for idx, process in enumerate(processes):
#     asyncio.run(print_process(process, idx))

exit_code = [p.wait() for p in processes]