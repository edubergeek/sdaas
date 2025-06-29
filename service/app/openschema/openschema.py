import os
import glob
import threading
import fnmatch
import json
import pandas as pd


class OpenSchema():
  def __init__(self, args):
    try:
      self.catalogFile = args['catalog']
    except RuntimeError:
      self.catalogFile = 'catalog.json'
    try:
      self.port = args['port']
    except RuntimeError:
      self.port = 8000
    try:
      self.Catalog()
    except RuntimeError:
      print("Cannot load catalog: ", self.catalogFile)
      current_directory = os.getcwd()
      print("Current directory:", current_directory)
    self.filter = []
    
  def Catalog(self):
    f = open(self.catalogFile)
    self.catalog = json.load(f)
    f.close()
    return self.catalog

  def ListDatasets(self):
    dsList = []
    dsStatus = -1

    # Validate self.catalog
    try:
      my_catalog = self.catalog
    except NameError:
      return {"response": "Undefined variable: self.catalog", "status": dsStatus}

    for dataset in self.catalog['dataset']:
      ds = { "id": dataset["id"], "name": dataset["name"] }
      dsStatus = 0
      dsList.append(ds)
    return { "response": dsList, "status": dsStatus }
        
  def SelectDataSet(self, dsid):
    self.selectedDataSet = 0
    for dataset in self.catalog['dataset']:
      if(dataset['id'] == dsid):
        break
      self.selectedDataSet += 1
    if self.selectedDataSet >= len(self.catalog['dataset']):
      raise Exception("Non-existent dataset %s" %(dsid))
        
  def GetDataset(self, dsid):
    dsInfo = {}
    dsStatus = -1
    try:
      self.SelectDataSet(dsid)
    except RuntimeError:
      return {"response": "Invalid dataset id: " + dsid, "status": dsStatus}
    ds = self.catalog['dataset'][self.selectedDataSet]
    dsInfo["name"] = ds["name"]
    dsInfo["contact"] = ds["contact"]["name"]
    dsInfo["email"] = ds["contact"]["email"]
    #dsInfo["description"] = ds["description"]
    dsInfo["publication"] = ds["publication"]["title"]
    dsInfo["citation"] = ds["publication"]["citation"]
    dsInfo["url"] = ds["publication"]["url"]
    dsInfo["doi"] = ds["publication"]["doi"]
    dsInfo["namespace"] = ds["namespace"]
    dsInfo["origin"] = ds["osdf_origin"]
    dsInfo["files"] = ds["files"]
    dsInfo["mean_file_size"] = ds["file_size_mean"]
    dsInfo["file_size_units"] = ds["file_size_unit"]
    dsInfo["volume"] = ds["volume"]
    dsInfo["volume_units"] = ds["volume_unit"]
    dsInfo["path"] = ds["bag"][0]
    dsInfo["extension"] = ds["type"]
    dsStatus = 0
    return { "response": dsInfo, "status": dsStatus }
        
  def GetFilter(self, dsid):
    dsStatus = -1
    try:
      self.SelectDataSet(dsid)
    except RuntimeError:
      return {"response": "Invalid dataset id: " + dsid, "status": dsStatus}
    ds = self.catalog['dataset'][self.selectedDataSet]
    dsFilter = {}
    try:
      dsFilter["name"] = ""
      dsFilter["parameter"] = {}
      dsFilter["attribute"] = {}
      for idx in range(len(ds["parameter"])):
        dsFilter["parameter"][ds["parameter"][idx]] = ""
      if ds["type"] == "csv":
        for idx in range(len(ds["csv"]["attribute"])):
          dsFilter["attribute"][ds["csv"]["attribute"][idx]] = ""
    except RuntimeError:
      return {"response": "Cannot load filter for id: " + dsid, "status": dsStatus}
    dsStatus = 0
    return { "response": dsFilter, "status": dsStatus }
        
  def SetFilter(self, dsid, schema):
    dsStatus = -1
    try:
      self.SelectDataSet(dsid)
    except RuntimeError:
      return {"response": "Invalid dataset id: " + dsid, "status": dsStatus}
    ds = self.catalog['dataset'][self.selectedDataSet]
    try:
      dsFilter = self.SetDatasetFilter(dsid, schema)
    except RuntimeError:
      return {"response": "Cannot set filter for id: " + dsid, "status": dsStatus}
    dsStatus = 0
    return { "response": dsFilter, "status": dsStatus }
        
  def SetDatasetFilter(self, dsid, schema):
    self.selectedFilter = 0
    for filt in self.filter:
      if filt['dataset'] == dsid and filt['name'] == schema['name']:
        break
      self.selectedFilter += 1
    if self.selectedFilter >= len(self.filter):
      self.filter.append({})
      self.filter[self.selectedFilter]['dataset'] = dsid
      self.filter[self.selectedFilter]['name'] = schema['name']
    self.filter[self.selectedFilter]["parameter"] = schema["parameter"]
    self.filter[self.selectedFilter]["attribute"] = schema["attribute"]
    dsStatus = 0
    return { "response": self.filter[self.selectedFilter], "status": dsStatus }

  def ListFilters(self):
    dsList = []
    dsStatus = -1

    # Validate self.catalog
    try:
      my_filter = self.filter
    except NameError:
      return {"response": "Undefined variable: self.filter", "status": dsStatus}

    for filt in self.filter:
      dsf = { "id": filt["dataset"], "name": filt["name"] }
      dsStatus = 0
      dsList.append(dsf)
    return { "response": dsList, "status": dsStatus }
        
  def Bags(self):
    return len(self.catalog['dataset'][self.selectedDataSet]['bag'])

  def BagList(self):
    return self.catalog['dataset'][self.selectedDataSet]['bag']

  def Bag(self, bagnum):
    if bagnum >= self.Bags():
      raise Exception("Invalid bagnum %d" %(bagnum))
    bag = self.BagList()
    return bag[bagnum]

  def Root(self):
    return self.Bag(0)

  def Leaf(self):
    return self.BagList()[self.Bags()-1]

  def BagPath(self, seperator='/'):
    return seperator.join(self.BagList())
    
