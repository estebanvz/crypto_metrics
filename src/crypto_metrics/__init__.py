#%%
import os
import logging
import numpy as np
import pandas as pd
import pandas_ta as ta

class CryptoDataTransformation:
    def __init__(self, save_path="./datasets/1h", criptos=["BTCUSDT"]) -> None:
        self.save_path = save_path
        self.criptos = criptos
        if(os.path.isdir(self.save_path) is False):
            logging.warning("The file {} do not exist!".format(save_path))
    def readDataset(self, lr_len=20,adx_len=14,emas_len=[55,21,10]):
        for cripto in self.criptos:
            path = "{}/{}.csv".format(self.save_path,cripto)
            if not os.path.isfile():
                print(f"{cripto}: is empty")
                return
            bars = np.loadtxt(path, delimiter="|")
            newBars = []
            for line in bars:
                newBars.append(line[:6])
            btc_df = pd.DataFrame(
                newBars, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
            btc_df["Index"] = pd.to_datetime(btc_df['Date'].astype(
                int), unit='ms').dt.tz_localize('UTC').dt.tz_convert('America/Santarem')
            btc_df.set_index('Index', inplace=True)
            btc_df.astype(float)
            btc_df["lr"] = linearRegression(btc_df, lr_len)
            btc_df = adx(btc_df, adx_len=adx_len)
            btc_df = emas(btc_df,emas=emas_len)
            btc_df= btc_df.dropna()
            btc_df.to_csv(path,sep="|",header=True)
#%%

def linearRegression(data, lengthKC=20):
    source = data['Close']
    tmp = ta.sma(source, period=lengthKC)
    # tmpmin = ta.min(data['Low'], period=lengthKC)
    tmpmin = data['Low'].rolling(window = lengthKC).min()
    tmpmax = data['Low'].rolling(window = lengthKC).max()
    # tmpmax = ta.max(data['High'], period=lengthKC)
    aux = source - (((tmpmax + tmpmin)/2 + tmp)/2)
    val = ta.linreg(aux, length=lengthKC,slope=True)
    return val

def adx(btc_df, num=23, adx_len =14, slope=False, dmi=True):
    tmp = ta.adx(
        btc_df["High"], btc_df["Low"], btc_df["Close"], period=adx_len)
    btc_df["adx"] = tmp[[f"ADX_{adx_len}"]]
    btc_df["mdm"] = tmp[[f"DMN_{adx_len}"]]
    btc_df["pdm"] = tmp[[f"DMP_{adx_len}"]]
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
        btc_df[str(ema)]= ta.ema(btc_df["Close"],period=ema)
    return btc_df
# %%
if __name__=="__main__":
    CDT = CryptoDataTransformation()
    transformer = CryptoDataTransformation()
    transformer.readDataset()   
# %%
