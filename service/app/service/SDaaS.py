import os
import glob
import threading
import fnmatch
import json
import pandas as pd


class DataManifest():
  def __init__(self, root_path, pattern, args=[], sort=False):
    self.root_path = root_path
    self.pattern = pattern
    self.args = args
    self.sort = sort
    xpattern = os.path.join(pattern["x"]["path"], pattern["x"]["file"])
    xpattern = os.path.join(root_path, xpattern)
    if len(args):              #if we have some args to substitute then do so
      self.xfullglob = xpattern.format(*[a for a in args])
    else:                      #otherwise just match the pattern itself
      self.xfullglob = xpattern

  def __iter__(self):
    self.walker = os.scandir(self.root_path)
    return self

  def __next__(self):
    entry = next(self.walker)
    if entry.is_dir(): # TODO fnmatch entry.path against left side of pattern
      next_walker = iter(DataManifest(entry.path, self.pattern, self.args, self.sort))
      return next(next_walker)
    if entry.is_file():
      if fnmatch.fnmatchcase(entry.path, self.xfullglob):
        yield entry.path
    return None



# +

class SDAAS():
  def __init__(self, args):
    self.catalogFile = args['catalog']
    self.port = args['port']
    
  def Catalog(self):
    f = open(self.catalogFile)
    self.catalog = json.load(f)
    f.close()
    return self.catalog

  def SelectDataSet(self, id):
    self.selectedDataSet = 0
    for dataset in catalog['dataset']:
      if(dataset['id'] == id):
        break
      self.selectedDataSet += 1
    if self.selectedDataSet >= len(catalog['dataset']):
      raise Exception("Non-existent dataset %s" %(id))
        
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
    
# -

if __name__ == "__main__":
  params = {
      'catalog': './catalog.json',
      'dataset': 'ATLAS_DR1',
      'port': 9001
  }
  sdaas = SDAAS(params)
    
  catalog = sdaas.Catalog()
  print(catalog)

    
  for dataset in catalog['dataset']:
    dataset_id = dataset['id']
    dataset_name = dataset['name']
    print('[%s]=%s' %( dataset_id, dataset_name))

  sdaas.SelectDataSet('ATLAS_DR1')
  root_path = sdaas.Root()
  print(root_path)

  print(sdaas.Bag(1))
  
  print(sdaas.BagPath())

  print(sdaas.Type())

  for param in sdaas.Parameters():
    print(param)

  dec_from='0[0-1]*'
  dec_upto='0[0-1]*'
#  year = '2021'
#  month = '12'
#  day = '25'
#  hour = '09'
#  minute = '00'
#  second = '38'

#  x_files = sdaas.DataManifest(x_pattern, y_pattern, [dec_from, dec_upto], sort=False)
#  print(x_files)


  print(dec_from, dec_upto)
  args = [dec_from, dec_upto]
  
  for matchdir in sdaas.BagGenerator(args):
    print(matchdir)


# +
  for fname in sdaas.AtomicBagGenerator(args, sort=True):
    print(fname)




# -

def read_bag(bagname, bag, batch_size, offset=0, completed = None):
  try:
    df = pd.read_csv(bagname, nrows=batch_size, skiprows=offset)
    if len(df) == 1:
      completed[bag] = True
      print("Bag", bag, "is complete")
    return df
  except pd.errors.EmptyDataError:
    completed[bag] = True
    print("Bag", bag, "is complete")
  return pd.DataFrame()  



def multi_threaded_bag_reader(bags, batch_size=16, threads=2):
  shards = []
  bags_end = []
    
  # Define the worker function
  def read_bag_thread(bagname, b, batch_size, offset, completed):
    result = read_bag(bagname, b, batch_size, offset, completed)
    if not completed[b]:
      shards.append(result)

  # how many "bags" (files) we need to process
  bag_count = len(bags)
    
  # initialize the bags_end list to False for each bag
  for b in range(bag_count):
    bags_end.append(False)
     
  offset = 0
  iters = 0
  # loop until all bags are completed
  while False in bags_end:
    # start with no workers
    workers = []
    # all workers start a new bag at offset 0
     
    # Find some bags that are not completed and run a worker thread
    w = 0
    while w < threads:
      for b in range(bag_count):
        # still some work left to do
        if not bags_end[b]:
          #print("worker", w, "Bag", b, "Offset", offset)
          worker = threading.Thread(target=read_bag_thread, args=(bags[b], b, batch_size, offset, bags_end,))
          workers.append(worker)
          worker.start()
        w += 1

    # Wait for all threads to finish
    for worker in workers:
      worker.join()

    iters += 1
    
    if len(workers) == 0:
      print(bags_end.count(True), "workers done in", iters, "iterations.")
      break
    
    if iters % 10 == 0:
      print(bags_end.count(True), "workers done in", iters, "iterations.")
    # More work to do, keep calm and carry on ...
    offset += batch_size
    
  return shards


bags = []
for bag in sdaas.AtomicBagGenerator(args, sort=True):
  bags.append(bag)

print(len(bags))

shards = multi_threaded_bag_reader(bags, batch_size=2**18, threads=2)
print(len(shards))

shards[0].describe()


shards[-1].describe()

shards[0].iloc[20:40].head(20)

shards[1].iloc[10:20].head(10)

# +
#  sdaas.Stream(x_manifest, y_manifest, batch_size=1, threads=1, port=33000)
