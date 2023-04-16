'''def aroon(Close, n=14):
    df = pd.DataFrame(Close)
    df['up'] = 100 * df['Close'].rolling(window=n + 1, center=False).apply(lambda x: x.argmax()) / n
    df['down'] = 100 * df['Close'].rolling(window=n + 1, center=False).apply(lambda x: x.argmin()) / n
    return (pd.Series(df['up']), pd.Series(df['down']))'''


