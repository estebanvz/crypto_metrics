# %%
import logging
import etalib
import pandas as pd
import os
import numpy as np


class CryptoDataTransformation:
    def __init__(self, save_path="./datasets/1h", criptos=["BTCUSDT"]) -> None:
        self.save_path = save_path
        self.criptos = criptos
        if(os.path.isdir(self.save_path) is False):
            logging.warning("The file {} do not exist!".format(save_path))
    def readDataset(self, lr_len=20,adx_len=14,emas_len=[55,21,10]):
        for cripto in self.criptos:
            bars = np.loadtxt("{}/{}.csv".format(self.save_path,cripto), delimiter="|")
            newBars = []
            for line in bars:
                newBars.append(line[:6])
            btc_df = pd.DataFrame(
                newBars, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
            btc_df["Index"] = pd.to_datetime(btc_df['Date'].astype(
                int), unit='ms').dt.tz_localize('UTC').dt.tz_convert('America/Santarem')
            btc_df.set_index('Index', inplace=True)
            btc_df.astype(float)
            val = linearRegression(btc_df, lr_len)
            btc_df["lr"] = val.df
            btc_df = adx(btc_df, adx_len=adx_len)
            btc_df = emas(btc_df,emas=emas_len)
            path = "{}/{}.csv".format(self.save_path,cripto)
            btc_df= btc_df.dropna()
            btc_df.to_csv(path,sep="|",header=True)

def linearRegression(data, lengthKC=20):
    source = data['Close']
    tmp = etalib.sma(source, period=lengthKC)
    tmpmin = etalib.min(data['Low'], period=lengthKC)
    tmpmax = etalib.max(data['High'], period=lengthKC)
    val = etalib.linearreg(
        source - (((tmpmax + tmpmin)/2 + tmp)/2), period=lengthKC)
    return val


def adx(btc_df, num=23, adx_len =14, slope=False, dmi=True):
    btc_df["adx"] = etalib.adx(
        btc_df["High"], btc_df["Low"], btc_df["Close"], period=adx_len).df
    if(dmi):
        btc_df["mdm"] = etalib.minus_dm(
            btc_df["High"], btc_df["Low"], period=adx_len).df
        btc_df["pdm"] = etalib.plus_dm(
            btc_df["High"], btc_df["Low"], period=adx_len).df
    if(slope):
        tmp = []
        for e in btc_df["adx"]:
            if(e > num):
                tmp.append(1)
            else:
                tmp.append(0)
        btc_df["adx23"] = tmp
    return btc_df
def emas(btc_df, emas=[55,21,10]):
    for ema in emas:
        btc_df[str(ema)]= etalib.ema(btc_df["Close"],ema)