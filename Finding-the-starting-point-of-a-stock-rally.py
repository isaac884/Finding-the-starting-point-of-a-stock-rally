####################################################################################################################################################################################
# Requirement
####################################################################################################################################################################################

import yfinance as yf  # Import Yahoo Finance 獲取股票數據
import pandas as pd  # Import pandas 處理數據
import numpy as np  # Import numpy 數值計算
import matplotlib.pyplot as plt  # Import matplotlib 繪製圖表
import matplotlib.dates as mdates  # Import matplotlib.dates 處理日期格式

####################################################################################################################################################################################
# Part 1: Get stock data
####################################################################################################################################################################################

def get_data(sym, per):
    if not per or len(per) == 1 or per.isdigit() or per.isalpha():  
        print("Invalid period \"{}\". Please specify a valid period, must be one of ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']\nPlease run the program again.".format(per))  # 顯示錯誤信息
        exit()  # 結束程序
    data = yf.download(sym, period=per, interval="1d")  # 下載指定 period 的日線數據
    if data.empty:  # 如果數據為空
        print("No data found for {}. Please check the stock symbol and run the program again.".format(sym))  # 顯示錯誤信息
        exit()  

    return data  # 傳回數據


####################################################################################################################################################################################
# Part 2: Function to calculate MACD
####################################################################################################################################################################################

def calmacd(df):
    df["ema12"] = df["Close"].ewm(span=12, adjust=False).mean()  # 計算 12 日指數平均線
    df["ema26"] = df["Close"].ewm(span=26, adjust=False).mean()  # 計算 26 日指數平均線
    df["macd"] = df["ema12"] - df["ema26"]  # 計算 MACD 值
    df["signal"] = df["macd"].ewm(span=9, adjust=False).mean()  # 計算 Signal 線
    df["macdgtsignal"] = df["macd"] > df["signal"]  # 判斷 MACD 是否大於 Signal 線
    df["macdltsignal"] = df["macd"] < df["signal"]  # 判斷 MACD 是否小於 Signal 線
    return df  # 傳回更新後的 DataFrame

####################################################################################################################################################################################
# Part 3: Function to calculate RSI
####################################################################################################################################################################################

def calrsi(df, period=14):
    delta = df['Close'].diff()  # 計算每日收盤價

    # 計算漲幅和跌幅
    gain = delta.where(delta > 0, 0)  # 漲幅
    loss = -delta.where(delta < 0, 0)  # 跌幅

    # 計算平均漲幅和平均跌幅
    avg_gain = gain.rolling(window=period, min_periods=1).mean()  # 平均漲幅
    avg_loss = loss.rolling(window=period, min_periods=1).mean()  # 平均跌幅

    # 計算相對強度RSI
    rs = avg_gain / avg_loss  # 計算相對強度RSI

    # 計算 RSI
    rsi = 100 - (100 / (1 + rs))  # 根據相對強度計算 RSI

    df['rsi'] = rsi  # 將 RSI 新增到 DataFrame 中
    return df  # 傳回更新後的 DataFrame

####################################################################################################################################################################################
# Part 4: Function to determine whether a stock has a rising signal
####################################################################################################################################################################################

def Rising(df):
    df['Rise_Point'] = ((df['macd'] > df['signal']) &  # 當前 MACD 大於 Signal 線
                        (df['macd'].shift(1) <= df['signal'].shift(1)) &  # 前一天 MACD 小於等於 Signal 線
                        (df['rsi'] > df['rsi'].shift(1))).astype(int)  # RSI 增長
    return df  # 傳回更新後的 DataFrame

####################################################################################################################################################################################
# Part 5: Function for drawing charts
####################################################################################################################################################################################

