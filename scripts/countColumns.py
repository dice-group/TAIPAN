from taipan.T2D.Sampler import T2DSampler

t2dSampler = T2DSampler()
tables = t2dSampler.getTablesSubjectIdentificationGoldStandard()

columns = 0
for table in tables:
    columnsTable = len(table.table[0])
    if(table.subjectColumn != -1):
        columnsTable = columnsTable - 1
    columns += columnsTable

print columns
