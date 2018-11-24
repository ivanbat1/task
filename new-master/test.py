# -*- coding: utf-8 -*-

from ctypes import POINTER, WINFUNCTYPE, c_void_p, c_int, c_ulong, c_char_p
from ctypes.wintypes import BOOL, DWORD, LPCWSTR, UINT
from urllib2 import urlopen
import json
import urllib2
from pythonicMT5 import zmq_python
import pythonicMT4
import time


EXMO_FEE = 0.002
STOCK_FEE = 0.001
PROFIT_PIPS = -0.000005
order = ''
trade = pythonicMT4.zmq_python()

# DECLARE_HANDLE(name) typedef void *name;
HCONV = c_void_p  # = DECLARE_HANDLE(HCONV)
HDDEDATA = c_void_p  # = DECLARE_HANDLE(HDDEDATA)
HSZ = c_void_p  # = DECLARE_HANDLE(HSZ)
LPBYTE = c_char_p  # POINTER(BYTE)
LPDWORD = POINTER(DWORD)
LPSTR = c_char_p
ULONG_PTR = c_ulong
QUOTER = 0

# Описание структуры CONVCONTEXT см. в windows/ddeml.h
PCONVCONTEXT = c_void_p

DMLERR_NO_ERROR = 0

# Predefined Clipboard Formats
CF_TEXT = 1
CF_BITMAP = 2
CF_METAFILEPICT = 3
CF_SYLK = 4
CF_DIF = 5
CF_TIFF = 6
CF_OEMTEXT = 7
CF_DIB = 8
CF_PALETTE = 9
CF_PENDATA = 10
CF_RIFF = 11
CF_WAVE = 12
CF_UNICODETEXT = 13
CF_ENHMETAFILE = 14
CF_HDROP = 15
CF_LOCALE = 16
CF_DIBV5 = 17
CF_MAX = 18

DDE_FACK = 0x8000
DDE_FBUSY = 0x4000
DDE_FDEFERUPD = 0x4000
DDE_FACKREQ = 0x8000
DDE_FRELEASE = 0x2000
DDE_FREQUESTED = 0x1000
DDE_FAPPSTATUS = 0x00FF
DDE_FNOTPROCESSED = 0x0000

DDE_FACKRESERVED = (~(DDE_FACK | DDE_FBUSY | DDE_FAPPSTATUS))
DDE_FADVRESERVED = (~(DDE_FACKREQ | DDE_FDEFERUPD))
DDE_FDATRESERVED = (~(DDE_FACKREQ | DDE_FRELEASE | DDE_FREQUESTED))
DDE_FPOKRESERVED = (~(DDE_FRELEASE))

XTYPF_NOBLOCK = 0x0002
XTYPF_NODATA = 0x0004
XTYPF_ACKREQ = 0x0008

XCLASS_MASK = 0xFC00
XCLASS_BOOL = 0x1000
XCLASS_DATA = 0x2000
XCLASS_FLAGS = 0x4000
XCLASS_NOTIFICATION = 0x8000

XTYP_ERROR = (0x0000 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK)
XTYP_ADVDATA = (0x0010 | XCLASS_FLAGS)
XTYP_ADVREQ = (0x0020 | XCLASS_DATA | XTYPF_NOBLOCK)
XTYP_ADVSTART = (0x0030 | XCLASS_BOOL)
XTYP_ADVSTOP = (0x0040 | XCLASS_NOTIFICATION)
XTYP_EXECUTE = (0x0050 | XCLASS_FLAGS)
XTYP_CONNECT = (0x0060 | XCLASS_BOOL | XTYPF_NOBLOCK)
XTYP_CONNECT_CONFIRM = (0x0070 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK)
XTYP_XACT_COMPLETE = (0x0080 | XCLASS_NOTIFICATION)
XTYP_POKE = (0x0090 | XCLASS_FLAGS)
XTYP_REGISTER = (0x00A0 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK)
XTYP_REQUEST = (0x00B0 | XCLASS_DATA)
XTYP_DISCONNECT = (0x00C0 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK)
XTYP_UNREGISTER = (0x00D0 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK)
XTYP_WILDCONNECT = (0x00E0 | XCLASS_DATA | XTYPF_NOBLOCK)
XTYP_MONITOR = (0x00F0 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK)

XTYP_MASK = 0x00F0
XTYP_SHIFT = 4

TIMEOUT_ASYNC = 0xFFFFFFFF

