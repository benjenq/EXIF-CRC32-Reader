from geopy.geocoders import Nominatim
import sys, traceback
geoLoc = None
def Reverse(latitude:float, logitude:float):
    '''GPS座標反解析
    ---
    latitude : 緯度
    logitude : 經度
    '''
    if abs(latitude) > 90 or abs(logitude) > 180:
        return False, 'Error GPS Coordinate'
    global geoLoc
    if geoLoc == None:
        #calling the nominatim tool
        geoLoc = Nominatim(user_agent="取得".encode("utf-8"))
    # passing the coordinates
    try:
        locname = geoLoc.reverse(f'{latitude},{logitude}')
        tmpAddrArray = [s.strip() for s in locname.address.split(',')]
        if '臺灣' in tmpAddrArray or '台灣' in tmpAddrArray or '日本' in tmpAddrArray or '中国' in tmpAddrArray:
            #todo
            tmpAddrArray = tmpAddrArray[::-1]
            strippedAddr = ''.join(tmpAddrArray)
        else:
            strippedAddr = ', '.join(tmpAddrArray)
        return True, strippedAddr
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return False, 'Failed to resolve address.\nPlease check internet.'