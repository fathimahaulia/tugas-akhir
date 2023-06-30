def read_data(stock_code, start_date, end_date, roll=0):
    df = yfinance.download(stock_code, start=start_date, end=end_date)

    # change date to a column
    df = df.reset_index()
    df['DateTemp'] = df['Date'].dt.strftime('%Y-%m-%d')
    df = df.drop(columns=['Adj Close', 'Date'])
    df.rename(columns = {'DateTemp':'Date'}, inplace = True)
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'].replace(to_replace=0, value=1/1000, inplace=True)

    if roll!=0:
        df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].rolling(roll).mean()
    else:
        df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']]

    df.dropna(how='any', axis=0, inplace=True)

    return df

def preprocessing_test(df, min_return, max_return, min_volume, max_volume):
    '''Calculate percentage change'''
    df['Open'] = df['Open'].pct_change()
    df['High'] = df['High'].pct_change()
    df['Low'] = df['Low'].pct_change()
    df['Close'] = df['Close'].pct_change()
    df['Volume'] = df['Volume'].pct_change()

    # Drop all rows with NaN values
    df.dropna(how='any', axis=0, inplace=True)

    # Normalize price columns
    df['Open'] = (df['Open'] - min_return) / (max_return - min_return)
    df['High'] = (df['High'] - min_return) / (max_return - min_return)
    df['Low'] = (df['Low'] - min_return) / (max_return - min_return)
    df['Close'] = (df['Close'] - min_return) / (max_return - min_return)
    # Normalize volume column
    df['Volume'] = (df['Volume'] - min_volume) / (max_volume - min_volume)

    # Remove date column
    df.drop(columns=['Date'], inplace=True)

    return df

def reverse_close_price(price_actual, seq_len, pct_pred, max, min):
    price_pred = []
    price_actual = np.array(price_actual)
    price_pred.append(price_actual[seq_len])
    for i in range(len(pct_pred)):
        pct_pred[i] = pct_pred[i]*(max - min) + min
        price_pred.append(price_actual[i+seq_len]*(pct_pred[i]+1))
    return price_pred

def viz_close_vol(df, stock_name):
    fig = plt.figure(figsize=(15,10))
    st = fig.suptitle(f"{stock_name} Close Price and Volume", fontsize=20)
    st.set_y(0.92)

    # Close Prices
    ax1 = fig.add_subplot(211)
    ax1.plot(df['Close'], label=f'{stock_name} Close Price')
    ax1.set_xticks(range(0, df.shape[0], 1464))
    ax1.set_xticklabels(df['Date'].loc[::1464])
    ax1.set_ylabel('Close Price', fontsize=18)
    ax1.legend(loc="upper left", fontsize=12)

    # Volume Prices
    ax2 = fig.add_subplot(212)
    ax2.plot(df['Volume'], label=f'{stock_name} Volume')
    ax2.set_xticks(range(0, df.shape[0], 1464))
    ax2.set_xticklabels(df['Date'].loc[::1464])
    ax2.set_ylabel('Volume', fontsize=18)
    ax2.legend(loc="upper left", fontsize=12)