json_quotes = {}
count_sb = 0
count_bs = 0
metatrader5 = zmq_python().get_data('')



def val(valute_in):
    global valute
    valute = valute_in


def ex(pusto):
    for x in pusto:
        x[u'symbol'] = x[u'symbol'].replace('#Ripple', 'XRPUSDT')
        x[u'symbol'] = x[u'symbol'].replace('#Litecoin', 'LTCUSDT')
        x[u'symbol'] = x[u'symbol'].replace('#Bitcoin', 'BTCUSDT')
        x[u'symbol'] = x[u'symbol'].replace('BCHUSD', 'BCHUSDT')

    return (pusto)

def whileloop():
    url = "https://quotes.instaforex.com/api/quotesTick?m=json"
    response = urlopen(url)
    price2 = json.loads(response.read())
    price2 = ex(price2)
    global g
    g = price2
    return price2


def get_winfunc(libname, funcname, restype=None, argtypes=(), _libcache={}):
    """Retrieve a function from a library, and set the data types."""
    from ctypes import windll

    if libname not in _libcache:
        _libcache[libname] = windll.LoadLibrary(libname)
    func = getattr(_libcache[libname], funcname)
    func.argtypes = argtypes
    func.restype = restype

    return func


DDECALLBACK = WINFUNCTYPE(HDDEDATA, UINT, UINT, HCONV, HSZ, HSZ, HDDEDATA,
                          ULONG_PTR, ULONG_PTR)


class DDE(object):
    """Object containing all the DDE functions"""
    AccessData = get_winfunc("user32", "DdeAccessData", LPBYTE, (HDDEDATA, LPDWORD))
    ClientTransaction = get_winfunc("user32", "DdeClientTransaction", HDDEDATA,
                                    (LPBYTE, DWORD, HCONV, HSZ, UINT, UINT, DWORD, LPDWORD))
    Connect = get_winfunc("user32", "DdeConnect", HCONV, (DWORD, HSZ, HSZ, PCONVCONTEXT))
    CreateStringHandle = get_winfunc("user32", "DdeCreateStringHandleW", HSZ, (DWORD, LPCWSTR, UINT))
    Disconnect = get_winfunc("user32", "DdeDisconnect", BOOL, (HCONV,))
    GetLastError = get_winfunc("user32", "DdeGetLastError", UINT, (DWORD,))
    Initialize = get_winfunc("user32", "DdeInitializeW", UINT, (LPDWORD, DDECALLBACK, DWORD, DWORD))
    FreeDataHandle = get_winfunc("user32", "DdeFreeDataHandle", BOOL, (HDDEDATA,))
    FreeStringHandle = get_winfunc("user32", "DdeFreeStringHandle", BOOL, (DWORD, HSZ))
    QueryString = get_winfunc("user32", "DdeQueryStringA", DWORD, (DWORD, HSZ, LPSTR, DWORD, c_int))
    UnaccessData = get_winfunc("user32", "DdeUnaccessData", BOOL, (HDDEDATA,))
    Uninitialize = get_winfunc("user32", "DdeUninitialize", BOOL, (DWORD,))


class DDEError(RuntimeError):
    """Exception raise when a DDE error occurs."""

    def __init__(self, msg, idInst=None):
        if idInst is None:
            RuntimeError.__init__(self, msg)
        else:
            RuntimeError.__init__(self, "%s (err=%s)" % (msg, hex(DDE.GetLastError(idInst))))


