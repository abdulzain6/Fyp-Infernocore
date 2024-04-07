# -*- coding: mbcs -*-
typelib_path = 'C:\\Windows\\System32\\quartz.dll'
_lcid = 0 # change this if required
from ctypes import *
import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes import GUID
from ctypes import HRESULT
from comtypes import helpstring
from comtypes import COMMETHOD
from comtypes import dispid
from comtypes import BSTR
from comtypes.automation import IDispatch
from comtypes import IUnknown
LONG_PTR = c_longlong
from comtypes.automation import VARIANT
from comtypes import CoClass
from comtypes.automation import VARIANT


class IBasicAudio(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    'IBasicAudio interface'
    _iid_ = GUID('{56A868B3-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = ['dual', 'oleautomation']
IBasicAudio._methods_ = [
    COMMETHOD([dispid(1610743808), 'propput'], HRESULT, 'Volume',
              ( ['in'], c_int, 'plVolume' )),
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Volume',
              ( ['out', 'retval'], POINTER(c_int), 'plVolume' )),
    COMMETHOD([dispid(1610743810), 'propput'], HRESULT, 'Balance',
              ( ['in'], c_int, 'plBalance' )),
    COMMETHOD([dispid(1610743810), 'propget'], HRESULT, 'Balance',
              ( ['out', 'retval'], POINTER(c_int), 'plBalance' )),
]
################################################################
## code template for IBasicAudio implementation
##class IBasicAudio_Impl(object):
##    def _get(self):
##        '-no docstring-'
##        #return plVolume
##    def _set(self, plVolume):
##        '-no docstring-'
##    Volume = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return plBalance
##    def _set(self, plBalance):
##        '-no docstring-'
##    Balance = property(_get, _set, doc = _set.__doc__)
##

class IMediaControl(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    'IMediaControl interface'
    _iid_ = GUID('{56A868B1-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = ['dual', 'oleautomation']
IMediaControl._methods_ = [
    COMMETHOD([dispid(1610743808)], HRESULT, 'Run'),
    COMMETHOD([dispid(1610743809)], HRESULT, 'Pause'),
    COMMETHOD([dispid(1610743810)], HRESULT, 'Stop'),
    COMMETHOD([dispid(1610743811)], HRESULT, 'GetState',
              ( ['in'], c_int, 'msTimeout' ),
              ( ['out'], POINTER(c_int), 'pfs' )),
    COMMETHOD([dispid(1610743812)], HRESULT, 'RenderFile',
              ( ['in'], BSTR, 'strFilename' )),
    COMMETHOD([dispid(1610743813)], HRESULT, 'AddSourceFilter',
              ( ['in'], BSTR, 'strFilename' ),
              ( ['out'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
    COMMETHOD([dispid(1610743814), 'propget'], HRESULT, 'FilterCollection',
              ( ['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
    COMMETHOD([dispid(1610743815), 'propget'], HRESULT, 'RegFilterCollection',
              ( ['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
    COMMETHOD([dispid(1610743816)], HRESULT, 'StopWhenReady'),
]
################################################################
## code template for IMediaControl implementation
##class IMediaControl_Impl(object):
##    def Run(self):
##        '-no docstring-'
##        #return 
##
##    def Pause(self):
##        '-no docstring-'
##        #return 
##
##    def Stop(self):
##        '-no docstring-'
##        #return 
##
##    def GetState(self, msTimeout):
##        '-no docstring-'
##        #return pfs
##
##    def RenderFile(self, strFilename):
##        '-no docstring-'
##        #return 
##
##    def AddSourceFilter(self, strFilename):
##        '-no docstring-'
##        #return ppUnk
##
##    @property
##    def FilterCollection(self):
##        '-no docstring-'
##        #return ppUnk
##
##    @property
##    def RegFilterCollection(self):
##        '-no docstring-'
##        #return ppUnk
##
##    def StopWhenReady(self):
##        '-no docstring-'
##        #return 
##

class IAMCollection(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    'Collection'
    _iid_ = GUID('{56A868B9-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = ['dual', 'oleautomation']
IAMCollection._methods_ = [
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Count',
              ( ['out', 'retval'], POINTER(c_int), 'plCount' )),
    COMMETHOD([dispid(1610743809)], HRESULT, 'Item',
              ( ['in'], c_int, 'lItem' ),
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppUnk' )),
    COMMETHOD([dispid(1610743810), 'propget'], HRESULT, '_NewEnum',
              ( ['out', 'retval'], POINTER(POINTER(IUnknown)), 'ppUnk' )),
]
################################################################
## code template for IAMCollection implementation
##class IAMCollection_Impl(object):
##    @property
##    def Count(self):
##        '-no docstring-'
##        #return plCount
##
##    def Item(self, lItem):
##        '-no docstring-'
##        #return ppUnk
##
##    @property
##    def _NewEnum(self):
##        '-no docstring-'
##        #return ppUnk
##

class IMediaEvent(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    'IMediaEvent interface'
    _iid_ = GUID('{56A868B6-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = ['dual', 'oleautomation']
class IMediaEventEx(IMediaEvent):
    _case_insensitive_ = True
    'IMediaEventEx interface'
    _iid_ = GUID('{56A868C0-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = []
IMediaEvent._methods_ = [
    COMMETHOD([dispid(1610743808)], HRESULT, 'GetEventHandle',
              ( ['out'], POINTER(LONG_PTR), 'hEvent' )),
    COMMETHOD([dispid(1610743809)], HRESULT, 'GetEvent',
              ( ['out'], POINTER(c_int), 'lEventCode' ),
              ( ['out'], POINTER(LONG_PTR), 'lParam1' ),
              ( ['out'], POINTER(LONG_PTR), 'lParam2' ),
              ( ['in'], c_int, 'msTimeout' )),
    COMMETHOD([dispid(1610743810)], HRESULT, 'WaitForCompletion',
              ( ['in'], c_int, 'msTimeout' ),
              ( ['out'], POINTER(c_int), 'pEvCode' )),
    COMMETHOD([dispid(1610743811)], HRESULT, 'CancelDefaultHandling',
              ( ['in'], c_int, 'lEvCode' )),
    COMMETHOD([dispid(1610743812)], HRESULT, 'RestoreDefaultHandling',
              ( ['in'], c_int, 'lEvCode' )),
    COMMETHOD([dispid(1610743813)], HRESULT, 'FreeEventParams',
              ( ['in'], c_int, 'lEvCode' ),
              ( ['in'], LONG_PTR, 'lParam1' ),
              ( ['in'], LONG_PTR, 'lParam2' )),
]
################################################################
## code template for IMediaEvent implementation
##class IMediaEvent_Impl(object):
##    def GetEventHandle(self):
##        '-no docstring-'
##        #return hEvent
##
##    def GetEvent(self, msTimeout):
##        '-no docstring-'
##        #return lEventCode, lParam1, lParam2
##
##    def WaitForCompletion(self, msTimeout):
##        '-no docstring-'
##        #return pEvCode
##
##    def CancelDefaultHandling(self, lEvCode):
##        '-no docstring-'
##        #return 
##
##    def RestoreDefaultHandling(self, lEvCode):
##        '-no docstring-'
##        #return 
##
##    def FreeEventParams(self, lEvCode, lParam1, lParam2):
##        '-no docstring-'
##        #return 
##

IMediaEventEx._methods_ = [
    COMMETHOD([], HRESULT, 'SetNotifyWindow',
              ( ['in'], LONG_PTR, 'hwnd' ),
              ( ['in'], c_int, 'lMsg' ),
              ( ['in'], LONG_PTR, 'lInstanceData' )),
    COMMETHOD([], HRESULT, 'SetNotifyFlags',
              ( ['in'], c_int, 'lNoNotifyFlags' )),
    COMMETHOD([], HRESULT, 'GetNotifyFlags',
              ( ['out'], POINTER(c_int), 'lplNoNotifyFlags' )),
]
################################################################
## code template for IMediaEventEx implementation
##class IMediaEventEx_Impl(object):
##    def SetNotifyWindow(self, hwnd, lMsg, lInstanceData):
##        '-no docstring-'
##        #return 
##
##    def SetNotifyFlags(self, lNoNotifyFlags):
##        '-no docstring-'
##        #return 
##
##    def GetNotifyFlags(self):
##        '-no docstring-'
##        #return lplNoNotifyFlags
##

class IMediaTypeInfo(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    'Media Type'
    _iid_ = GUID('{56A868BC-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = ['dual', 'oleautomation']
IMediaTypeInfo._methods_ = [
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Type',
              ( ['out', 'retval'], POINTER(BSTR), 'strType' )),
    COMMETHOD([dispid(1610743809), 'propget'], HRESULT, 'Subtype',
              ( ['out', 'retval'], POINTER(BSTR), 'strType' )),
]
################################################################
## code template for IMediaTypeInfo implementation
##class IMediaTypeInfo_Impl(object):
##    @property
##    def Type(self):
##        '-no docstring-'
##        #return strType
##
##    @property
##    def Subtype(self):
##        '-no docstring-'
##        #return strType
##

class IDeferredCommand(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    'IDeferredCommand'
    _iid_ = GUID('{56A868B8-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = []
IDeferredCommand._methods_ = [
    COMMETHOD([], HRESULT, 'Cancel'),
    COMMETHOD([], HRESULT, 'Confidence',
              ( ['out'], POINTER(c_int), 'pConfidence' )),
    COMMETHOD([], HRESULT, 'Postpone',
              ( ['in'], c_double, 'newtime' )),
    COMMETHOD([], HRESULT, 'GetHResult',
              ( ['out'], POINTER(HRESULT), 'phrResult' )),
]
################################################################
## code template for IDeferredCommand implementation
##class IDeferredCommand_Impl(object):
##    def Cancel(self):
##        '-no docstring-'
##        #return 
##
##    def Confidence(self):
##        '-no docstring-'
##        #return pConfidence
##
##    def Postpone(self, newtime):
##        '-no docstring-'
##        #return 
##
##    def GetHResult(self):
##        '-no docstring-'
##        #return phrResult
##

class IVideoWindow(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    'IVideoWindow interface'
    _iid_ = GUID('{56A868B4-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = ['dual', 'oleautomation']
IVideoWindow._methods_ = [
    COMMETHOD([dispid(1610743808), 'propput'], HRESULT, 'Caption',
              ( ['in'], BSTR, 'strCaption' )),
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Caption',
              ( ['out', 'retval'], POINTER(BSTR), 'strCaption' )),
    COMMETHOD([dispid(1610743810), 'propput'], HRESULT, 'WindowStyle',
              ( ['in'], c_int, 'WindowStyle' )),
    COMMETHOD([dispid(1610743810), 'propget'], HRESULT, 'WindowStyle',
              ( ['out', 'retval'], POINTER(c_int), 'WindowStyle' )),
    COMMETHOD([dispid(1610743812), 'propput'], HRESULT, 'WindowStyleEx',
              ( ['in'], c_int, 'WindowStyleEx' )),
    COMMETHOD([dispid(1610743812), 'propget'], HRESULT, 'WindowStyleEx',
              ( ['out', 'retval'], POINTER(c_int), 'WindowStyleEx' )),
    COMMETHOD([dispid(1610743814), 'propput'], HRESULT, 'AutoShow',
              ( ['in'], c_int, 'AutoShow' )),
    COMMETHOD([dispid(1610743814), 'propget'], HRESULT, 'AutoShow',
              ( ['out', 'retval'], POINTER(c_int), 'AutoShow' )),
    COMMETHOD([dispid(1610743816), 'propput'], HRESULT, 'WindowState',
              ( ['in'], c_int, 'WindowState' )),
    COMMETHOD([dispid(1610743816), 'propget'], HRESULT, 'WindowState',
              ( ['out', 'retval'], POINTER(c_int), 'WindowState' )),
    COMMETHOD([dispid(1610743818), 'propput'], HRESULT, 'BackgroundPalette',
              ( ['in'], c_int, 'pBackgroundPalette' )),
    COMMETHOD([dispid(1610743818), 'propget'], HRESULT, 'BackgroundPalette',
              ( ['out', 'retval'], POINTER(c_int), 'pBackgroundPalette' )),
    COMMETHOD([dispid(1610743820), 'propput'], HRESULT, 'Visible',
              ( ['in'], c_int, 'pVisible' )),
    COMMETHOD([dispid(1610743820), 'propget'], HRESULT, 'Visible',
              ( ['out', 'retval'], POINTER(c_int), 'pVisible' )),
    COMMETHOD([dispid(1610743822), 'propput'], HRESULT, 'Left',
              ( ['in'], c_int, 'pLeft' )),
    COMMETHOD([dispid(1610743822), 'propget'], HRESULT, 'Left',
              ( ['out', 'retval'], POINTER(c_int), 'pLeft' )),
    COMMETHOD([dispid(1610743824), 'propput'], HRESULT, 'Width',
              ( ['in'], c_int, 'pWidth' )),
    COMMETHOD([dispid(1610743824), 'propget'], HRESULT, 'Width',
              ( ['out', 'retval'], POINTER(c_int), 'pWidth' )),
    COMMETHOD([dispid(1610743826), 'propput'], HRESULT, 'Top',
              ( ['in'], c_int, 'pTop' )),
    COMMETHOD([dispid(1610743826), 'propget'], HRESULT, 'Top',
              ( ['out', 'retval'], POINTER(c_int), 'pTop' )),
    COMMETHOD([dispid(1610743828), 'propput'], HRESULT, 'Height',
              ( ['in'], c_int, 'pHeight' )),
    COMMETHOD([dispid(1610743828), 'propget'], HRESULT, 'Height',
              ( ['out', 'retval'], POINTER(c_int), 'pHeight' )),
    COMMETHOD([dispid(1610743830), 'propput'], HRESULT, 'Owner',
              ( ['in'], LONG_PTR, 'Owner' )),
    COMMETHOD([dispid(1610743830), 'propget'], HRESULT, 'Owner',
              ( ['out', 'retval'], POINTER(LONG_PTR), 'Owner' )),
    COMMETHOD([dispid(1610743832), 'propput'], HRESULT, 'MessageDrain',
              ( ['in'], LONG_PTR, 'Drain' )),
    COMMETHOD([dispid(1610743832), 'propget'], HRESULT, 'MessageDrain',
              ( ['out', 'retval'], POINTER(LONG_PTR), 'Drain' )),
    COMMETHOD([dispid(1610743834), 'propget'], HRESULT, 'BorderColor',
              ( ['out', 'retval'], POINTER(c_int), 'Color' )),
    COMMETHOD([dispid(1610743834), 'propput'], HRESULT, 'BorderColor',
              ( ['in'], c_int, 'Color' )),
    COMMETHOD([dispid(1610743836), 'propget'], HRESULT, 'FullScreenMode',
              ( ['out', 'retval'], POINTER(c_int), 'FullScreenMode' )),
    COMMETHOD([dispid(1610743836), 'propput'], HRESULT, 'FullScreenMode',
              ( ['in'], c_int, 'FullScreenMode' )),
    COMMETHOD([dispid(1610743838)], HRESULT, 'SetWindowForeground',
              ( ['in'], c_int, 'Focus' )),
    COMMETHOD([dispid(1610743839)], HRESULT, 'NotifyOwnerMessage',
              ( ['in'], LONG_PTR, 'hwnd' ),
              ( ['in'], c_int, 'uMsg' ),
              ( ['in'], LONG_PTR, 'wParam' ),
              ( ['in'], LONG_PTR, 'lParam' )),
    COMMETHOD([dispid(1610743840)], HRESULT, 'SetWindowPosition',
              ( ['in'], c_int, 'Left' ),
              ( ['in'], c_int, 'Top' ),
              ( ['in'], c_int, 'Width' ),
              ( ['in'], c_int, 'Height' )),
    COMMETHOD([dispid(1610743841)], HRESULT, 'GetWindowPosition',
              ( ['out'], POINTER(c_int), 'pLeft' ),
              ( ['out'], POINTER(c_int), 'pTop' ),
              ( ['out'], POINTER(c_int), 'pWidth' ),
              ( ['out'], POINTER(c_int), 'pHeight' )),
    COMMETHOD([dispid(1610743842)], HRESULT, 'GetMinIdealImageSize',
              ( ['out'], POINTER(c_int), 'pWidth' ),
              ( ['out'], POINTER(c_int), 'pHeight' )),
    COMMETHOD([dispid(1610743843)], HRESULT, 'GetMaxIdealImageSize',
              ( ['out'], POINTER(c_int), 'pWidth' ),
              ( ['out'], POINTER(c_int), 'pHeight' )),
    COMMETHOD([dispid(1610743844)], HRESULT, 'GetRestorePosition',
              ( ['out'], POINTER(c_int), 'pLeft' ),
              ( ['out'], POINTER(c_int), 'pTop' ),
              ( ['out'], POINTER(c_int), 'pWidth' ),
              ( ['out'], POINTER(c_int), 'pHeight' )),
    COMMETHOD([dispid(1610743845)], HRESULT, 'HideCursor',
              ( ['in'], c_int, 'HideCursor' )),
    COMMETHOD([dispid(1610743846)], HRESULT, 'IsCursorHidden',
              ( ['out'], POINTER(c_int), 'CursorHidden' )),
]
################################################################
## code template for IVideoWindow implementation
##class IVideoWindow_Impl(object):
##    def _get(self):
##        '-no docstring-'
##        #return strCaption
##    def _set(self, strCaption):
##        '-no docstring-'
##    Caption = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return WindowStyle
##    def _set(self, WindowStyle):
##        '-no docstring-'
##    WindowStyle = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return WindowStyleEx
##    def _set(self, WindowStyleEx):
##        '-no docstring-'
##    WindowStyleEx = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return AutoShow
##    def _set(self, AutoShow):
##        '-no docstring-'
##    AutoShow = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return WindowState
##    def _set(self, WindowState):
##        '-no docstring-'
##    WindowState = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pBackgroundPalette
##    def _set(self, pBackgroundPalette):
##        '-no docstring-'
##    BackgroundPalette = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pVisible
##    def _set(self, pVisible):
##        '-no docstring-'
##    Visible = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pLeft
##    def _set(self, pLeft):
##        '-no docstring-'
##    Left = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pWidth
##    def _set(self, pWidth):
##        '-no docstring-'
##    Width = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pTop
##    def _set(self, pTop):
##        '-no docstring-'
##    Top = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pHeight
##    def _set(self, pHeight):
##        '-no docstring-'
##    Height = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return Owner
##    def _set(self, Owner):
##        '-no docstring-'
##    Owner = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return Drain
##    def _set(self, Drain):
##        '-no docstring-'
##    MessageDrain = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return Color
##    def _set(self, Color):
##        '-no docstring-'
##    BorderColor = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return FullScreenMode
##    def _set(self, FullScreenMode):
##        '-no docstring-'
##    FullScreenMode = property(_get, _set, doc = _set.__doc__)
##
##    def SetWindowForeground(self, Focus):
##        '-no docstring-'
##        #return 
##
##    def NotifyOwnerMessage(self, hwnd, uMsg, wParam, lParam):
##        '-no docstring-'
##        #return 
##
##    def SetWindowPosition(self, Left, Top, Width, Height):
##        '-no docstring-'
##        #return 
##
##    def GetWindowPosition(self):
##        '-no docstring-'
##        #return pLeft, pTop, pWidth, pHeight
##
##    def GetMinIdealImageSize(self):
##        '-no docstring-'
##        #return pWidth, pHeight
##
##    def GetMaxIdealImageSize(self):
##        '-no docstring-'
##        #return pWidth, pHeight
##
##    def GetRestorePosition(self):
##        '-no docstring-'
##        #return pLeft, pTop, pWidth, pHeight
##
##    def HideCursor(self, HideCursor):
##        '-no docstring-'
##        #return 
##
##    def IsCursorHidden(self):
##        '-no docstring-'
##        #return CursorHidden
##

class IBasicVideo(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    'IBasicVideo interface'
    _iid_ = GUID('{56A868B5-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = ['dual', 'oleautomation']
class IBasicVideo2(IBasicVideo):
    _case_insensitive_ = True
    'IBasicVideo2'
    _iid_ = GUID('{329BB360-F6EA-11D1-9038-00A0C9697298}')
    _idlflags_ = []
IBasicVideo._methods_ = [
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'AvgTimePerFrame',
              ( ['out', 'retval'], POINTER(c_double), 'pAvgTimePerFrame' )),
    COMMETHOD([dispid(1610743809), 'propget'], HRESULT, 'BitRate',
              ( ['out', 'retval'], POINTER(c_int), 'pBitRate' )),
    COMMETHOD([dispid(1610743810), 'propget'], HRESULT, 'BitErrorRate',
              ( ['out', 'retval'], POINTER(c_int), 'pBitErrorRate' )),
    COMMETHOD([dispid(1610743811), 'propget'], HRESULT, 'VideoWidth',
              ( ['out', 'retval'], POINTER(c_int), 'pVideoWidth' )),
    COMMETHOD([dispid(1610743812), 'propget'], HRESULT, 'VideoHeight',
              ( ['out', 'retval'], POINTER(c_int), 'pVideoHeight' )),
    COMMETHOD([dispid(1610743813), 'propput'], HRESULT, 'SourceLeft',
              ( ['in'], c_int, 'pSourceLeft' )),
    COMMETHOD([dispid(1610743813), 'propget'], HRESULT, 'SourceLeft',
              ( ['out', 'retval'], POINTER(c_int), 'pSourceLeft' )),
    COMMETHOD([dispid(1610743815), 'propput'], HRESULT, 'SourceWidth',
              ( ['in'], c_int, 'pSourceWidth' )),
    COMMETHOD([dispid(1610743815), 'propget'], HRESULT, 'SourceWidth',
              ( ['out', 'retval'], POINTER(c_int), 'pSourceWidth' )),
    COMMETHOD([dispid(1610743817), 'propput'], HRESULT, 'SourceTop',
              ( ['in'], c_int, 'pSourceTop' )),
    COMMETHOD([dispid(1610743817), 'propget'], HRESULT, 'SourceTop',
              ( ['out', 'retval'], POINTER(c_int), 'pSourceTop' )),
    COMMETHOD([dispid(1610743819), 'propput'], HRESULT, 'SourceHeight',
              ( ['in'], c_int, 'pSourceHeight' )),
    COMMETHOD([dispid(1610743819), 'propget'], HRESULT, 'SourceHeight',
              ( ['out', 'retval'], POINTER(c_int), 'pSourceHeight' )),
    COMMETHOD([dispid(1610743821), 'propput'], HRESULT, 'DestinationLeft',
              ( ['in'], c_int, 'pDestinationLeft' )),
    COMMETHOD([dispid(1610743821), 'propget'], HRESULT, 'DestinationLeft',
              ( ['out', 'retval'], POINTER(c_int), 'pDestinationLeft' )),
    COMMETHOD([dispid(1610743823), 'propput'], HRESULT, 'DestinationWidth',
              ( ['in'], c_int, 'pDestinationWidth' )),
    COMMETHOD([dispid(1610743823), 'propget'], HRESULT, 'DestinationWidth',
              ( ['out', 'retval'], POINTER(c_int), 'pDestinationWidth' )),
    COMMETHOD([dispid(1610743825), 'propput'], HRESULT, 'DestinationTop',
              ( ['in'], c_int, 'pDestinationTop' )),
    COMMETHOD([dispid(1610743825), 'propget'], HRESULT, 'DestinationTop',
              ( ['out', 'retval'], POINTER(c_int), 'pDestinationTop' )),
    COMMETHOD([dispid(1610743827), 'propput'], HRESULT, 'DestinationHeight',
              ( ['in'], c_int, 'pDestinationHeight' )),
    COMMETHOD([dispid(1610743827), 'propget'], HRESULT, 'DestinationHeight',
              ( ['out', 'retval'], POINTER(c_int), 'pDestinationHeight' )),
    COMMETHOD([dispid(1610743829)], HRESULT, 'SetSourcePosition',
              ( ['in'], c_int, 'Left' ),
              ( ['in'], c_int, 'Top' ),
              ( ['in'], c_int, 'Width' ),
              ( ['in'], c_int, 'Height' )),
    COMMETHOD([dispid(1610743830)], HRESULT, 'GetSourcePosition',
              ( ['out'], POINTER(c_int), 'pLeft' ),
              ( ['out'], POINTER(c_int), 'pTop' ),
              ( ['out'], POINTER(c_int), 'pWidth' ),
              ( ['out'], POINTER(c_int), 'pHeight' )),
    COMMETHOD([dispid(1610743831)], HRESULT, 'SetDefaultSourcePosition'),
    COMMETHOD([dispid(1610743832)], HRESULT, 'SetDestinationPosition',
              ( ['in'], c_int, 'Left' ),
              ( ['in'], c_int, 'Top' ),
              ( ['in'], c_int, 'Width' ),
              ( ['in'], c_int, 'Height' )),
    COMMETHOD([dispid(1610743833)], HRESULT, 'GetDestinationPosition',
              ( ['out'], POINTER(c_int), 'pLeft' ),
              ( ['out'], POINTER(c_int), 'pTop' ),
              ( ['out'], POINTER(c_int), 'pWidth' ),
              ( ['out'], POINTER(c_int), 'pHeight' )),
    COMMETHOD([dispid(1610743834)], HRESULT, 'SetDefaultDestinationPosition'),
    COMMETHOD([dispid(1610743835)], HRESULT, 'GetVideoSize',
              ( ['out'], POINTER(c_int), 'pWidth' ),
              ( ['out'], POINTER(c_int), 'pHeight' )),
    COMMETHOD([dispid(1610743836)], HRESULT, 'GetVideoPaletteEntries',
              ( ['in'], c_int, 'StartIndex' ),
              ( ['in'], c_int, 'Entries' ),
              ( ['out'], POINTER(c_int), 'pRetrieved' ),
              ( ['out'], POINTER(c_int), 'pPalette' )),
    COMMETHOD([dispid(1610743837)], HRESULT, 'GetCurrentImage',
              ( ['in', 'out'], POINTER(c_int), 'pBufferSize' ),
              ( ['out'], POINTER(c_int), 'pDIBImage' )),
    COMMETHOD([dispid(1610743838)], HRESULT, 'IsUsingDefaultSource'),
    COMMETHOD([dispid(1610743839)], HRESULT, 'IsUsingDefaultDestination'),
]
################################################################
## code template for IBasicVideo implementation
##class IBasicVideo_Impl(object):
##    @property
##    def AvgTimePerFrame(self):
##        '-no docstring-'
##        #return pAvgTimePerFrame
##
##    @property
##    def BitRate(self):
##        '-no docstring-'
##        #return pBitRate
##
##    @property
##    def BitErrorRate(self):
##        '-no docstring-'
##        #return pBitErrorRate
##
##    @property
##    def VideoWidth(self):
##        '-no docstring-'
##        #return pVideoWidth
##
##    @property
##    def VideoHeight(self):
##        '-no docstring-'
##        #return pVideoHeight
##
##    def _get(self):
##        '-no docstring-'
##        #return pSourceLeft
##    def _set(self, pSourceLeft):
##        '-no docstring-'
##    SourceLeft = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pSourceWidth
##    def _set(self, pSourceWidth):
##        '-no docstring-'
##    SourceWidth = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pSourceTop
##    def _set(self, pSourceTop):
##        '-no docstring-'
##    SourceTop = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pSourceHeight
##    def _set(self, pSourceHeight):
##        '-no docstring-'
##    SourceHeight = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pDestinationLeft
##    def _set(self, pDestinationLeft):
##        '-no docstring-'
##    DestinationLeft = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pDestinationWidth
##    def _set(self, pDestinationWidth):
##        '-no docstring-'
##    DestinationWidth = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pDestinationTop
##    def _set(self, pDestinationTop):
##        '-no docstring-'
##    DestinationTop = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pDestinationHeight
##    def _set(self, pDestinationHeight):
##        '-no docstring-'
##    DestinationHeight = property(_get, _set, doc = _set.__doc__)
##
##    def SetSourcePosition(self, Left, Top, Width, Height):
##        '-no docstring-'
##        #return 
##
##    def GetSourcePosition(self):
##        '-no docstring-'
##        #return pLeft, pTop, pWidth, pHeight
##
##    def SetDefaultSourcePosition(self):
##        '-no docstring-'
##        #return 
##
##    def SetDestinationPosition(self, Left, Top, Width, Height):
##        '-no docstring-'
##        #return 
##
##    def GetDestinationPosition(self):
##        '-no docstring-'
##        #return pLeft, pTop, pWidth, pHeight
##
##    def SetDefaultDestinationPosition(self):
##        '-no docstring-'
##        #return 
##
##    def GetVideoSize(self):
##        '-no docstring-'
##        #return pWidth, pHeight
##
##    def GetVideoPaletteEntries(self, StartIndex, Entries):
##        '-no docstring-'
##        #return pRetrieved, pPalette
##
##    def GetCurrentImage(self):
##        '-no docstring-'
##        #return pBufferSize, pDIBImage
##
##    def IsUsingDefaultSource(self):
##        '-no docstring-'
##        #return 
##
##    def IsUsingDefaultDestination(self):
##        '-no docstring-'
##        #return 
##

IBasicVideo2._methods_ = [
    COMMETHOD([], HRESULT, 'GetPreferredAspectRatio',
              ( ['out'], POINTER(c_int), 'plAspectX' ),
              ( ['out'], POINTER(c_int), 'plAspectY' )),
]
################################################################
## code template for IBasicVideo2 implementation
##class IBasicVideo2_Impl(object):
##    def GetPreferredAspectRatio(self):
##        '-no docstring-'
##        #return plAspectX, plAspectY
##

class IMediaPosition(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    'IMediaPosition interface'
    _iid_ = GUID('{56A868B2-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = ['dual', 'oleautomation']
IMediaPosition._methods_ = [
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Duration',
              ( ['out', 'retval'], POINTER(c_double), 'plength' )),
    COMMETHOD([dispid(1610743809), 'propput'], HRESULT, 'CurrentPosition',
              ( ['in'], c_double, 'pllTime' )),
    COMMETHOD([dispid(1610743809), 'propget'], HRESULT, 'CurrentPosition',
              ( ['out', 'retval'], POINTER(c_double), 'pllTime' )),
    COMMETHOD([dispid(1610743811), 'propget'], HRESULT, 'StopTime',
              ( ['out', 'retval'], POINTER(c_double), 'pllTime' )),
    COMMETHOD([dispid(1610743811), 'propput'], HRESULT, 'StopTime',
              ( ['in'], c_double, 'pllTime' )),
    COMMETHOD([dispid(1610743813), 'propget'], HRESULT, 'PrerollTime',
              ( ['out', 'retval'], POINTER(c_double), 'pllTime' )),
    COMMETHOD([dispid(1610743813), 'propput'], HRESULT, 'PrerollTime',
              ( ['in'], c_double, 'pllTime' )),
    COMMETHOD([dispid(1610743815), 'propput'], HRESULT, 'Rate',
              ( ['in'], c_double, 'pdRate' )),
    COMMETHOD([dispid(1610743815), 'propget'], HRESULT, 'Rate',
              ( ['out', 'retval'], POINTER(c_double), 'pdRate' )),
    COMMETHOD([dispid(1610743817)], HRESULT, 'CanSeekForward',
              ( ['out', 'retval'], POINTER(c_int), 'pCanSeekForward' )),
    COMMETHOD([dispid(1610743818)], HRESULT, 'CanSeekBackward',
              ( ['out', 'retval'], POINTER(c_int), 'pCanSeekBackward' )),
]
################################################################
## code template for IMediaPosition implementation
##class IMediaPosition_Impl(object):
##    @property
##    def Duration(self):
##        '-no docstring-'
##        #return plength
##
##    def _get(self):
##        '-no docstring-'
##        #return pllTime
##    def _set(self, pllTime):
##        '-no docstring-'
##    CurrentPosition = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pllTime
##    def _set(self, pllTime):
##        '-no docstring-'
##    StopTime = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pllTime
##    def _set(self, pllTime):
##        '-no docstring-'
##    PrerollTime = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pdRate
##    def _set(self, pdRate):
##        '-no docstring-'
##    Rate = property(_get, _set, doc = _set.__doc__)
##
##    def CanSeekForward(self):
##        '-no docstring-'
##        #return pCanSeekForward
##
##    def CanSeekBackward(self):
##        '-no docstring-'
##        #return pCanSeekBackward
##

class IAMStats(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    'Statistics'
    _iid_ = GUID('{BC9BCF80-DCD2-11D2-ABF6-00A0C905F375}')
    _idlflags_ = ['dual', 'oleautomation']
IAMStats._methods_ = [
    COMMETHOD([dispid(1610743808)], HRESULT, 'Reset'),
    COMMETHOD([dispid(1610743809), 'propget'], HRESULT, 'Count',
              ( ['out', 'retval'], POINTER(c_int), 'plCount' )),
    COMMETHOD([dispid(1610743810)], HRESULT, 'GetValueByIndex',
              ( ['in'], c_int, 'lIndex' ),
              ( ['out'], POINTER(BSTR), 'szName' ),
              ( ['out'], POINTER(c_int), 'lCount' ),
              ( ['out'], POINTER(c_double), 'dLast' ),
              ( ['out'], POINTER(c_double), 'dAverage' ),
              ( ['out'], POINTER(c_double), 'dStdDev' ),
              ( ['out'], POINTER(c_double), 'dMin' ),
              ( ['out'], POINTER(c_double), 'dMax' )),
    COMMETHOD([dispid(1610743811)], HRESULT, 'GetValueByName',
              ( ['in'], BSTR, 'szName' ),
              ( ['out'], POINTER(c_int), 'lIndex' ),
              ( ['out'], POINTER(c_int), 'lCount' ),
              ( ['out'], POINTER(c_double), 'dLast' ),
              ( ['out'], POINTER(c_double), 'dAverage' ),
              ( ['out'], POINTER(c_double), 'dStdDev' ),
              ( ['out'], POINTER(c_double), 'dMin' ),
              ( ['out'], POINTER(c_double), 'dMax' )),
    COMMETHOD([dispid(1610743812)], HRESULT, 'GetIndex',
              ( ['in'], BSTR, 'szName' ),
              ( ['in'], c_int, 'lCreate' ),
              ( ['out'], POINTER(c_int), 'plIndex' )),
    COMMETHOD([dispid(1610743813)], HRESULT, 'AddValue',
              ( ['in'], c_int, 'lIndex' ),
              ( ['in'], c_double, 'dValue' )),
]
################################################################
## code template for IAMStats implementation
##class IAMStats_Impl(object):
##    def Reset(self):
##        '-no docstring-'
##        #return 
##
##    @property
##    def Count(self):
##        '-no docstring-'
##        #return plCount
##
##    def GetValueByIndex(self, lIndex):
##        '-no docstring-'
##        #return szName, lCount, dLast, dAverage, dStdDev, dMin, dMax
##
##    def GetValueByName(self, szName):
##        '-no docstring-'
##        #return lIndex, lCount, dLast, dAverage, dStdDev, dMin, dMax
##
##    def GetIndex(self, szName, lCreate):
##        '-no docstring-'
##        #return plIndex
##
##    def AddValue(self, lIndex, dValue):
##        '-no docstring-'
##        #return 
##

class IFilterInfo(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    'FilterInfo'
    _iid_ = GUID('{56A868BA-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = ['dual', 'oleautomation']
IFilterInfo._methods_ = [
    COMMETHOD([dispid(1610743808)], HRESULT, 'FindPin',
              ( ['in'], BSTR, 'strPinID' ),
              ( ['out'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
    COMMETHOD([dispid(1610743809), 'propget'], HRESULT, 'Name',
              ( ['out', 'retval'], POINTER(BSTR), 'strName' )),
    COMMETHOD([dispid(1610743810), 'propget'], HRESULT, 'VendorInfo',
              ( ['out', 'retval'], POINTER(BSTR), 'strVendorInfo' )),
    COMMETHOD([dispid(1610743811), 'propget'], HRESULT, 'Filter',
              ( ['out', 'retval'], POINTER(POINTER(IUnknown)), 'ppUnk' )),
    COMMETHOD([dispid(1610743812), 'propget'], HRESULT, 'Pins',
              ( ['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
    COMMETHOD([dispid(1610743813), 'propget'], HRESULT, 'IsFileSource',
              ( ['out', 'retval'], POINTER(c_int), 'pbIsSource' )),
    COMMETHOD([dispid(1610743814), 'propget'], HRESULT, 'Filename',
              ( ['out', 'retval'], POINTER(BSTR), 'pstrFilename' )),
    COMMETHOD([dispid(1610743814), 'propput'], HRESULT, 'Filename',
              ( ['in'], BSTR, 'pstrFilename' )),
]
################################################################
## code template for IFilterInfo implementation
##class IFilterInfo_Impl(object):
##    def FindPin(self, strPinID):
##        '-no docstring-'
##        #return ppUnk
##
##    @property
##    def Name(self):
##        '-no docstring-'
##        #return strName
##
##    @property
##    def VendorInfo(self):
##        '-no docstring-'
##        #return strVendorInfo
##
##    @property
##    def Filter(self):
##        '-no docstring-'
##        #return ppUnk
##
##    @property
##    def Pins(self):
##        '-no docstring-'
##        #return ppUnk
##
##    @property
##    def IsFileSource(self):
##        '-no docstring-'
##        #return pbIsSource
##
##    def _get(self):
##        '-no docstring-'
##        #return pstrFilename
##    def _set(self, pstrFilename):
##        '-no docstring-'
##    Filename = property(_get, _set, doc = _set.__doc__)
##

class IQueueCommand(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    'IQueueCommand'
    _iid_ = GUID('{56A868B7-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = []
IQueueCommand._methods_ = [
    COMMETHOD([], HRESULT, 'InvokeAtStreamTime',
              ( ['out'], POINTER(POINTER(IDeferredCommand)), 'pCmd' ),
              ( ['in'], c_double, 'time' ),
              ( ['in'], POINTER(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'iid' ),
              ( ['in'], c_int, 'dispidMethod' ),
              ( ['in'], c_short, 'wFlags' ),
              ( ['in'], c_int, 'cArgs' ),
              ( ['in'], POINTER(VARIANT), 'pDispParams' ),
              ( ['in', 'out'], POINTER(VARIANT), 'pvarResult' ),
              ( ['out'], POINTER(c_short), 'puArgErr' )),
    COMMETHOD([], HRESULT, 'InvokeAtPresentationTime',
              ( ['out'], POINTER(POINTER(IDeferredCommand)), 'pCmd' ),
              ( ['in'], c_double, 'time' ),
              ( ['in'], POINTER(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'iid' ),
              ( ['in'], c_int, 'dispidMethod' ),
              ( ['in'], c_short, 'wFlags' ),
              ( ['in'], c_int, 'cArgs' ),
              ( ['in'], POINTER(VARIANT), 'pDispParams' ),
              ( ['in', 'out'], POINTER(VARIANT), 'pvarResult' ),
              ( ['out'], POINTER(c_short), 'puArgErr' )),
]
################################################################
## code template for IQueueCommand implementation
##class IQueueCommand_Impl(object):
##    def InvokeAtStreamTime(self, time, iid, dispidMethod, wFlags, cArgs, pDispParams):
##        '-no docstring-'
##        #return pCmd, pvarResult, puArgErr
##
##    def InvokeAtPresentationTime(self, time, iid, dispidMethod, wFlags, cArgs, pDispParams):
##        '-no docstring-'
##        #return pCmd, pvarResult, puArgErr
##

class FilgraphManager(CoClass):
    'Filtergraph type info'
    _reg_clsid_ = GUID('{E436EBB3-524F-11CE-9F53-0020AF0BA770}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{56A868B0-0AD4-11CE-B03A-0020AF0BA770}', 1, 0)
FilgraphManager._com_interfaces_ = [IMediaControl, IMediaEvent, IMediaPosition, IBasicAudio, IBasicVideo, IVideoWindow]

class Library(object):
    'ActiveMovie control type library'
    name = 'QuartzTypeLib'
    _reg_typelib_ = ('{56A868B0-0AD4-11CE-B03A-0020AF0BA770}', 1, 0)

class IRegFilterInfo(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    'Registry Filter Info'
    _iid_ = GUID('{56A868BB-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = ['dual', 'oleautomation']
IRegFilterInfo._methods_ = [
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Name',
              ( ['out', 'retval'], POINTER(BSTR), 'strName' )),
    COMMETHOD([dispid(1610743809)], HRESULT, 'Filter',
              ( ['out'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
]
################################################################
## code template for IRegFilterInfo implementation
##class IRegFilterInfo_Impl(object):
##    @property
##    def Name(self):
##        '-no docstring-'
##        #return strName
##
##    def Filter(self):
##        '-no docstring-'
##        #return ppUnk
##

class IPinInfo(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    'Pin Info'
    _iid_ = GUID('{56A868BD-0AD4-11CE-B03A-0020AF0BA770}')
    _idlflags_ = ['dual', 'oleautomation']
IPinInfo._methods_ = [
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Pin',
              ( ['out', 'retval'], POINTER(POINTER(IUnknown)), 'ppUnk' )),
    COMMETHOD([dispid(1610743809), 'propget'], HRESULT, 'ConnectedTo',
              ( ['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
    COMMETHOD([dispid(1610743810), 'propget'], HRESULT, 'ConnectionMediaType',
              ( ['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
    COMMETHOD([dispid(1610743811), 'propget'], HRESULT, 'FilterInfo',
              ( ['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
    COMMETHOD([dispid(1610743812), 'propget'], HRESULT, 'Name',
              ( ['out', 'retval'], POINTER(BSTR), 'ppUnk' )),
    COMMETHOD([dispid(1610743813), 'propget'], HRESULT, 'Direction',
              ( ['out', 'retval'], POINTER(c_int), 'ppDirection' )),
    COMMETHOD([dispid(1610743814), 'propget'], HRESULT, 'PinID',
              ( ['out', 'retval'], POINTER(BSTR), 'strPinID' )),
    COMMETHOD([dispid(1610743815), 'propget'], HRESULT, 'MediaTypes',
              ( ['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
    COMMETHOD([dispid(1610743816)], HRESULT, 'Connect',
              ( ['in'], POINTER(IUnknown), 'pPin' )),
    COMMETHOD([dispid(1610743817)], HRESULT, 'ConnectDirect',
              ( ['in'], POINTER(IUnknown), 'pPin' )),
    COMMETHOD([dispid(1610743818)], HRESULT, 'ConnectWithType',
              ( ['in'], POINTER(IUnknown), 'pPin' ),
              ( ['in'], POINTER(IDispatch), 'pMediaType' )),
    COMMETHOD([dispid(1610743819)], HRESULT, 'Disconnect'),
    COMMETHOD([dispid(1610743820)], HRESULT, 'Render'),
]
################################################################
## code template for IPinInfo implementation
##class IPinInfo_Impl(object):
##    @property
##    def Pin(self):
##        '-no docstring-'
##        #return ppUnk
##
##    @property
##    def ConnectedTo(self):
##        '-no docstring-'
##        #return ppUnk
##
##    @property
##    def ConnectionMediaType(self):
##        '-no docstring-'
##        #return ppUnk
##
##    @property
##    def FilterInfo(self):
##        '-no docstring-'
##        #return ppUnk
##
##    @property
##    def Name(self):
##        '-no docstring-'
##        #return ppUnk
##
##    @property
##    def Direction(self):
##        '-no docstring-'
##        #return ppDirection
##
##    @property
##    def PinID(self):
##        '-no docstring-'
##        #return strPinID
##
##    @property
##    def MediaTypes(self):
##        '-no docstring-'
##        #return ppUnk
##
##    def Connect(self, pPin):
##        '-no docstring-'
##        #return 
##
##    def ConnectDirect(self, pPin):
##        '-no docstring-'
##        #return 
##
##    def ConnectWithType(self, pPin, pMediaType):
##        '-no docstring-'
##        #return 
##
##    def Disconnect(self):
##        '-no docstring-'
##        #return 
##
##    def Render(self):
##        '-no docstring-'
##        #return 
##

__all__ = [ 'IQueueCommand', 'IMediaEventEx', 'IAMCollection',
           'IMediaTypeInfo', 'LONG_PTR', 'IMediaEvent',
           'IVideoWindow', 'IMediaPosition', 'IRegFilterInfo',
           'IFilterInfo', 'FilgraphManager', 'IBasicVideo2',
           'IPinInfo', 'IAMStats', 'IBasicAudio', 'IBasicVideo',
           'IDeferredCommand', 'IMediaControl']
from comtypes import _check_version; _check_version('1.1.11', 1611459624.5344577)
