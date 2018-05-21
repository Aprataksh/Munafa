from pyalgotrade import strategy
from pyalgotrade.barfeed import csvfeed

import csv
from pyalgotrade import strategy
from pyalgotrade.technical import cross
from pyalgotrade.technical import ma


class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__position = None
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, smaPeriod)

    def getSMA(self):
        return self.__sma

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0:
                cash = self.getBroker().getCash() * 0.9
                priceOfStock = bars[self.__instrument].getPrice()
                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma) > 0:
            self.__position.exitMarket()

def get_ticker_list():
    with open(r"C:\Users\Rohit\Python_source_code\nse 500 stock data\nifty500_list.csv", 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line:
                ticker_list.append(line[2])
        # print(ticker_list)


from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.stratanalyzer import sharpe

ticker_list = []
def main(plot):
    get_ticker_list()
    smaPeriod = 163
    for instrument in ticker_list[:10]:
        # Download the bars
        feed = csvfeed.GenericBarFeed(frequency=300)
        feed.addBarsFromCSV(instrument, r"C:/Users/Rohit/Python_source_code/nse 500 stock data/Date Time Data/" + instrument + ".csv")

        strat = SMACrossOver(feed, instrument, smaPeriod)
        sharpeRatioAnalyzer = sharpe.SharpeRatio()
        strat.attachAnalyzer(sharpeRatioAnalyzer)

        if plot:
            plt = plotter.StrategyPlotter(strat, True, False, True)
            plt.getInstrumentSubplot(instrument).addDataSeries("sma", strat.getSMA())

        strat.run()
        print(instrument)
        print("Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05))

        if plot:
            plt.plot()

if __name__ == "__main__":
    main(True)