class DDEClient(object):
    """The DDEClient class.

   Use this class to create and manage a connection to a service/topic.  To get
   classbacks subclass DDEClient and overwrite callback."""

    def __init__(self, service, topic):
        """Create a connection to a service/topic."""
        from ctypes import byref

        self._idInst = DWORD(0)
        self._hConv = HCONV()

        self._callback = DDECALLBACK(self._callback)
        res = DDE.Initialize(byref(self._idInst), self._callback, 0x00000010, 0)
        if res != DMLERR_NO_ERROR:
            raise DDEError("Unable to register with DDEML (err=%s)" % hex(res))

        hszService = DDE.CreateStringHandle(self._idInst, service, 1200)
        hszTopic = DDE.CreateStringHandle(self._idInst, topic, 1200)
        self._hConv = DDE.Connect(self._idInst, hszService, hszTopic, PCONVCONTEXT())
        DDE.FreeStringHandle(self._idInst, hszTopic)
        DDE.FreeStringHandle(self._idInst, hszService)
        if not self._hConv:
            raise DDEError("Unable to establish a conversation with server", self._idInst)

    def __del__(self):
        """Cleanup any active connections."""
        if self._hConv:
            DDE.Disconnect(self._hConv)
        if self._idInst:
            DDE.Uninitialize(self._idInst)

    def advise(self, item, stop=False):
        """Request updates when DDE data changes."""

        hszItem = DDE.CreateStringHandle(self._idInst, item, 1200)
        hDdeData = DDE.ClientTransaction(LPBYTE(), 0, self._hConv, hszItem, CF_TEXT,
                                         XTYP_ADVSTOP if stop else XTYP_ADVSTART, TIMEOUT_ASYNC, LPDWORD())
        DDE.FreeStringHandle(self._idInst, hszItem)
        if not hDdeData:
            raise DDEError("Unable to %s advise" % ("stop" if stop else "start"), self._idInst)
        DDE.FreeDataHandle(hDdeData)

    def execute(self, command, timeout=5000):
        """Execute a DDE command."""
        pData = c_char_p(command)
        cbData = DWORD(len(command) + 1)
        hDdeData = DDE.ClientTransaction(pData, cbData, self._hConv, HSZ(), CF_TEXT, XTYP_EXECUTE, timeout, LPDWORD())
        if not hDdeData:
            raise DDEError("Unable to send command", self._idInst)
        DDE.FreeDataHandle(hDdeData)

    def request(self, item, timeout=5000):
        """Request data from DDE service."""
        from ctypes import byref

        hszItem = DDE.CreateStringHandle(self._idInst, item, 1200)
        hDdeData = DDE.ClientTransaction(LPBYTE(), 0, self._hConv, hszItem, CF_TEXT, XTYP_REQUEST, timeout, LPDWORD())
        DDE.FreeStringHandle(self._idInst, hszItem)
        if not hDdeData:
            raise DDEError("Unable to request item", self._idInst)

        if timeout != TIMEOUT_ASYNC:
            pdwSize = DWORD(0)
            pData = DDE.AccessData(hDdeData, byref(pdwSize))
        if not pData:
            DDE.FreeDataHandle(hDdeData)
            raise DDEError("Unable to access data", self._idInst)
            # TODO: use pdwSize
            DDE.UnaccessData(hDdeData)
        else:
            pData = None
            DDE.FreeDataHandle(hDdeData)
        return pData

    def callback(self, value, item=None):
        """Calback function for advice."""
        # print '(mt4)', item, value
        # print '(mt5)', metatrader5
        for i in range(len(metatrader5)):
        #     # y['symbol'] - api instaforex просто удалите если ненужно
        #     # если нужно что-то заменть в мт4 или мт5 какието котировки покажу пример ка это делать,
        #     # потому что у меня нет наглядного примера какие котировки могт быть и так -
        #     # item - то котировки мт4, metatrader5[i][0] - это мт5 и просто
        #     # добавляете ".replace('#Litecoin', 'LTCUSDT')"
        #     # первое значение это то что нужно заменить второе на что нужно
        #     # заменить, думаю понятно (я показал на примере мт5)
        #     # часть кода отвечающая за поиск валютной пары, если нашли нужную простокоментируйте
        #     # ету часть и разкоментируйте ту которая отвечает за покупку
            if item == metatrader5[i][0]:

        #         # получение sb1 bs2 если не нужно так же коментируем м в условие иф удаляем эти значения
        #         # sb1 = float(y['bid']) - float(value.split(' ')[-2])  # api bid - dde ask
        #         # bs1 = float(value.split(' ')[-1]) - float(y['ask'])  # dde bid - api ask
                sb2 = float(value.split(' ')[-1]) - float(metatrader5[i][1]) # dde bid - dde mt5 ask
                bs2 = float(metatrader5[i][2]) - float(value.split(' ')[-2])  # dde mt5 bid - dde ask
        #         # здесь эсли нужно что-то убарть просто удалите условие в скобках которое ненужно
        #         #  (sb1 >= PROFIT_PIPS or bs1 >= PROFIT_PIPS) or
                global json_quotes, count_sb, count_bs
                if sb2 >= PROFIT_PIPS or bs2 >= PROFIT_PIPS:
                    if sb2:
                        count_sb += 1
                        json_quotes = {metatrader5[i][0]:'bs2 = {}, sb2 = {}'.format(count_bs, count_sb)}
                    elif bs2:
                        count_bs += 1
                        json_quotes = {metatrader5[i][0]:'bs2 = {}, sb2 = {}'.format(count_bs, count_sb)}
                    print json_quotes
                    # print 'sb2=', sb2, 'sb2=', bs2
                    # print item, '(MT4)', (value.split(' ')[-1]), value.split(' ')[-2]
                    # print item, '(MT5)', metatrader5[i][2], metatrader5[i][1]
                    # print "====="

            # если вы нашли свою пару пропишите ее вмосто "EURUSD"
            # y['symbol'] - api instaforex просто удалите если ненужно
            # часть кода отвечающая за покупку\продажу найденой валютной пары валютной пары,
            # if "EURUSD" == item == metatrader5[i][0]:
            #     sb1 = float(y['bid']) - float(value.split(' ')[-2])  # api bid - dde ask
            #     bs1 = float(value.split(' ')[-1]) - float(y['ask'])  # dde bid - api ask
            #
            #     sb2 = float(value.split(' ')[-1]) - float(metatrader5[i][1])  # dde bid - dde mt5 ask
            #     bs2 = float(metatrader5[i][2]) - float(value.split(' ')[-2])  # dde mt5 bid - dde ask
            #     global order
            #         #               здесь эсли нужно что-то убарть просто удалите условие в скобке которое ненужно
            #     if order != 'Buy' and order != 'Sell' and (sb1 >= PROFIT_PIPS or sb2 >= PROFIT_PIPS):
            #         print 'Buy'
            #         order = 'Buy'
            #         # тут можете установить stop_loss и take_profit самостоятельно,
            #         # он будет для всех одинаковый, так что выставляете в процентах
            #         trade.buy_order(symbol=item, stop_loss=0, take_profit=0)
            #         #   здесь эсли нужно что-то убарть просто удалите условие в скобке которое ненужно
            #     elif order != 'Buy' and order != 'Sell' and (bs1 >= PROFIT_PIPS or bs2 >= PROFIT_PIPS):
            #         print 'Sell'
            #         order = 'Sell'
            #         # тут можете установить stop_loss и take_profit самостоятельно,
            #         # он будет для всех одинаковый, так что выставляете в процентах
            #         trade.sell_order(symbol=item, stop_loss=0, take_profit=0)
            #
            #     elif order == 'Buy':
            #         order = ''
            #         print 'closeBuy'
            #         # время в секундах, через которое будет закрываться ордер
            #         time.sleep(60)
            #         trade.close_buy_order()
            #
            #     elif order == 'Sell':
            #         order = ''
            #         print 'closeSell'
            #         # время в секундах, через которое будет закрываться ордер
            #         time.sleep(60)
            #         trade.close_sell_order()

    def _callback(self, wType, uFmt, hConv, hsz1, hsz2, hDdeData, dwData1, dwData2):
        # if wType == XTYP_ADVDATA:
        from ctypes import byref, create_string_buffer

        dwSize = DWORD(0)
        pData = DDE.AccessData(hDdeData, byref(dwSize))
        if pData:
            item = create_string_buffer('\000' * 128)
            DDE.QueryString(self._idInst, hsz2, item, 128, 1004)
            self.callback(pData, item.value)
            DDE.UnaccessData(hDdeData)
        return DDE_FACK
        return 0


def WinMSGLoop():
    """Run the main windows message loop."""
    from ctypes import POINTER, byref, c_ulong
    from ctypes.wintypes import BOOL, HWND, MSG, UINT
    LPMSG = POINTER(MSG)
    LRESULT = c_ulong
    GetMessage = get_winfunc("user32", "GetMessageW", BOOL, (LPMSG, HWND, UINT, UINT))
    TranslateMessage = get_winfunc("user32", "TranslateMessage", BOOL, (LPMSG,))
    # restype = LRESULT
    DispatchMessage = get_winfunc("user32", "DispatchMessageW", LRESULT, (LPMSG,))
    msg = MSG()
    lpmsg = byref(msg)
    # global metatrader5
    while GetMessage(lpmsg, HWND(), 0, 0) > 0:
        TranslateMessage(lpmsg)
        DispatchMessage(lpmsg)
        # metatrader5 = zmq_python().get_data('')


if __name__ == "__main__":
    dde = DDEClient("MT4", "quote")  # Создали экземпляр клиента DDE.
    with open('quotes', 'r+') as f:
        for i in f.readlines():
            dde.advise(i.replace('\n', ''))
    WinMSGLoop()  # Запустили цикл обработки сообщений.