#    fmt = self.DataSetXFilePattern()
#    glob = fmt.format(*[p for p in params])

  def Type(self):
    return self.catalog['dataset'][self.selectedDataSet]['type']

  def Extension(self):
    type = self.Type()
    return self.catalog['dataset'][self.selectedDataSet][type]['extension']

  def IsMultiple(self):
    return self.catalog['dataset'][self.selectedDataSet]['multiple']

  def IsAtomic(self):
    return self.catalog['dataset'][self.selectedDataSet]['atomic']

  def Manifest(self, x_pattern, y_pattern=[], args=[], sort=False):
    path=self.DataSetRootPath()
    if len(args): #if we have some args to substitute then do so
      x_file_glob = x_pattern.format(*[a for a in args])
    else:         #otherwise just match the pattern itself
      x_file_glob = x_pattern
   
    matched=[]
    with os.scandir(path) as it:
      for entry in it:
        if not entry.name.startswith('.') and entry.is_file():
          if fnmatch.fnmatch(entry.name, x_file_glob):
            matched.append(entry.name)
    if sort: 
      return sorted(matched)
    return matched

  def _scandir(self, dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

  def BagGenerator(self, args=[], sort=False, name=None):
    if name is None:
      name = self.Root()
    if len(args): #if we have some args to substitute then do so
      globpat = name.format(*[a for a in args])
    else:         #otherwise just match the pattern itself
      globpat = name
    
    globpart=globpat.split('/')
    for n in range(len(globpart)):
      globstr = os.path.join(self.Root(), '/'.join(globpart[:n+1]))
      with os.scandir(name) as it:
        for entry in it:
          if not entry.name == '..' and entry.is_dir():
            if fnmatch.fnmatchcase(entry.path, globstr):
              yield entry.path
            else:
              return self.BagGenerator(args, sort, entry.path)
    yield name


  def AtomicBagGenerator(self, args=[], sort=False): 
    name = self.Leaf()
    if len(args): #if we have some args to substitute then do so
      globpat = name.format(*[a for a in args])
    else:         #otherwise just match the pattern itself
      globpat = name

    for matchdir in self.BagGenerator(args, sort):
      matched=[]
      with os.scandir(matchdir) as it:
        print("Scanning ", matchdir)
        for entry in it:
          if entry.is_file():
            #print("Matching", entry.name, "to", globpat)
            if fnmatch.fnmatchcase(entry.name, globpat):
              matched.append(entry.path)
      if sort: 
        matched = sorted(matched)
      for fname in matched:
        yield fname
   
  def ManifestGlob(self, glob_pattern):
    ds = self.catalog['dataset'][self.selectedDataSet]
    glob_str = os.path.join(self.DataSetRootPath(), glob_pattern)
    return glob.glob(glob_str)

  def Parameters(self):
    ds = self.catalog['dataset'][self.selectedDataSet]
    param = ds['parameter']
    return param
    
    
