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


def get_time_intervals():
    # if today is thursday
    start_time = datetime.datetime.now().replace(hour=9, minute=15, second=1, microsecond=0)
    end_time = datetime.datetime.now().replace(hour=15, minute=33, second=1, microsecond=0)
    time_intervals = []
    while start_time < end_time:
        time_intervals.append(start_time)
        start_time += datetime.timedelta(minutes=3)
    return time_intervals
#











class Download_Metadata()
    def __init__(self,):
        self







































# class fyers():
#     def __init__(self):
#         self.client_id='S7DKTQZ5MH-100'
#         secret_key ='YZ487I7MYG'
#         redirect_uri = 'https://www.google.com/'
#         response_type = 'code'
#
#     def get_expiry(self):
#         coming_thursday = dt.date.today() + dt.timedelta(days=(3- dt.date.today().weekday()+7)%7)
#         if not os.path.exists(f'ExpirySymbols/ExpirySymbols{coming_thursday}.csv'):
#             fyers_fo = "https://public.fyers.in/sym_details/NSE_FO.csv"
#             df_symbols = pd.read_csv(fyers_fo, index_col=False, header=None)
#             df_symbols.drop([5,14],axis=1,inplace=True)
#             df_symbols.columns=['Fytoken', 'Symbol Details', 'Exchange Instrument type', 'Minimum lot size', 'Tick size', 'ISIN', 'Last update date', 'Expiry date', 'Symbol ticker', 'Exchange', 'Segment', 'Scrip code', 'Underlying scrip code', 'Strike price', 'Option type']
#             df_symbols = df_symbols[df_symbols['Underlying scrip code'] =='NIFTY' ]
#             df_symbols.reset_index(drop=True, inplace=True)
#             df_symbols['Expiry date'] = pd.to_datetime(df_symbols['Expiry date'],unit='s').dt.date
#             exps = sorted(df_symbols['Expiry date'].unique())
#             expiry = exps[0]
#             print(f"{dt.datetime.now()} Expiry: {expiry} ")
#             self.df_symbols = df_symbols[df_symbols['Expiry date']==expiry]
#             # lot_size = df_symbols.loc[0,'Minimum lot size']
#             self.df_symbols = self.df_symbols.sort_values(by=['Strike price'])
#             self.df_symbols.reset_index(drop=True, inplace=True)
#             self.df_symbols.set_index('Fytoken',inplace=True)
#             with open(f'ExpirySymbols/ExpirySymbols{expiry}.csv','w') as f:
#                 self.df_symbols.to_csv(f)
#         else:
#             self.df_symbols = pd.read_csv(f'ExpirySymbols/ExpirySymbols{coming_thursday}.csv')
#
#     def get_access_token(self):
#         secret_key ='YZ487I7MYG'
#         redirect_uri = 'https://www.google.com/'
#         response_type = 'code'
#
#         today_date = str(dt.datetime.now().date())
#         if not os.path.exists(f'accessToken/access_token{today_date}.txt'):
#             for file in os.listdir('accessToken'):
#                 os.remove(f'accessToken/{file}')
#             session= accessToken.SessionModel(client_id= self.client_id,secret_key=secret_key,redirect_uri=redirect_uri, response_type=response_type, grant_type='authorization_code')
#             response = session.generate_authcode()
#             print('Login Url:',response)
#             time.sleep(2)
#             auth_url = input('Enter the URL: ')
#             auth_code = auth_url.split('auth_code=')[1].split('&state')[0]
#             session.set_token(auth_code)
#             self.access_token = session.generate_token()['access_token']
#             with open(f'accessToken/access_token{today_date}.txt', 'w') as f:
#                 f.write(self.access_token)
#         else:
#             with open(f'accessToken/access_token{today_date}.txt', 'r') as f:
#                 self.access_token = f.read()
#
#     def get_symbol(self, strike, ce = True):
#         if ce:
#             self.symbol = self.df_symbols.loc[(self.df_symbols['Strike price']==strike) & (self.df_symbols['Option type']== 'CE'),'Symbol ticker'].values[0]
#         else:
#             self.symbol = self.df_symbols.loc[(self.df_symbols['Strike price']==strike) & (self.df_symbols['Option type']== 'PE'),'Symbol ticker'].values[0]
#
