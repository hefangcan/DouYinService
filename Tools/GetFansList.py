# 通过抖音id获取该用户的粉丝
# 获取粉丝列表，第三步

import hashlib
import json
from pprint import pprint
from urllib import request, parse
import time
from io import StringIO
import gzip

import requests

byteTable1 ="D6 28 3B 71 70 76 BE 1B A4 FE 19 57 5E 6C BC 21 B2 14 37 7D 8C A2 FA 67 55 6A 95 E3 FA 67 78 ED 8E 55 33 89 A8 CE 36 B3 5C D6 B2 6F 96 C4 34 B9 6A EC 34 95 C4 FA 72 FF B8 42 8D FB EC 70 F0 85 46 D8 B2 A1 E0 CE AE 4B 7D AE A4 87 CE E3 AC 51 55 C4 36 AD FC C4 EA 97 70 6A 85 37 6A C8 68 FA FE B0 33 B9 67 7E CE E3 CC 86 D6 9F 76 74 89 E9 DA 9C 78 C5 95 AA B0 34 B3 F2 7D B2 A2 ED E0 B5 B6 88 95 D1 51 D6 9E 7D D1 C8 F9 B7 70 CC 9C B6 92 C5 FA DD 9F 28 DA C7 E0 CA 95 B2 DA 34 97 CE 74 FA 37 E9 7D C4 A2 37 FB FA F1 CF AA 89 7D 55 AE 87 BC F5 E9 6A C4 68 C7 FA 76 85 14 D0 D0 E5 CE FF 19 D6 E5 D6 CC F1 F4 6C E9 E7 89 B2 B7 AE 28 89 BE 5E DC 87 6C F7 51 F2 67 78 AE B3 4B A2 B3 21 3B 55 F8 B3 76 B2 CF B3 B3 FF B3 5E 71 7D FA FC FF A8 7D FE D8 9C 1B C4 6A F9 88 B5 E5"
def getXGon(url,stub,cookies):
    NULL_MD5_STRING = "00000000000000000000000000000000"
    sb=""
    if len(url)<1 :
        sb =NULL_MD5_STRING
    else:
        sb =encryption(url)
    if len(stub)<1:
        sb+=NULL_MD5_STRING
    else:
        sb+=stub
    if len(cookies)<1:
        sb+=NULL_MD5_STRING
    else:
        sb+=encryption(cookies)
    index = cookies.index("sessionid=")
    if index == -1:
        sb+=NULL_MD5_STRING
    else:
        sessionid = cookies[index+10:]
        if sessionid.__contains__(';'):
            endIndex = sessionid.index(';')
            sessionid = sessionid[:endIndex]
        sb+=encryption(sessionid)
    return sb

def encryption(url):
    obj = hashlib.md5()
    obj.update(url.encode("UTF-8"))
    secret = obj.hexdigest()
    return secret.lower()

def initialize(data):
    myhex = 0
    byteTable2 = byteTable1.split(" ")
    for i in range(len(data)):
        hex1 = 0
        if i==0:
            hex1= int(byteTable2[int(byteTable2[0],16)-1],16)
            byteTable2[i]=hex(hex1)
            # byteTable2[i] = Integer.toHexString(hex1);
        elif i==1:
            temp=   int("D6",16)+int("28",16)
            if temp>256:
                temp-=256
            hex1 = int(byteTable2[temp-1],16)
            myhex = temp
            byteTable2[i] = hex(hex1)
        else:
            temp = myhex+int(byteTable2[i], 16)
            if temp > 256:
                temp -= 256
            hex1 = int(byteTable2[temp - 1], 16)
            myhex = temp
            byteTable2[i] = hex(hex1)
        if hex1*2>256:
            hex1 = hex1*2 - 256
        else:
            hex1 = hex1*2
        hex2 = byteTable2[hex1 - 1]
        result = int(hex2,16)^int(data[i],16)
        data[i] = hex(result)
    for i in range(len(data)):
        data[i] = data[i].replace("0x", "")
    return data

def handle(data):
    for i in range(len(data)):
        byte1 = data[i]
        if len(byte1)<2:
            byte1+='0'
        else:
            byte1 = data[i][1] +data[i][0]
        if i<len(data)-1:
            byte1 = hex(int(byte1,16)^int(data[i+1],16)).replace("0x","")
        else:
            byte1 = hex(int(byte1, 16) ^ int(data[0], 16)).replace("0x","")
        byte1 = byte1.replace("0x","")
        a =  (int(byte1, 16) & int("AA", 16)) / 2
        a = int(abs(a))
        byte2 =((int(byte1,16)&int("55",16))*2)|a
        byte2 = ((byte2&int("33",16))*4)|(int)((byte2&int("cc",16))/4)
        byte3 = hex(byte2).replace("0x","")
        if len(byte3)>1:
            byte3 = byte3[1] +byte3[0]
        else:
            byte3+="0"
        byte4 = int(byte3,16)^int("FF",16);
        byte4 = byte4 ^ int("14",16)
        data[i] = hex(byte4).replace("0x","")
    return data

