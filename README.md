# TieredSampling
This is the source code for the paper "Tiered Sampling: An Efficient Method for Counting Sparse Motifs in Massive Graph Streams" published on IEEE Conference on Big Data 2017. Please cite the paper with the following bibtex:
@INPROCEEDINGS{terolli2017, 
author={L. {De Stefani} and E. {Terolli} and E. {Upfal}}, 
booktitle={2017 IEEE International Conference on Big Data (Big Data)}, 
title={Tiered sampling: An efficient method for approximate counting sparse motifs in massive graph streams}, 
year={2017},  
pages={776-786}, 
keywords={graph motif mining;reservoir sampling;stream computing}, 
doi={10.1109/BigData.2017.8257993}, 
ISSN={}, 
month={Dec},}

The source code for each algorithm in our paper is saved in a separate directory. To run an algorithm just enter in its corresponding directory and execute the following command in the terminal.

**python Main.py -g GraphFile -r FirstResevoirSize -t SecondReservoirSize -s RandomSeed**

where:
**GraphFile** is a path of a text file storing the graph as a list of undirected edges.
**FirstReservoirSize** is the capacity of the Edge Reservoir
**SecondReservoirSize** is the capacity of the Submotif Reservoir
