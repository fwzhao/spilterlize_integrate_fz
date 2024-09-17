#!/bin/env python

#### split data by annotation ####

#### libraries
import os
import pandas as pd

#### configurations

# input
data_path = snakemake.input["data"]
support_path = snakemake.input["support_path"]
annotation_path = snakemake.input["annotation"]

# parameters
result_path = snakemake.params["result_path"]
split_by = snakemake.params["split_by"]


# load data
data = pd.read_csv(data_path, index_col=0)
support = pd.read_csv(support_path, index_col=0)
annotation = pd.read_csv(annotation_path, index_col=0)

# split and save count and annotation data
for split_var in split_by:
    if split_var == "all":
        data.loc[:, annotation.index].to_csv(os.path.join(result_path,"all","counts.csv"))
        data.loc[:, annotation.index].to_csv(os.path.join(result_path,"all","support.csv"))
        annotation.to_csv(os.path.join(result_path,"all","annotation.csv"))
    
    if split_var in annotation.columns:
        for split in annotation[split_var].unique():
            
            # split & save counts
            data.loc[:, annotation[(annotation[split_var]==split)].index].to_csv(os.path.join(result_path,f"{split_var}_{split}","counts.csv"))

            # split & save counts
            support.loc[:, annotation[(annotation[split_var]==split)].index].to_csv(os.path.join(result_path,f"{split_var}_{split}","support.csv"))
    
            # split & save annotations
            annotation.loc[annotation[split_var]==split, :].to_csv(os.path.join(result_path,f"{split_var}_{split}","annotation.csv"))