from Stock import Stock
from pandas import DataFrame as dF


def highest_profit_rate():

    dframe = provide_data()
    dframe = dframe[dframe['date'].isin(['1', '2', '3'])]
    dframe['change'] = dframe['closing value'] - dframe['opening value']
    res = dframe.groupby(['name'])['change'].sum().sort_values(axis= 0, ascending= False).head(3)

    les_stock = []

    for index, _ in res.iteritems():
        les_stock.append(Stock(index))

    return les_stock


def provide_data():

    data = []

    data.append(['مدیریت', '1', 100, 200])
    data.append(['مدیریت', '2', 200, 150])
    data.append(['مدیریت', '3', 150, 300])

    data.append(['خساپا', '1', 500, 700])
    data.append(['خساپا', '2', 700, 700])
    data.append(['خساپا', '3', 700, 750])

    data.append(['شقز', '1', 150, 700])
    data.append(['شقز', '2', 700, 200])
    data.append(['شقز', '3', 200, 180])

    data.append(['چهارم', '1', 150, 151])
    data.append(['چهارم', '2', 151, 152])
    data.append(['چهارم', '3', 152, 153])

    dframe = dF(data, columns=['name', 'date', 'opening value', 'closing value'])

    return dframe

