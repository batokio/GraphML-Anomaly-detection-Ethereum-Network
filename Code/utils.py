#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 16:23:03 2022

@author: Bryan
"""

from imports import *


# Function that returns the list of nodes in both graphs
def add_missing_nodes(G1, G2):
  union = G1.nodes() | G2.nodes()
  return list(union)

# Function that lists every nodes and weight to create the weighted directed graph
def tuples_graph(df):
  new_df = df[['from_address_idx', 'to_address_idx', 'value_eth']]
  tuples_graph = [tuple(x) for x in new_df.to_numpy()]
  return tuples_graph


# Function that creates two directed graphs having the same node set
def create_new_graph(G1, G2, df1, df2):
  unions = add_missing_nodes(G1, G2)
  tuples_graphs1 = tuples_graph(df1)
  tuples_graphs2 = tuples_graph(df2)
  new_G1 = nx.DiGraph()
  new_G2 = nx.DiGraph()
  new_G1.add_nodes_from(unions)
  new_G1.add_weighted_edges_from(tuples_graphs1)
  new_G2.add_nodes_from(unions)
  new_G2.add_weighted_edges_from(tuples_graphs2)  
  return new_G1, new_G2

# Function plotting lollipop chart
def lollipop_chart(similarities_df, k=2):
    '''
    

    Parameters
    ----------
    similarities_df : Dataframe
        Similarity scores for each combination of consecutive subgraph.
    k : Integer, optional
        Variable controlling the Upper Control Limit. The default is 2.

    Returns
    -------
    Lollipop chart

    '''
    data = similarities_df.similarity 
    x= similarities_df.time
    
    line = [np.mean(data)]*len(x)
    LCL = [max(np.median(data) - k*np.std(data),0)]*len(x)
    UCL = [np.median(data) + k*np.std(data)]*len(x)
    
    ref_line = line-data
    
    # lollipop chart 
    plt.figure(figsize=(20,15))
    plt.stem(x, data, bottom = np.mean(data), use_line_collection= True)
    plt.plot(x, line)
    plt.plot(x, LCL, "r--")
    plt.plot(x, UCL, "r--")
    plt.xticks(rotation=90)
    plt.show()
    
    
# Funtion that returns the list of similarity scores
def sim_computation(list_timelines):
    
    similarity = []
    
    for i in tqdm(range(len(list_timelines)-1)):
    
        # Get the dataframes
        df1 = pd.read_csv(savepath+ file_names[i], sep = ',',
                          dtype={"from_address_idx": str, 
                                 "to_address_idx": str, 
                                 "value_eth":float, 
                                 "gas_price_eth":float,
                                 "receipt_gas_used_eth": str
                                 }
                          )
        
        df2 = pd.read_csv(savepath+ file_names[i+1], sep = ',',
                      dtype={"from_address_idx": str, 
                             "to_address_idx": str, 
                             "value_eth":float, 
                             "gas_price_eth":float,
                             "receipt_gas_used_eth": str
                             }
                      )
        
    
        # Create graphs
        G1 = nx.from_pandas_edgelist(df1, 'from_address_idx', 'to_address_idx')
        G2 = nx.from_pandas_edgelist(df2, 'from_address_idx', 'to_address_idx')
        
        # Get the weighted graphs
        n_G1, n_G2 = create_new_graph(G1, G2, df1, df2)
        
        # Compute the similarity with Deltacon
        sim = DeltaCon(n_G1, n_G2)
        
        # append the similarity list
        similarity.append(sim)
    
    return(similarity)