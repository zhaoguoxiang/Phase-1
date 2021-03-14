from rdkit import Chem 
from rdkit.Chem import AllChem 

smifile = '../Molecules/substituted_benzene_para.smi'
title = smifile.split('/')[-1].rstrip('.smi')
gjfpath = '../opt_input/phase-2'
keywords = '''%nprocshared=24
%mem=32GB
#p opt freq b3lyp/6-31g(d) em=gd3 nosymm
'''

with open (smifile,'r+') as f:
    smiles = f.readlines()
for i in range(len(smiles)):
    smiles[i] = smiles[i].strip('\n')
mols = [Chem.MolFromSmiles(smi) for smi in smiles]
mols = [Chem.AddHs(mol) for mol in mols]#TM Chem 函数和AllChem函数不一样，必须得这样写
for mol in mols:
    #Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    AllChem.MMFFOptimizeMolecule(mol) 

for i in range(len(mols)):
    with open(gjfpath+'/'+title+'_'+str(i)+'.gjf', 'w') as f:
        f.write('%chk='+title+'_'+str(i)+'.chk\n'+keywords+'\n'+title+'_'+str(i)+'\n\n'+'0 1\n')
        for atom in mols[i].GetAtoms():
            idx = atom.GetIdx()
            x = mols[i].GetConformer(0).GetAtomPosition(idx).x
            if x>=0:
                x = ' '+str(x)
            else:
                x = str(x)
            x = x[0:10]
            y = mols[i].GetConformer(0).GetAtomPosition(idx).y
            if y>=0:
                y = ' '+str(y)
            else:
                y = str(y)
            y = y[0:10]
            z = mols[i].GetConformer(0).GetAtomPosition(idx).z
            if z>=0:
                z = ' '+str(z)
            else:
                z = str(z)
            z = z[0:10]
            f.write(' '+atom.GetSymbol()+'                '+x+'   '+y+'   '+z+'\n')
        f.write('\n\n')  



#生成提交计算的脚本文件

head = '''#!/bin/bash
#SBATCH -p v3_64
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 24
export g16ROOT=/public1/home/sc32041/soft/g16
export PATH=$g16ROOT:$PATH
source $g16ROOT/bsd/g16.profile
export GAUSS_SCRDIR=/public1/home/sc32041/soft/g16/tmp
export GAUSS_EXEDIR=$g16ROOT
'''
with open(gjfpath+'/opt-'+title+'.sh', 'w') as f:
    f.write(head)
    for i in range(len(mols)):
        f.write('srun -c 24 g16 '+title+'_'+str(i)+'.gjf\n')
        f.write('formchk '+title+'_'+str(i)+'.chk\n')
