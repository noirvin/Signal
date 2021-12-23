import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Predictor:
    def __init__(self,df):
        self.df=df
        self.resistances=np.array([])
        self.supports=np.array([])
    def pre_process(x,y):

        pass

    def train(x_train,y_train):

        pass


    def get_Support(self,i):
        support = self.df['Low'][i] < self.df['Low'][i-1]  and self.df['Low'][i] < self.df['Low'][i+1] and self.df['Low'][i+1] < self.df['Low'][i+2] and self.df['Low'][i-1] < self.df['Low'][i-2]
        return support
    def get_Resistance(self,i):
        resistance = self.df['High'][i] > self.df['High'][i-1]  and self.df['High'][i] > self.df['High'][i+1] and self.df['High'][i+1] > self.df['High'][i+2] and self.df['High'][i-1] > self.df['High'][i-2]
        return resistance
