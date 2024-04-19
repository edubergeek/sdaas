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
