# GraphML-Anomaly-detection-Ethereum-Network

An anomaly detection analysis performed on the Ethereum network using the DeltaCon algorithm.

## 1.  Settings

In addition to the common Python libraries, our model requires the installation of the following packages: 
- `NetworkX`
- `Scipy`

## 2.  Dataset : Transaction Network of Ethereum

The Transaction Network is the network of all Ethereum transaction, made by users, either to other users or smart contracts, or to a *Null* address in case of smart contract creation. In the context of this project, the analysis focuses only on the peer-to-peers transactions (e.g. excluding smart contracts and interactions involving a *Null* address).

## 3. Anomaly Detection

The analysis is performed on the period ranging from January 19, 2022 to January 24, 2022. Over this period, the market capitalization of Ethereum declined by almost 50%. The goal is to find if it is possible to detect significant price drops through graph analysis.

## 4. Data Extraction from Google Cloud BigQuery

1. Login to Google Cloud Platform. 
2. Create a bucket to store your files.
2. Go to BigQuery and find the data set 'ethereum_blockchain'
3. Select the table you want and 'Export to GCS'.
4. Then select the GCS location (the bucket created in step 2). 
5. If csv is preferred: <bucket>/<folder>/file*.csv (e.g. tmpbucket/blocks/blocks*.csv). <bR>
   The * will help to number the files as exporting the tables will split the data into multiple files. <br>
   Replace .csv with .txt or .json as per your preference.
6. Pip install gsutil, open command line and download the files. (Tried with Python 3.9)<br>
   For downloaded entire folder: gsutil -m cp -r gs://bucketname/folder-name local-location <br>
   For downloaded multiple files: gsutil -m cp -r gs://bucketname/folder-name/filename* local-location<br>

Manual download is also possible from the bucket (not recommended).<br>
After downloaded the necessary data you might want to delete the bucket to prevent charges.<br>
Alternative method: https://github.com/blockchain-etl/ethereum-etl <br>
