# Catalog JSON Description
Each available dataset declares a description of structure, contents and origin 

## Keys
- dataset - Singleton dict comprising an array of datasets
- namespace - global unique namespace of SDAAS
- id - namespace scope unique dataset identifier
- name - dataset user friendly name
- osdf_origin - OSDF origin
- contact - OSDF origin point of contact
- name - namespace contact name at origin
- email - namespace contact email address
- publication - publication information
- url - publication url
- title - publication title
- citation - publication authors
- doi - publication DOI
- path - root path to dataset on local server
- schema - path/file - file & path arg substition and globbing
- extension - file extension
- volume - disk space required for full dataset
- volume_unit - disk space units
- files - total file count for full dataset
- file_size_min - size of smallest file
- file_size_max - size of largest file
- file_size_mean - average size of file
- file_size_unit - file size units
- metadata_file - metadata self-description text files
- header - first row of data file lists column names e.g. csv file
- attribute - list of names for column e.g. for csv with no header
- dtype - list of panda data types for columns
- pattern_arg - list of args for path/file pattern substitution
- x - x is required and used to match  path and file patterns
- path_pattern - leaf directories based on pattern_arg value substitution
- file_pattern - object file composition with arg value substitution
- thumb_pattern - thumbnail img file
- file_dim - single input file dimension, 0=dynamic
- object_dim - composite object dimension before transforms, 0=dynamic
- composition - for composite objects, how to compose
    - method: "row" - append input rows to "axis" e.g. csv
    - method: "scan" - append to "axis" in "order"
    - method: "y" - get dynamic "axis" dim from same axis in "y"
- y - same as **x**, optional, intended for ML data patterns


## Example
```
{
  "dataset": [
    {
      "namespace": "UHIFA",
      "id": "ATLAS_DR1",
      "name": "ATLAS Variable Light Curves",
      "osdf_origin": "IFA_ITC_ORIGIN",
      "contact": {
        "name": "Curt Dodds",
        "email": "dodds@hawaii.edu"
      },
      "publication": {
        "url": "https://iopscience.iop.org/article/10.3847/1538-3881/aae47f",
        "title": "A First Catalog of Variable Stars Measured by ATLAS",
        "citation": "A. N. Heinze et al 2018 AJ 156 241",
        "doi": "10.17909/T9H98D"
      },
      "path": "/atlas/dr1",
      "schema": "path/file",
      "extension": "csv",
      "volume": 29,
      "volume_unit": "GB",
      "files": 285,
      "file_size_min": 0.016384,
      "file_size_max": 2188.304389,
      "file_size_mean": 792.338216,
      "file_size_unit": "MB",
      "metadata_file": [ "stats.txt" ],
      "header": 1,
      "attribute": ["ATO_ID","starID","ra","dec","CLASS","gmag","rmag","imag","z                                                                                                                                                             mag","ymag","prob_CBF","prob_CBH","prob_DBF","prob_DBH","prob_HARD","prob_MIRA",                                                                                                                                                             "prob_MPULSE","prob_MSINE","prob_NSINE","prob_PULSE","prob_SINE","prob_IRR","pro                                                                                                                                                             b_LPV","prob_dubious","fp_period","ls_Pday","fp_LSperiod","fp_lngfitper","vf_c_m                                                                                                                                                             ed","vf_o_med","mjd","dra","ddec","filter","m","dm" ],
      "dtype": ["string","string","float","float","string","float","float","floa                                                                                                                                                             t","float","float","float","float","float","float","float","float","float","floa                                                                                                                                                             t","float","float","float","float","float","float","float","float","float","floa                                                                                                                                                             t","float","float","float","float","float","string","float","float" ],
      "pattern_arg": [ "dec_from", "dec_upto" ],
      "x": {
        "path_pattern": "",
        "file_pattern": "atlas_lc_dr1_{0}-{1}.csv",                                                                                                                                                                                          
        "thumb_pattern": "",
        "file_dim": (0,36),
        "object_dim": (0,36),
        "composition": { "method": "row", "axis": 0, "order": "" }
      },
      "y": {
        "path_pattern": "",
        "file_pattern": "",
        "thumb_pattern": "",
        "file_dim": (),
        "object_dim": (),
        "composition": { "method": "", "axis": 0, "order": "" }
       }
    },
    {
      "namespace": "UHIFA",
      "id": "HINODE_SOT_SP",
      "name": "Hinode SOT SP",
      "osdf_origin": "IFA_ITC_ORIGIN",
      "contact": {
        "name": "Curt Dodds",
        "email": "dodds@hawaii.edu"
      },
      "publication": {
        "url": "",
        "title": "",
        "citation": "",
        "doi": ""
      },
      "path": "/hinode",
      "schema": "path/file",
      "extension": "fits",
      "volume": 12.321,
      "volume_unit": "TB",
      "files": 285,
      "file_size_min": 117.612028,
      "file_size_max": 2188.304389,
      "file_size_mean": 1000,
      "file_size_unit": "MB",
      "metadata": [],
      "header": 0,
      "attribute": [],
      "dtype": [],
      "pattern_arg": [
        "year",
        "month",
        "day",
        "hour",
        "minute",
        "second"
      ],
      "x": {
        "path_pattern": "level1/{0}/{1}/{2}/SP3D/{0}{1}{2}_{3}{4}{5}",
        "file_pattern": "*.fits",
        "thumb_pattern": "*_stksimg.save",
        "file_dim": (112,384,4),
        "object_dim": (384,0,112,4),
        "composition": { "method": "scan", "axis": 1, "order": "time" }
      },
      "y": {
        "path_pattern": "level2/{0}/{1}/{2}/SP3D/{0}{1}{2}_{3}{4}{5}",
        "file_pattern": "*.fits",
        "thumb_pattern": "thumbnails/*.png",
        "file_dim": (384,0,4),
        "object_dim": (384,0,112,4),
        "composition": { "method": "x", "axis": 1, "order": "" }
      }
    }
  ]
}
```

```python

```
