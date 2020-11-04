
import numpy as np

import csv
import pandas as pd

import matplotlib.pyplot as plt


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


df = pd.read_csv('unimodal.csv')

m, n = df.shape

complete = df[df["Epoch"] == 999]

survive = complete[['batch', 'Exp Num', 'svo_dist:d1:m', 'svo_dist:d1:s']]

survive.to_csv("survive_uni.csv")



df_bi = pd.read_csv('bimodal.csv')

complete_bi = df_bi[df_bi["Epoch"] == 999]

survive_bi = complete_bi[['batch', 'Exp Num', 'svo_dist:d1:m', 'svo_dist:d1:s','svo_dist:d2:m','svo_dist:d2:s']]

survive_bi.to_csv("survive_bi.csv")


df_tri1 = pd.read_csv('_1.csv')

complete_tri1 = df_tri1[df_tri1["Epoch"] == 999]

survive_tri1 = complete_tri1[['batch', 'Exp.Num', 'svo_dist.d1.m', 'svo_dist.d1.s','svo_dist.d2.m','svo_dist.d2.s','svo_dist.d3.m','svo_dist.d3.s']]

survive_tri1.to_csv("survive_tri1.csv")


df_tri2 = pd.read_csv('_2.csv')

complete_tri2 = df_tri2[df_tri2["Epoch"] == 999]

survive_tri2 = complete_tri2[['batch', 'Exp.Num', 'svo_dist.d1.m', 'svo_dist.d1.s','svo_dist.d2.m','svo_dist.d2.s','svo_dist.d3.m','svo_dist.d3.s']]

survive_tri2.to_csv("survive_tri2.csv")



df_tri3 = pd.read_csv('_3.csv')

complete_tri3 = df_tri3[df_tri3["Epoch"] == 999]

survive_tri3 = complete_tri3[['batch', 'Exp.Num', 'svo_dist.d1.m', 'svo_dist.d1.s','svo_dist.d2.m','svo_dist.d2.s','svo_dist.d3.m','svo_dist.d3.s']]

survive_tri3.to_csv("survive_tri3.csv")









