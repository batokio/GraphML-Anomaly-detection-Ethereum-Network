# GraphML-Anomaly-detection-Ethereum-Network

An anomaly detection analysis performed on the Ethereum network using the DeltaCon algorithm.

## 1.  Settings

In addition to the common Python libraries, our model requires the installation of the following packages: 
- `NetworkX`
- `Scipy`

## 2.  Dataset : Transaction Network of Ethereum

The Transaction Network is the network of all Ethereum transaction, made by users, either to other users or smart contracts, or to a *Null* address in case of smart contract creation. In the context of this project, the analysis focuses only on the peer-to-peers transactions (e.g. excluding smart contracts and interactions involving a *Null* address).