def plot(data):
    plt.figure(figsize=(12, 8))  # 設定圖表大小
    
    plt.subplot(3, 1, 1)  # 設定sub圖位置
    
    # monthly收盤價圖表
    plt.plot(data.index, data["Close"], label="Monthly Close", color='black')  # 繪製收盤價

    # 標註rising point
    Rising = data[data['Rise_Point'] == 1]  # 選擇（Rise_Point == 1）
    plt.scatter(Rising.index, Rising["Close"], marker='^', color='green', s=60, label="Rising point")  # 標註rising point
    
   
    plt.ylabel("Price")  # set Y axis title 為"價格"
    plt.xlabel("Date")  # set X axis title 為 "日期"
    plt.title("{} Monthly close price with Rising point".format(sym))  # set title
    plt.xticks(rotation=20)
    plt.legend(loc='upper left',  prop={'size': 6})  # 設定圖例位置
    plt.grid()  # 顯示網格
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # 設定每個月顯示一次
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # 日期格式為 'YYYY-MM'
    plt.tight_layout()     # 調整佈局以避免圖表重疊

    # MACD 和 Signal 線圖表
    plt.subplot(3, 1, 2)  
    plt.plot(data.index, data["macd"], label="MACD", color='blue')  # 畫出 MACD
    plt.plot(data.index, data["signal"], label="Signal Line", color='red')  # 畫出 Signal 線
    plt.title("MACD and signal line")  
    plt.xlabel("Date")  
    plt.ylabel("Value") 
    plt.legend(loc='upper left',  prop={'size': 6}) 
    plt.xticks(rotation=20)  
    plt.grid()  
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  
    plt.tight_layout()  

    # RSI 圖表
    plt.subplot(3, 1, 3) 
    plt.plot(df.index, df['rsi'], label='RSI', color='blue')  # 畫出 RSI
    # RSI overbought and oversold 水平線
    plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')  # 設定 70 為Overbought水平
    plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')  # 設定 30 為Oversold水平
    plt.title("RSI (Relative Strength Index)")  
    plt.xlabel("Date")  
    plt.ylabel("Value")
    plt.legend(loc='upper left',  prop={'size': 5}) 
    plt.xticks(rotation=20)
    plt.grid() 
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  

    plt.tight_layout()  
    plt.show()  
####################################################################################################################################################################################
# Part 6: Function calculate Bollinger Bands
####################################################################################################################################################################################

def bollingerBands(data):
    # 計算20期移動平均線（SMA）
    data['SMA'] = data['Close'].rolling(window=20).mean()

    # 計算20期標準差（SD）
    data['SD'] = data['Close'].rolling(window=20).std()

    # 計算Bollinger Bands的上軌（UB）和下軌（LB）
    data['UB'] = data['SMA'] + 2 * data['SD']
    data['LB'] = data['SMA'] - 2 * data['SD']

  
    plt.figure(figsize=(12, 6)) 

    # 收盤價格（藍色曲線）
    plt.plot(data['Close'], label='Price', color='blue', linewidth=1)

    # 中軌線（橙色曲線，即SMA）
    plt.plot(data['SMA'], label='Middle Band (SMA)', color='orange', linewidth=1)

    # Bollinger Bands的上軌線（紅色虛線）
    plt.plot(data['UB'], label='Upper Band', color='red', linestyle='--', linewidth=1)

    # Bollinger Bands的下軌線（綠色虛線）
    plt.plot(data['LB'], label='Lower Band', color='green', linestyle='--', linewidth=1)

 
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))


    plt.legend(loc='upper left', prop={'size': 5})


    plt.xticks(rotation=20)

    # Bollinger Bands區域（上軌與下軌之間的灰色區域）
    plt.fill_between(data.index, data['UB'], data['LB'], color='gray', alpha=0.2, label='Bollinger Bands')

    plt.title('Stock Price with Bollinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid()
    plt.tight_layout()
    plt.show()



####################################################################################################################################################################################
# Main function
####################################################################################################################################################################################

sym = input("Enter the stock symbol: ").upper()  # 輸入股票代號
per = input("Enter the period you want, must be one of ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'] \nPlease enter: ")
df = get_data(sym, per)  # 獲取股票數據

# 計算 MACD、RSI 和上漲信號
df = calmacd(df)  # 計算 MACD
df = calrsi(df)  # 計算 RSI
df = Rising(df)  # 計算上漲

# 繪製圖表
plot(df)

#計算Bollinger Bands
bollingerBands(df)
