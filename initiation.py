import os
import re
import shutil
import time

import cclib
import pandas as pd
import numpy as np

def mktmpdir(path):
    folder = os.path.exists(path)
    if folder:
        shutil.rmtree(path)
        os.mkdir(path)
        print('the path has been rebuild!')
    else:
        os.mkdir(path)

def listfiles (keywords, rootdir = './'):
    filelist = []
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if (file.endswith(keywords)):
                filelist.append(os.path.join(root, file))
    for i in range(len(filelist)): 
        filelist[i] = filelist[i].replace('\\','/') 
    return filelist

# delnull 函数是删除字符串列表中的空字符串
def delnull(strs):
    without_empty_strings = []
    for string in strs:
        if (string != ""):
            without_empty_strings.append(string)
    return without_empty_strings
# infof 函数infofunction，给出行号和.readlines列表，目的是将行中的字符分割，去掉空字符串
def infof(rn,fl):
    info = re.split(' |,|:|\n',fl[rn])
    info = [c.strip() for c in info]
    info = delnull(info)
    return info

def getlinenums (file, keywords):
# you can optimize the function by open file once to complete the several search job in one step
    numlist = []
    with open(file,'r') as f:
        for (num,content) in enumerate(f):
            if (keywords in content):
                numlist.append(num)
    if len(numlist) > 1:
        return numlist
    elif len(numlist) == 1:
        return numlist[0]
    else:
        print('Can not find content with given keywords')


def filename(filepath):#
    filename = filepath.split('/')[-1].split('.')[-2]
    return filename

def multiwfn(inputfile, commands):
    path = '../temp/multiwfntmp'
    subdir = path+'/export'
    mktmpdir(path)
    mktmpdir(subdir)
    file = filename(inputfile)
    with open(path+'/para.txt','w') as para:
        para.write(commands)
    
    os.system('Multiwfn '+inputfile+' < '+path+'/para.txt > '+subdir+'/'+file+'.txt')   
    
    #os.remove(path+'/para.txt')

def gamma(gammafile):
    commands = '200\n7\n-4\n7\n'
    path = '../temp/multiwfntmp'
    subdir = path+'/export'
    mktmpdir(path)
    mktmpdir(subdir)
    file = filename(gammafile)
    with open(path+'/para.txt','w') as para:
        para.write(commands)   
    os.system('Multiwfn '+gammafile+' < '+path+'/para.txt > '+subdir+'/'+file+'.txt')

    linenums = getlinenums(subdir+'/'+file+'.txt','Magnitude of gamma:')
    print(linenums)
    with open(subdir+'/'+file+'.txt','r+') as f:
        fl =f.readlines()[linenums]
        magnitudeofgamma = float( fl.split(':')[-1].strip(' ').strip('\n'))
    return magnitudeofgamma
    
    

