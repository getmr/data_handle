import os
import re
import time


# 配置文件启动命令
# python  -- segment_standrd
seg_std_py = "segment_standard_v3.20180611.py 6001 app"
seg_std_path = "/data/app/standard-segment"
# python  -- scene start
scene_st_py = "start.py scene-app"
scene_st_path = "/data/app/scene_start"
# python  -- plane start
plane_st_py = "start.py plane-bayes-app"
plane_st_path = "/data/app/plane_bayes"
# python  -- hotel start
hotel_st_py = "start.py hotel-bayes-app"
hotel_st_path = "/data/app/hotel_bayes"

# java  -- socket
java_skt = "-jar socket-api-0.0.1-SNAPSHOT.jar 60001 socket app"
# java  -- standard
java_std = "-jar nlp-model-standard-0.0.1-SNAPSHOT.jar segment-standard \
standard app"
# java  -- condition
java_cond = "-jar nlp-model-condition-0.0.1-SNAPSHOT.jar node app"
# business-plane
java_bs_plane = "-jar business-plane-0.0.1-SNAPSHOT.jar app"
# business-hotel
java_bs_hotel = "-jar business-hotel-0.0.1-SNAPSHOT.jar app"
# nlp-model-gis
java_gis = "-jar nlp-model-gis-0.0.1-SNAPSHOT.jar nearbyHotel app 0"
# java项目路径
java_path = "/data/app"


while True:
    # 监测python进程
    py_process = os.popen("ps aux | grep python").read()
    py_process_list = py_process.split("\n")
    print(py_process_list)

    # 获得每一个python进程名字的列表
    py_list = []
    for pro in py_process_list:
        pro = re.search(r"python (.+)", pro)
        if pro:
            py_list.append(pro.group(1))

    # 监测切词标准化
    if seg_std_py not in py_list:
        os.chdir(seg_std_path)
        os.system("nohup python {} &>/dev/null  &".format(seg_std_py))
        print("启动切词")
    # 监测scene
    if scene_st_py not in py_list:
        os.chdir(scene_st_path)
        os.system("nohup python {} &>/dev/null  &".format(scene_st_py))
        print("启动scene")
    # 监测plane
    if plane_st_py not in py_list:
        os.chdir(plane_st_path)
        os.system("nohup python {} &>/dev/null  &".format(plane_st_py))
        print("启动plane")
    # 监测hotel
    if hotel_st_py not in py_list:
        os.chdir(hotel_st_path)
        os.system("nohup python {} &>/dev/null  &".format(hotel_st_py))
        print("启动hotel")

    # 监测java进程
    java_process = os.popen("ps aux | grep java").read()
    java_process_list = java_process.split("\n")
    # 获得每一个java进程名字的列表
    java_list = []
    for pro in java_process_list:
        pro = re.search(r"java (.+)", pro)
        if pro:
            py_list.append(pro.group(1))

    # 监测sockt
    if java_skt not in java_list:
        os.chdir(java_path)
        os.system("nohup java {} >/dev/null 2>&1 &".format(java_skt))
        print("sockt启动")
    # 监测java标准化
    if java_std not in java_list:
        os.chdir(java_path)
        os.system("nohup java {} >/dev/null 2>&1 &".format(java_std))
        print("java标准化启动")
    # 监测java business_plane
    if java_bs_plane not in java_list:
        os.chdir(java_path)
        os.system("nohup java {} >/dev/null 2>&1 &".format(java_bs_plane))
        print("java_bs_plane启动")
    # 监测java business_hotel
    if java_bs_hotel not in java_list:
        os.chdir(java_path)
        os.system("nohup java {} >/dev/null 2>&1 &".format(java_bs_hotel))
        print("java_bs_hotel 启动")
    # 监测condition
    if java_cond not in java_list:
        os.chdir(java_path)
        os.system("nohup java {} >/dev/null 2>&1 &".format(java_cond))
        print("java_condition 启动")
    # 监测jsva_gis
    if java_gis not in java_list:
        os.chdir(java_path)
        os.system("nohup java {} >/dev/null 2>&1 &".format(java_gis))
        print("java_gis启动")
    time.sleep(1)
