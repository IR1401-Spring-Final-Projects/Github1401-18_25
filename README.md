# Github1401-18_25
This project is a Retrival System defined based on Github Readmes. All the data are crawled from Github api. Additionally, the classification and clustring parts use codes from most starred repos. 

## How to run the project

First of all, for installing requirements run the command below. 

```
pip install -r requirements.txt
```

After that, you have to download fasttext model from this [link](https://drive.google.com/file/d/1pZGpzhVsPcWu4kkp2Yb5ISFYBKcyeIFo/view?usp=sharing) and unzip the downloaded file. Afterward, put the three unzipped files under the "Third" folder inside the root directory. 
Then run the main.py file under the root of the project. The GUI will be opened after a few seconds. 

## Structure of the Project
There have been 3 assignments that are merged in this project. The folder "Third", "Fourth", "Fifth" each contain the codes and notebooks for each assignments. The Report for each assignment is inside the notebook. 
In the third assignment, four different Retrival methods are implemented. All of them contain Query Expansion(QE). 
In the forth assginment, clustering and classification are implemented. 
In the fifth assignment, link prediction is implemented. This assignment did not have any specific result, so it is not used in the UI. 
In the final project, elasticsearch is implemented

## Elasticsearch 

Elasticsearch is a NoSQL, distributed, full-text database. Because of NoSQL, it doesn't require any structured data and does not use any standard structured query language for searching.

For setting up Elasticsearch locally You just have to download it and run the executable according to your system. Make sure that you have Java installed on your machine
Once you set up the local environment, you can verify whether it’s working by hitting http://localhost:9200 in your browser or via cURL. It should give you a JSON response like this:

```
{
  "name" : "1b415f1159de",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "xl2IFgFrSNOWCgov26hF5Q",
  "version" : {
    "number" : "7.9.2",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "d34da0ea4a966c4e49417f2da2f244e3e97b4e6e",
    "build_date" : "2020-09-23T00:45:33.626720Z",
    "build_snapshot" : false,
    "lucene_version" : "8.6.2",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

```

And for pythonizing it Elasticsearch provides REST APIs to manage data, but to use ES with Python efficiently, there is an official library called elasticsearch.
