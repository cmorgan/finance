"""
Data from Yahoo Finance
Author: Chris Morgan
"""


from datetime import datetime, date
import urllib2
import logging

import pandas


class YahooData(object):
    def __init__(self, symbols, start_date=(1900, 1, 1),
                 end_date=date.today().timetuple()[0:3], adjust=True):
        """
        :param symbols: list of symbols
        :param start_date: start date (y, m, d)
        :param end_date: end date (y, m, d)
        :param adjust: adjust all data against adjusted close
        """

        self.start_date = date(*start_date)
        self.end_date = date(*end_date)
        self.adjust = adjust
        self.data_frames = {}
        self.symbols = symbols if isinstance(symbols, list) else [symbols]

    def download(self):
        for s in self.symbols:
            url = historical_price_url(s, self.start_date, self.end_date)
            df = get_historical_prices(url)

            if self.adjust:
                df = adjust(df, remove_original=True)

            self.data_frames[s] = df

    def head(self):
        return self.panel.head()

    @property
    def close(self):
        return self.get_slice('close')

    def get_slice(self, column):
        '''
        :returns: slice of WidePanel for a given column
        '''
        return self.panel.minor_xs(column)

    @property
    def downloaded_symbols(self):
        return self.panel.items.tolist()

    def __repr__(self):
        return str(self.panel)


def historical_price_url(symbol, start_date, end_date):
    """
    :param symbol: Yahoo finanance symbol
    :param start_date: start date (y, m, d)
    :param end_date: end date (y, m, d)
    :returns: URL for accessing Yahoo historical prices
    """

    return ('http://ichart.finance.yahoo.com/table.csv'
            '?s={0}&a={1}&b={2}&c={3}&d={4}&e={5}&f={6}'.format(
                symbol.upper(), start_date.month - 1, start_date.day,
                start_date.year, end_date.month - 1, end_date.day,
                end_date.year))


def get_historical_prices(yahoo_url):
    """
    :param yahoo_url: historical_price_url()
    :returns: DataFrame of historical prices
    """

    try:
        lines = urllib2.urlopen(yahoo_url).readlines()
    except Exception, e:
        s = "Failed to download:\n{0}".format(e)
        print s

    dates = []
    data = [[] for i in range(6)]

    # header : Date, Open, High, Low, Close, Volume, Adj Close
    for line in lines[1:]:
        fields = line.rstrip().split(',')
        dates.append(datetime.strptime(fields[0], '%Y-%m-%d'))
        for i, field in enumerate(fields[1:]):
            data[i].append(float(field))

    idx = pandas.Index(dates)
    data = dict(zip(['open', 'high', 'low', 'close', 'volume', 'adj_close'],
                    data))

    df = pandas.DataFrame(data, index=idx).sort()
    logging.debug('Got %i days of data' % len(df))
    return df


def adjust(dataframe, remove_original=False):
    '''
    :param dataframe: pandas.DataFrame containing prices
    :param remove_original: Boolean, replace original prices with adjusted
    :returns: pandas.DataFrame containing adjusted prices against adj_close
    '''

    c = dataframe['close'] / dataframe['adj_close']

    dataframe['adj_open'] = dataframe['open'] / c
    dataframe['adj_high'] = dataframe['high'] / c
    dataframe['adj_low'] = dataframe['low'] / c

    if remove_original:
        dataframe = dataframe.drop(['open', 'close', 'high', 'low'], axis=1)
        renames = dict(zip(['adj_open', 'adj_close', 'adj_high', 'adj_low'],
                           ['open', 'close', 'high', 'low']))
        dataframe = dataframe.rename(columns=renames)

    return dataframe