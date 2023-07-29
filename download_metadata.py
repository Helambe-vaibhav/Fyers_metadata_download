import datetime as dt
import datetime
import pandas as pd
import os
import warnings
import requests
warnings.filterwarnings("ignore")

# for downloading options metadata

def next_week():
    # for getting coming thursday date
    coming_thursday = dt.date.today() + dt.timedelta(days=(3- dt.date.today().weekday()+7)%7)
    cur_path =f'datafiles/{coming_thursday}'
    if not os.path.exists(cur_path):
        os.mkdir(cur_path)
        fyers_fo = "https://public.fyers.in/sym_details/NSE_FO.csv"
        df_symbols = pd.read_csv(fyers_fo, index_col=False, header=None)
        # print(df_symbols.head())
        df_symbols.drop([5,14,17],axis=1,inplace=True)
        # print(df_symbols.columns)
        df_symbols.columns=['Fytoken', 'Symbol Details', 'Exchange Instrument type', 'Minimum lot size', 'Tick size', 'ISIN', 'Last update date', 'Expiry date', 'Symbol ticker', 'Exchange', 'Segment', 'Scrip code', 'Underlying scrip code', 'Strike price', 'Option type']
        df_symbols = df_symbols[df_symbols['Underlying scrip code'] =='NIFTY' ]
        df_symbols.reset_index(drop=True, inplace=True)
        df_symbols['Expiry date'] = pd.to_datetime(df_symbols['Expiry date'],unit='s').dt.date
        exps = sorted(df_symbols['Expiry date'].unique())
        expiry = exps[1]
        print(f"{dt.datetime.now()} Expiry: {expiry} ")
        df_symbols = df_symbols[df_symbols['Expiry date']==expiry]
        # lot_size = df_symbols.loc[0,'Minimum lot size']
        df_symbols = df_symbols.sort_values(by=['Strike price'])
        df_symbols.reset_index(drop=True, inplace=True)
        df_symbols.set_index('Fytoken',inplace=True)
        with open(f'datafiles/{coming_thursday}/ExpirySymbols{coming_thursday}.csv','w') as f:
            df_symbols.to_csv(f)
        trades = pd.DataFrame(columns = ['Trade_NO','TradeType','ShortSymbol','ShortSellPrice','ShortBuyAlmaDiff','LongSymbol','LongBuyTime','LongBuyPrice','LongSellTime','LongSellPrice','ShortBuyPrice','LongProfit','ShortProfit','TotalProfit'])
        # trades = pd.DataFrame(columns=['Trade_NO','TradeType','StrikeOP', 'EntryTime', 'Buy','BuyAlma','CoverStrikeOP' ,'CoverSell','CoverSellAlma','ExitTime', 'Sell','SellAlma','CoverBuy','CoverBuyAlma','Highest','Lowest','Profit','CoverProfit','Total_Profit'])
        trades.to_csv(cur_path+f'/trades{coming_thursday}.csv',index= False)
next_week()


def get_symbol(strike, option_type = 'CE'):
    now = dt.datetime.now()
    if dt.date.today().weekday() == 3 and now.time() >= datetime.time(15, 27, 1):
        coming_thursday = dt.date.today() + dt.timedelta(days=(3- dt.date.today().weekday()+7)%7+7)
    else:
        coming_thursday = dt.date.today() + dt.timedelta(days=(3- dt.date.today().weekday()+7)%7)
    df_symbols = pd.read_csv(f'datafiles/{coming_thursday}/ExpirySymbols{coming_thursday}.csv')
    symbol = df_symbols.loc[(df_symbols['Strike price']==strike) & (df_symbols['Option type']== option_type),'Symbol ticker'].values[0]
    return symbol
