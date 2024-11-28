import os

ext = ".csv"
dir = "dags/data"
a = [(f_name, os.path.abspath(f_name)) for f_name in os.listdir(dir) if f_name.endswith(ext)]
# for file_name in os.listdir(dir_name):
#     if file_name.endswith(extension):
#         print(os.path.abspath(file_name))
for idx, f in enumerate(a):
    print(idx)
    print(f[1])
    print(f[0])