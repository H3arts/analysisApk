# coding:utf8
import zipfile
import os
import sys
import hashlib
import subprocess
import re
import io
from config import *

# 解压apk文件
def unzip(in_path, out_path):
    print "[INFO] Unzip APK"
    try:
        files = []
        with zipfile.ZipFile(in_path, "r") as z:
            z.extractall(out_path)
            files = z.namelist()
        return files
    except Exception as e:
        print "[ERROR] Unziping Error:" + str(e)

# 计算文件md5
def get_filemd5_dir(file_path):
    print "[INFO] Get Filemd5 Path"
    try:
        # 计算文件的md5
        f = open(file_path, 'rb')
        md5 = hashlib.md5()
        md5.update(f.read())
        md5sum = md5.hexdigest()
        f.close()

        # 创建文件md5对应的目录
        file_dir = os.path.join(TMP_PATH, md5sum)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)

        return file_dir
    except Exception as e:
        print "[ERROR] Get Filemd5 Path Error:" + str(e)

def dex2smali(out_path, smali_path, files):
    print "[INFO] dex2smali"
    try:
        baksmali_path = os.path.join(TOOLS_DIR, 'baksmali.jar')
        for f in files:
            if f.lower().endswith('.dex'):
                dex_path = os.path.join(out_path, f)
                args = ['java','-jar',baksmali_path, dex_path,'-o',smali_path]
                subprocess.call(args)
    except Exception as e:
        print "[ERROR] dex2smali Error:" + str(e)

def get_url_from_smali(smali_path):
    print "[INFO] Getting url"
    try:
        match_ip = re.compile(r'(?<![\.\d])((?:(?:2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(?:2[0-4]\d|25[0-5]|[01]?\d\d?))(?![\.\d])')
        match_url = p = re.compile(ur'((?:https?://|s?ftps?://|www\d{0,3}[.])[\w().=/;,#:@?&~*+!$%\'{}-]+)', re.UNICODE)
        URLS = []
        IPs = []
        for dirname, subdir, files in os.walk(smali_path):
            for smali_file in files:
                sfile_path = os.path.join(smali_path, dirname, smali_file)
                if smali_file.endswith('.smali'):
                    dat = ''
                    with io.open(sfile_path, mode='r', encoding='utf8', errors='ignore') as f:
                        dat = f.read()
                    urllist = re.findall(match_url, dat.lower())
                    iplist = re.findall(match_ip, dat.lower())
                    for url in urllist:
                        if url not in URLS:
                            URLS.append(url)
                    for ip in iplist:
                        if ip not in IPs:
                            IPs.append(ip)
        return URLS, IPs

    except Exception as e:
        print "[ERROR] Get Url Error:" + str(e)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print u"[Error] 参数个数错误!"
        print "usage: python appdetect.py xxx.apk"
        exit()
    print os.path.abspath(sys.argv[1])
    print BASE_DIR, TMP_PATH
    in_path = sys.argv[1]
    # 获取md5路径
    out_path = get_filemd5_dir(in_path)
    # 解压apk
    files = unzip(in_path, out_path)
    smali_path = os.path.join(out_path, 'smali')
    # if not os.path.isdir(smali_path):
    #     os.makedirs(smali_path)
    # 反编译dex文件
    dex2smali(out_path, smali_path, files)
    # 从smali文件中获取url
    urls,ips = get_url_from_smali(smali_path)
    for i in urls:
        print i
    for i in ips:
        print i
    #print unzip(sys.argv[1], './apk/lol')
