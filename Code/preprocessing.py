#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 18:32:09 2022

@author: Bryan
"""

from imports import *

# Python script that takes as input the raw data
# and ouput a correspondance table between wallet addresse to indices

def wal_conversion_table(filepath, savepath):
    
    # load the file in a pandas dataframe
    df = pd.read_csv(filepath)
    
    # list every wallet addresses in lists
    source_addresses = []
    target_addresses = []
    
    # loop over the dataframe
    for row in tqdm(range(len(df))):
        source_addresses.append(df.from_address[row])
        target_addresses.append(df.to_address[row])
        
    
    # concatenate lists
    wallets = source_addresses + target_addresses
    
    # remove duplicate from the list
    wallets = np.unique(wallets).tolist()
    
    # print the number of single source / target wallets / unique wallet
    print("Number of sources: {:,}".format(len(np.unique(source_addresses))))
    print("Number of targets: {:,}".format(len(np.unique(target_addresses))))
    print("Number of wallets: {:,}".format(len(wallets)))
    
    # get the indices
    indices = np.arange(0, len(wallets)).tolist()
    
    
    # create a conversion dataframe
    conversion_df = pd.DataFrame(list(zip(wallets, indices)),
               columns =['wallet_address', 'index'])
    
    
    # save the conversion dataframe
    conversion_df.to_csv(path_or_buf= savepath + "conversion_df.csv", sep=',')
    
    return df, conversion_df

def preprocessing(token_transactions_df, conversion_df):
    
    # create a dictionary that will store the wallet_address and their corresponding index
    dictionary = conversion_df.set_index('wallet_address').to_dict()
    
    # create new from/to_address columns replace token addresses by their indices
    token_transactions_df['from_address_idx'] = token_transactions_df['from_address'].apply(lambda x: dictionary['index'][x])
    token_transactions_df['to_address_idx'] = token_transactions_df['to_address'].apply(lambda x: dictionary['index'][x])
    
    # create new value and gas columns in ETH
    # 1 ETH = 1,000,000,000,000,000,000 wei (10^18)
    conv_rate =  1.0e+18
    token_transactions_df['value_eth'] = token_transactions_df['value'] / conv_rate
    token_transactions_df['gas_price_eth'] = token_transactions_df['gas_price'] / conv_rate
    token_transactions_df['receipt_gas_used_eth'] = token_transactions_df['receipt_gas_used'] / conv_rate
    
    
    # Convert timestamps to datetime format
    token_transactions_df['block_timestamp_true'] =  pd.to_datetime(token_transactions_df['block_timestamp'])
    
    
    # Drop useless columns
    token_transactions_df.drop(columns=['value', 
                                        'gas_price', 
                                        'receipt_gas_used', 
                                        'block_number',
                                        'block_timestamp',
                                        'from_address', 
                                        'to_address'],
                               axis=1, inplace=True)
    
    
    
    
    
    return token_transactions_df