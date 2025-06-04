# SDaaS
**Science Data as a Service**


## Overview
This package efficiently extracts, transforms and streams data over the network to a **SDaaS** client. It was created by [Curt Dodds](https://github.com/edubergeek), at the [Institute for Astronomy, University of Hawaii, Manoa](https://www.ifa.hawaii.edu/), to provide unsiloed access to astronomy big data that had been siloed on storage systems in Hawaii. It is designed to be easily extended with dataset specific features using class inheritance and overriding base methods.


## Open Access to Science Data
The author is a strong proponent of open access to science data and developed this software to solve the problem of datasets that are so large they cannot easily be moved from one location to another. Users of this software are encouraged to participate in the [National Data Platform](https://nationaldataplatform.org/), [Pelican Platform](https://pelicanplatform.org/), [Open Science Data Federation](https://osg-htc.org/services/osdf.html) and [National Research Platform](https://nationalresearchplatform.org/the-pacific-research-platform-prp-is-now-the-national-research-platform-nrp/) where this software will hopefully be integrated.


## Usage
For portability **SDaaS** is implemented as a service running in a docker container and a client running in a docker container. The service should be running adjacent to the location where the data is stored. There may be many client instances running anywhere with a network connection to the host running the **SDaaS** service.

Docker Compose may be used to run the docker container. An equivalent docker run command can also be used.

### Run the service
```
cd service
docker compose up -d
```
### Stop the service
```
cd service
docker compose down
```
### Run the client
```
cd client
docker compose up -d
```
### Stop the client
```
cd client
docker compose down
```
**or** from the main Jupyter menu in your browser, simply choose Quit at the upper right.


## Quick Start
We run a demo service at the [Institute for Astronomy, University of Hawaii, Manoa](https://www.ifa.hawaii.edu/) on host: data.ifa.hawaii.edu and port 7411. This service allows you to list available datasets. You can select a dataset and filter it, transform it and stream stream it to a client using **SDaaS**. To do this, run the Jupyter notebook [sdaas_demo.ipynb](./sdaas_demo.ipynb/).


# Taxonomy
1. Data model
    1. Bag of objects
    1. Examples are atomic objects
    1. A batch is a fixed size set of examples
1. Bag
    1. An ML training set is a bag of objects
    1. A dataset is a bag of objects
    1. A bag contains one or more objects (no empty bags)
1. Object
    1. An object may be a bag or an example
1. Example
    1. An example may be composable in which case it is a bag of objects with assembly instructions
    1. An example may be simple in which case it is a bag of one or more objects that require no assembly
    1. An example must be serializable (e.g. to a byte stream)
    1. All data comprising an example is associated in two subsets (X, Y) where Y can be an empty set but X is never empty.


# Generator Pipeline

## The Bag Manifest
1. Declare the hierarchical structure
    1. Bags of bags arbitrarily nested with semantic parameter substitution at each level
    1. Declare what is in a leaf bag
        1. Atomic single example (e.g. a png image file)
        1. Atomic multiple example, a set of examples contained in an object (e.g. a csv file or zip of images)
        1. Composable single example, a bag or list of objects to assemble into an object (e.g. PS1 warp image, Hinode level1)
    1. Composable objects require assembly instructions
    1. List objects that comprise the Y subset
        1. Default all objects to X subset
        1. Default Y subset is empty
        1. Explicitly declare which objects belong to Y subset
            1. This may use hierarchy semantics (e.g. Hinode level1 or level2 in path)
            1. This may use file glob semantics (e.g. filename matching for Y)
            1. This may use assembly instructions (e.g. ATLAS-DR1, Numerai)

### CSV file (ATLAS-DR1)
1. Bag
    1. A path (directory) e.g. **```"/atlas/dr1"```**
    1. A csv files containing examples (except the first row?)
1. Example
    1. CSV file
        1. Ignore first row
        1. Each row after 1 is an example
        1. One column (class) composes the Y subset
1. Parallelism
    1. Multiple CSV files can be processed in parallel
    1. Batch size samples can be streamed as they are processed from multiple files

### Complex FITS file assembly (Hinode)
1. Bag
    1. E.g. /hinode/level1/2017/08/20/SP3D/20170820_180544
    1. Root /hinode
    1. Bag hierarchy
        1. 0 "level1" (X) or "level2" (Y)
        1. 1 "year"
        1. 2 "month"
        1. 3 "day"
        1. 4 "SP3D" constant
        1. 5 "timestamp"
1. Example
    1. Bag 0 determines X vs Y subset e.g. "level1" vs "level2"
    1. Assembly
        1. X - shape () from *.fits sorted by file name (timestamp order)
            1. e.g. /hinode/**level1**/2017/08/20/SP3D/20170820_180544/*.fits
        1. Y - shape () from 0th bag == "level2" and "level2.1"
            1. e.g. /hinode/**level2**/2017/08/20/SP3D/20170820_180544/*.fits
            1. e.g. /hinode/**level2.1**/2017/08/20/SP3D/20170820_180544/*.fits
    
## Assemble An Example
1. Build a pipeline that emits pairs of training examples (x, y) where a file walk on XGlob is transformed
    1. first to an object representation of the X file(s)
    1. then paired with the matching object representation of the Y file(s) or features 
1. Y may not be from a file e.g. for categorical classification. Y may be a subset of X file features (class ordinal or code)
1. Continue pipeline with one or more filters then patch extraction then augmentation transforms

## Multithreading
1. Parallelize bagging (globbed file tree walk)
2. Parallelize batch generation (multiple assemblers append to a batch until batch is complete)

## Caching
1. Cache batches in memory to a limit
1. Cache batches to disk as an OSDF_ORIGIN that can be copied to an OSDF_CACHE
    1. Origin Namespace
    1. Dataset UUID
    1. Generator UUID - uniquely identify the unique set of batches generated by this process

```python

```
