import pandas as pd
import numpy as np

from multiprocessing import freeze_support
from rdkit import Chem
from mordred import Calculator, descriptors

smifile = '../Molecules/substituted_benzene_para.smi'

with open(smifile) as f:
    a = f.readlines()
smiles = []
for b in range(len(a)):
    smiles.append(a[b].strip('\n'))

mols = [Chem.MolFromSmiles(smi) for smi in smiles]

if __name__ == "__main__":
    freeze_support()

    
    #print(mols)

    # Create Calculator
    calc = Calculator(descriptors)

    # map method calculate multiple molecules (return generator)
    #print(list(calc.map(mols)))

    # pandas method calculate multiple molecules (return pandas DataFrame)
    data = calc.pandas(mols)
    print(data)
    #data.to_csv('../ai/substituted_benzene_mono_md.csv')
# 需要对dataframe添加名字列，好和γ值对应
    namelist = []
    for i in range(len(mols)):
        namelist.append('benzenemono_'+str(i))
    namedict = {'name':namelist}
    print(namedict)
    df = pd.DataFrame.from_dict(namedict)
    n = pd.concat([data, df], axis=1)
    n.to_csv('../ai/substituted_benzene_para_md.csv')
