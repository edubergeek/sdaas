import os
import json


class SDAAS():
  def __init__(self, args):
    self.catalogFile = args['catalog']
    
  def Catalog(self):
    f = open(self.catalogFile)
    self.catalog = json.load(f)
    f.close()
    return self.catalog

  def SelectDataSet(self, name):
    self.selectedDataSet = 0
    for dataset in catalog['catalog']:
      if(dataset['name'] == name):
        break
      self.selectedDataSet += 1
    if self.selectedDataSet >= len(catalog['catalog']):
      self.selectedDataSet = 0
        
  def DataSetPath(self):
    return self.catalog['catalog'][self.selectedDataSet]['path']

  def DataSetExtension(self):
    return self.catalog['catalog'][self.selectedDataSet]['extension']

  def DataManifest(self):
    filelist = [file for dirs in os.walk(self.DataSetPath(), topdown=True)
        for file in dirs[2] if file.endswith(self.DataSetExtension())]
    return filelist


if __name__ == "__main__":
  params = {
      'catalog': './catalog.json',
      'dataset': 'ATLAS-VAR',
  }
  sdaas = SDAAS(params)
  catalog = sdaas.Catalog()
  for dataset in catalog['catalog']:
    dataset_name = dataset['name']
    print(dataset_name)
  
  sdaas.SelectDataSet('ATLAS-VAR')
  print(sdaas.DataSetPath())
  print(sdaas.DataSetExtension())

  manifest = sdaas.DataManifest()
  for fname in manifest:
    print(fname)


