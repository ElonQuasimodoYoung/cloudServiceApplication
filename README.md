# COMP90024 Cluster And Cloud Computing Semester 1 Assignment 2 - Big Data Analytics on the Cloud (Group 11)

## Brief Introduction.
This repository is related to build a non-trivial cloud software system for data analysis. The technologies the system 
is based on includes Melbourne Research Cloud, Kubernetes, Fission and ElasticSearch. The Melbourne Research Cloud 
id based on the OpenStack and provides the system cloud infrastructure. The kubernetes is used to the deployment, scaling, 
operation and management for application containers. As an open-source and serverless framework, the Fission is used to
help to deploy and manage functions in the Kubernetes cluster. The ElasticSearch helps the system to search, analyze, 
and visualize large volumes of data in real-time. For simplicity, you can treat the Fission, ElasticSearch and JupterNotebook 
as the backend, database and frontend of this system respectively.

## Repository Structure.
**Backend folder** includes fission functions for uploading data from various sources to ElasticSearch and getting data 
from the ElasticSearch for frontend statistical analysis. The sub-folders of the Backend folder that names start with "add" 
contain Python scripts and Node.js scripts for obtaining SUDO data, external data and real-time data. The sub-folder of 
Backend folder that name starts with "get" contains Python scripts for querying data from the ElasticSearch.<br><br>
**Data folder** includes SUDO(Spatial Urban Data Observatory) data that should be uploaded to ElasticSearch from the local 
machine. It includes income dataset and Tasmania crash dataset.<br><br>
**Database folder** includes shell scripts creating ElasticSearch indexes for all datasets we make use of.<br><br>
**Docs folder** includes links to access our assignment report, data source and API documentation of external data source. 
The K8s cluster installation instruction(Credit: Luca Morandini, https://gitlab.unimelb.edu.au/feit-comp90024/comp90024/-/tree/master/installation) 
is also in this file.<br><br>
**Frontend folder** includes the Jupyternotebook file of statistical analysis for our data in the ElasticSearch.<br><br>
**Test folder** includes the Python test script for the Python script that obtains and processes data from the ElasticSearch
in the backend folder.<br><br>
**Project Report** is the pdf file called CCC2024-Report-Team11.pdf.

## Kubernetes cluster deployment
Refer to the "k8s_installation_README.md" in the docs folder.(Credit: Luca Morandini, https://gitlab.unimelb.edu.au/feit-comp90024/comp90024/-/tree/master/installation)

## Deployment of clients
Before deploying clients, Python and Node.js environment should be established by running the following shell command: <br>
```
fission env create --name python --image fission/python-env --builder fission/python-builder
fission env create --name nodejs --image fission/node-env --builder fission/node-builder
```
Of course, source the openstack api, login to the bastion node of cluster is necessary, but we omit them here.
### addairdata fission function
First, in case any potential issues, delete timer, fission package and fission function(As we noticed the fission package 
update and fission function update didn't work sometimes when developing).<br>
```
fission timer delete --name everytenminuteair
fission function delete --name addair
fission package delete --name addair
```
Then, in the addairdata folder, create a fission package named "addair":<br>
```
fission package create --sourcearchive ./addair.zip \
    --env python \
    --name addair \
    --buildcmd './build.sh'
```
Next, create a fission function named "addair" by using the package we created before:<br>
```
fission function create --name addair \
    --pkg addair \
    --env python \
    --entrypoint "addair.main"
```
Finally, create a timer that calls the fission function "addair" every ten minutes:<br>
```
fission timer create --name everytenminuteair --function addair --cron "@every 10m"
```
Now, a client that harvests real-time air quality data of Ballarat City is established. This client will collect a piece 
of Ballarat air quality data every ten minutes and upload it into the ElasticSearch index designated for Ballarat air 
quality data.<br>
### addcrash fission function
In the addcrashdata folder, run the following command to call function addcrashdata.<br>
```
node addcrashdata.js
```
Now, a client called addcrashdata will upload the SUDO Tasmania crash dataset in the data folder to the
ElasticSearch index designated for the Tasmania crash data. As the SUDO Tasmania crash dataset is static data, we don't 
need to set a fission timer trigger to call it every certain time intervals.<br>
### addincome fission function
In the addincomedata folder, run the following command to call function loadIncome.<br>
```
node loadIncome.js
```
Now, a client called loadIncome will upload the SUDO Income dataset in the data folder to the
ElasticSearch index designated for the SUDO Income dataset. As the SUDO Income dataset is static data, we don't 
need to set a fission timer trigger to call it every certain time intervals.<br>
### addsentiments fission function
First, in case any potential issues, delete fission package and fission function(As we noticed the fission package 
update and fission function update didn't work sometimes when developing).<br>
```
fission function delete --name addsentiments
fission package delete --name addsentiments
```
Then, in the addsentimentsdata folder, create a fission package named "addsentiments":<br>
```
fission package create --sourcearchive ./addsentiments.zip \
    --env python \
    --name addsentiments \
    --buildcmd './build.sh'
```
Next, create a fission function named "addsentiments" by using the package we created before:<br>
```
fission function create --name addsentiments \
    --pkg addsentiments \
    --env python \
    --entrypoint "addsentiments.main"
```
Now, a client that harvests sentiments data of is established. This client will collect sentiments data from 
external data source by API and upload it into the ElasticSearch index designated for sentiments data.<br>
### addweather fission function
First, in case any potential issues, delete timer, fission package and fission function(As we noticed the fission package 
update and fission function update didn't work sometimes when developing).<br>
```
fission timer delete --name everytenminute
fission function delete --name addweather
fission package delete --name addweather
```
Then, in the addweatherdata folder, create a fission package named "addweather":<br>
```
fission package create --sourcearchive ./addweather.zip \
    --env python \
    --name addweather \
    --buildcmd './build.sh'
```
Next, create a fission function named "addweather" by using the package we created before:<br>
```
fission function create --name addweather \
    --pkg addweather \
    --env python \
    --entrypoint "addweather.main"
```
Finally, create a timer that calls the fission function "addweather" every ten minutes:<br>
```
fission timer create --name everytenminute --function addweather --cron "@every 10m"
```
Now, a client that harvests real-time weather data of Ballarat City is established. This client will collect a piece 
of Ballarat weather data every ten minutes and upload it into the ElasticSearch index designated for Ballarat 
weather data.<br>
### getcrash and getsumsentiments fission function
First, in case any potential issues, fission package and fission functions(As we noticed the fission package 
update and fission function update didn't work sometimes when developing).<br>
```
fission function delete --name getcrash
fission function delete --name getsumsentiments
fission package delete --name getdata
```
Then, in the getdata folder, create a fission package named "getdata":<br>
```
fission package create --sourcearchive ./getdata.zip \
    --env python \
    --name getdata \
    --buildcmd './build.sh'
```
Next, create fission functions named "getcrash" and "getsumsentiments" by using the package we created before:<br>
```
fission function create --name getcrash \
    --pkg getdata \
    --env python \
    --entrypoint "getcrash.main"
```
```
fission function create --name getsumsentiments \
    --pkg getdata \
    --env python \
    --entrypoint "getsumsentiments.main"
```

Finally, create routes that call the fission function "getcrash" and "getsumsentiments" from outside of cluster:<br>
```
fission route update --name getcrashbyx --function getcrash \
    --method GET \ 
    --url '/crash/field/{field:[a-zA-Z _]*}/para/{para:.*}'
```
```
fission route create --name getsumsentiment --function getsumsentiments \ 
    --method GET \ 
    --url '/sentiments/country/{country:[a-zA-Z]+}/field/{field:[a-zA-Z]+}'
```
Now, clients that query data from the ElasticSearch and then process data are established.<br>

## Team
**Donghao Yang**(Student ID:1514687, Email: donghao1@student.unimelb.edu.au)<br>
**Role:** K8S cluster deployment, ElasticSearch index management, static data collection client deployment, 
real-time data collection client deployment, report writing, Gitlab repository management.<br>

**Ziqiang Li**(Student ID: 1173898, Email: ziqiangl1@student.unimelb.edu.au)<br>
**Role:** ElasticSearch index management, static data collection client deployment, 
real-time data collection client deployment, report writing. <br>

**Rui Mao**(Student ID: 1469805, Email: ruimao1@student.unimelb.edu.au)<br>
**Role:** Frontend data analysis, test, ElasticSearch index management, backend data processing, 
static data collection client deployment, external static data collection client deployment, 
real-time data collection client deployment, report writing, YouTube video recoding.<br>

**Xiaxuan Du**(Student ID: 1481272, Email: xiaxuand@student.unimelb.edu.au)<br>
**Role:** K8S cluster deployment, frontend data analysis, static data collection client deployment, 
external static data collection client deployment, report writing, YouTube video recoding.<br>

**Ruoyu Lu**(Student ID: 1466195, Email: rlu3@student.unimelb.edu.au)<br>
**Role:** K8S cluster deployment, report writing, Gitlab repository management.<br>


## Reference
[1] Ballarat Air Quality Data Api Documentation: https://data.ballarat.vic.gov.au/explore/dataset/air-quality-observations/api/?disjunctive.location_description <br>
[2] Ballarat Air Quality Data Source: https://discover.data.vic.gov.au/dataset/air-quality-observations <br>
[3] Ballarat Weather Data source: https://reg.bom.gov.au/products/IDV60801/IDV60801.94852.shtml <br>
[4] Income Data Source and Tasmania Crash Data Source: https://sudo.eresearch.unimelb.edu.au/ <br>
[5] Sentiments Data Source: https://api.ado.eresearch.unimelb.edu.au/analysis/place/collections/twitter <br>
[6] Sentiments Data Api Documentation: https://www.ado.eresearch.unimelb.edu.au/api-documentation/ <br>
[7] K8s installation, fission deployment and ElasticSearch deployment guide: https://gitlab.unimelb.edu.au/feit-comp90024/comp90024/-/tree/master/installation <br><br>

## Thanks! Live long and prosper.