def xGorgon(timeMillis,inputBytes):
    data1 = []
    data1.append("3")
    data1.append("61")
    data1.append("41")
    data1.append("10")
    data1.append("80")
    data1.append("0")
    data2 = input(timeMillis,inputBytes)
    data2 = initialize(data2)
    data2 = handle(data2)
    for i in range(len(data2)):
        data1.append(data2[i])

    xGorgonStr = ""
    for i in range(len(data1)):
        temp = data1[i]+""
        if len(temp)>1:
            xGorgonStr += temp
        else:
            xGorgonStr +="0"
            xGorgonStr+=temp
    return xGorgonStr

def input(timeMillis,inputBytes):
    result = []
    for i in range(4):
        if inputBytes[i]<0:
            temp = hex(inputBytes[i])+''
            temp = temp[6:]
            result.append(temp)
        else:
            temp = hex(inputBytes[i]) + ''
            result.append(temp)
    for i in range(4):
        result.append("0")
    for  i in range(4):
        if inputBytes[i+32]<0:
            result.append( hex(inputBytes[i+32])+'')[6:]
        else:
            result.append(hex(inputBytes[i + 32]) + '')
    for i in range(4):
        result.append("0")
    tempByte = hex(int(timeMillis))+""
    tempByte = tempByte.replace("0x","")
    for i in range(4):
        a = tempByte[i * 2:2 * i + 2]
        result.append(tempByte[i*2:2*i+2])
    for i in range(len(result)):
        result[i] = result[i].replace("0x","")
    return result

def strToByte(str):
    length = len(str)
    str2 = str
    bArr =[]
    i=0
    while i < length:
        # bArr[i/2] = b'\xff\xff\xff'+(str2hex(str2[i]) << 4+str2hex(str2[i+1])).to_bytes(1, "big")
        a = str2[i]
        b = str2[1+i]
        c = ((str2hex(a) << 4)+str2hex(b))
        bArr.append(c)
        i+=2
    return bArr

def str2hex(s):
    odata = 0;
    su =s.upper()
    for c in su:
        tmp=ord(c)
        if tmp <= ord('9') :
            odata = odata << 4
            odata += tmp - ord('0')
        elif ord('A') <= tmp <= ord('F'):
            odata = odata << 4
            odata += tmp - ord('A') + 10
    return odata

def doGetGzip(url,headers,charset):
    req = requests.get(url, headers=headers, verify=False)

    print(req.text)

if __name__ == "__main__":
    ts = str(time.time()).split(".")[0]
    _rticket = str(time.time() * 1000).split(".")[0]
    url = 'https://aweme-hl.snssdk.com/aweme/v1/user/follower/list/?user_id=1199141175&sec_user_id=MS4wLjABAAAAS-ZzAasV10I_fUTg6QD19oLOCKx29icwFI6MlbSC97fYb94acVykH8z_lbZju9ZD&max_time={}&count=20&offset=0&source_type=1&address_book_access=1&gps_access=1&vcd_count=0&os_api=23&device_type=MI%205s&device_platform=android&ssmix=a&iid=1028786593992525&manifest_version_code=100501&dpi=320&uuid=008796760665134&version_code=100500&app_name=aweme&cdid=9039c8c0-66b3-4992-a2ca-e1a90e98d3ba&version_name=10.5.0&ts=1590740576&openudid=75f0c9390fb221d9&device_id=78804984545944&resolution=800*1280&os_version=6.0.1&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=10509900&aid=1128&channel=tengxun_new&_rticket={}'.format(time.time(),_rticket)

    cookies = 'd_ticket=dff5938a91e056156dda648b98456f7d774b5; odin_tt=9057e23ce98f406d5b7bb812df1ad446ef7783fa977ce5eb2981308a0650b49b50734a7a6d6fd21af60be0dc9684d0da09413fef0544f3e54e8abe45b7cf2be4; sessionid=373834220f19c51d55d50c84b5ec10c5; sessionid_ss=373834220f19c51d55d50c84b5ec10c5; sid_guard=373834220f19c51d55d50c84b5ec10c5%7C1588920775%7C5184000%7CTue%2C+07-Jul-2020+06%3A52%3A55+GMT; sid_tt=373834220f19c51d55d50c84b5ec10c5; uid_tt=f533d39bf850b97401fbaad14258f19a; uid_tt_ss=f533d39bf850b97401fbaad14258f19a; install_id=3034290764913102; ttreq=1$7ab7a651c80675df74633f4a42649edbd35768c9; SLARDAR_WEB_ID=05614d03-bea0-4c8e-beb9-fda01dfa2c3a'
    params = url[url.index('?') + 1:]
    STUB = ""
    s = getXGon(params, STUB, cookies)
    gorgon = xGorgon(ts, strToByte(s))
    headers = {
        "X-Gorgon": gorgon,
        # "X-SS-REQ-TICKET": "1585711173953",
        "X-Khronos": ts,
        "sdk-version": "1",
        "Accept-Encoding": "gzip",
        "X-SS-REQ-TICKET": _rticket,
        "User-Agent": "ttnet okhttp/3.10.0.2",
        "Host": "aweme.snssdk.com",
        "Cookie": cookies,
        "Connection": "Keep-Alive",
        "x-tt-token": "00373834220f19c51d55d50c84b5ec10c598631721d3cd1f9af48261e7d514ab931004eef2647be6a65e28895b988ed8b21e"
    }
    result = doGetGzip(url, headers, "UTF-8")

