# created: 8/17/2013
# author:  aliang

import urllib2
from urllib2 import URLError
from collections import namedtuple
import logging
import StringIO
import csv

from types import StringType, UnicodeType, DictType

# StaticClass
class GetStockSymbols(object):

    # CONSTANTS
    EXCHANGE_URI = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=%s&render=download"

    NYSE = "NYSE"
    NASDAQ = "NASDAQ"
    AMEX = "AMEX"

    ALL_EXCHANGES = (NYSE, NASDAQ, AMEX)

     # TODO 1 decide between using staticmethods or not. probably doesn't need to be static
     # TODO 2 maybe an option between using a list or generator. however, not like there is a HUGE number of ticker symbols to begin with
    @staticmethod
    def call_endpoint(exchange_name):
        '''
            @type exchange_name: StringType
            @rtype: ListType
        '''
        assert isinstance(exchange_name, StringType), type(exchange_name)

        try:
            resp = urllib2.urlopen(GetStockSymbols.EXCHANGE_URI % exchange_name).read()
        except URLError:
            GetStockSymbols.__LOGGER.debug("service unavailable... really?")

        output = StringIO.StringIO(resp)
        cr = csv.reader(output)
        SecuritySymbol = namedtuple('SecuritySymbol',
                                    [x.replace(' ', "_").lower() for x in cr.next() if x]
                                    )

        # might as well put an assert here because if there isn't a field for symbol anymore this is kind of pointless
        assert 'symbol' in SecuritySymbol._fields

        return [SecuritySymbol(*[x for x in row if x])
                    for row in cr
                    ]

    @staticmethod
    def get_all():
        '''
            Gets a list of symbols for each of the exchanges in GetStockSymbolsUpdater.ALL_EXCHANGES

            currently these are just NASDAQ, NYSE, and AMEX

            @rtype: TupleType
        '''
        return tuple(GetStockSymbols.call_endpoint(name) for name in GetStockSymbols.ALL_EXCHANGES)


    __LOGGER = logging.getLogger("__name__")
