from rdkit import Chem 

smipath = '../Molecules'

####################################################################################################
#此处生成smiles并去重，标准化
withdrawing = ['(N(=O)(=O))','(C#N)','(C(=O)(O))','(S(=O)(=O)(O))','(CO)','(C(=O)(C))']
donor = ['(N)','(NC)','(N(C)(C))','(O)','(NC(=O)C)','(OC(=O)(C))','(C)','(F)','(Cl)',]
# benzene and its monosubstituent
bnezene = 'c1ccccc1'
monosubstituent = []
for group in withdrawing:
    monosubstituent.append(bnezene+group)
for group in donor:
    monosubstituent.append(bnezene+group)
#去重
mols = [Chem.MolFromSmiles(smi) for smi in monosubstituent]
monosubstituent =list(set( [Chem.MolToSmiles(mol) for mol in mols]))

# metasubstitution
metasubstitution = []
for group in withdrawing:
    for g in withdrawing:
        metasubstitution.append('c1'+group+'cc'+g+'ccc1')
    for f in donor:
        metasubstitution.append('c1'+group+'cc'+f+'ccc1')
for group in donor:
    for g in withdrawing:
        metasubstitution.append('c1'+group+'cc'+g+'ccc1')
    for f in donor:
        metasubstitution.append('c1'+group+'cc'+f+'ccc1')
#去重
mols = [Chem.MolFromSmiles(smi) for smi in metasubstitution]
metasubstitution =list(set( [Chem.MolToSmiles(mol) for mol in mols]))

# orthosubstituent
orthosubstituent = []
for group in withdrawing:
    for g in withdrawing:
        orthosubstituent.append('c1'+group+'c'+g+'cccc1')
    for f in donor:
        orthosubstituent.append('c1'+group+'c'+f+'cccc1')
for group in donor:
    for g in withdrawing:
        orthosubstituent.append('c1'+group+'c'+g+'cccc1')
    for f in donor:
        orthosubstituent.append('c1'+group+'c'+f+'cccc1')
#去重
mols = [Chem.MolFromSmiles(smi) for smi in orthosubstituent]
orthosubstituent =list(set( [Chem.MolToSmiles(mol) for mol in mols]))

# paraorienting
paraorienting = []
for group in withdrawing:
    for g in withdrawing:
        paraorienting.append('c1'+group+'ccc'+g+'cc1')
    for f in donor:
        paraorienting.append('c1'+group+'ccc'+f+'cc1')
for group in donor:
    for g in withdrawing:
        paraorienting.append('c1'+group+'ccc'+g+'cc1')
    for f in donor:
        paraorienting.append('c1'+group+'ccc'+f+'cc1')
#去重
mols = [Chem.MolFromSmiles(smi) for smi in paraorienting]
paraorienting =list(set( [Chem.MolToSmiles(mol) for mol in mols]))


###############################################################################################
#以下生成smi文件

with open (smipath+'/substituted_benzene_para.smi','w') as f:
    for smi in paraorienting:
        f.write(smi+'\n')
with open (smipath+'/substituted_benzene_orth.smi','w') as f:
    for smi in orthosubstituent:
        f.write(smi+'\n')
with open (smipath+'/substituted_benzene_meta.smi','w') as f:
    for smi in metasubstitution:
        f.write(smi+'\n')
with open (smipath+'/substituted_benzene_mono.smi','w') as f:
    for smi in monosubstituent:
        f.write(smi+'\n')


################################################################################################
