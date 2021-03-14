#multiwfn 分析提取gamma

from initiation import *
import os

gammadir = '../gamma_output/phase-2'
parameterfile = './parameter/gamma.txt'

gammadict = {}
name = []
val = []
for file in listfiles('.log',gammadir):
    title = file.split('/')[-1].rstrip('.log')
    command = 'multiwfn '+file+' <'+parameterfile
    outinfo = os.popen(command).readlines()
    gammaval = float(outinfo[138][-16:-1].strip(' '))
    name.append(title)
    val.append(gammaval)
    #gammadict[title] = gammaval
    gammadict = {'name':name, 'gamma':val}

print(gammadict)
print(name)
print(val)
gammadata = pd.DataFrame.from_dict(gammadict)
gammadata.to_csv('../ai/substituted_benzene_para_gamma.csv')


#this is a test