import requests as req
import numpy as np
with open("demo\\tracklist.txt", "r", encoding='utf8') as tracklistfile:
    trackList = np.asarray(tracklistfile.readlines())
    trackList = np.unique(trackList)
i = 0
trackList = trackList[1:]
workList = []
for n in np.nditer(trackList):
    n = str(n)
    if(n[0] == 'u'):
        break
    n = n.rstrip('\n')
    print("正在测试:%s" % n)
    try:
        test = req.get(n, timeout=5)
    except:
        print("Error:连接时发生错误")
        continue
    if(test.status_code == 200):
        print("可连接")
        workList.append(n)
    else:
        print("无法连通")
    test.close()
workList = np.asarray(workList)
with open("demo\\workList.txt", "w", encoding="utf8") as workfile:
    for n in np.nditer(workList):
        workfile.writelines(str(n)+'\n')
print("完成")
