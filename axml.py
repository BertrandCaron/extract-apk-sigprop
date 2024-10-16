endDocTag = 0x00100101
startTag = 0x00100102
endTag = 0x00100103

def decompressXML( xml: bytearray) -> str:
        
    finalXml = str()
      
    numbStrings = LEW(xml, 4*4)
        
    sitOff = 0x24
    stOff = sitOff + numbStrings * 4
    xmlTagOff = LEW(xml, 3 * 4)
    for i in range(xmlTagOff, len(xml) - 4, 4):
        if LEW(xml, i) == startTag:
            xmlTagOff = i
            break
        
    off = xmlTagOff
        
    while (off < len(xml)):
        tag0 = LEW(xml, off)
        nameSi = LEW(xml, off + 5 * 4)

        if tag0 == startTag:
            numbAttrs = LEW(xml, off + 7*4)
            off += 9*4
            name = compXmlString(xml, sitOff, stOff, nameSi)
            sb = str()
            for i in range(numbAttrs):
                attrNameSi      = LEW(xml, off +   1 * 4 )
                attrValueSi     = LEW(xml, off +   2 * 4 )
                attrResId       = LEW(xml, off +   4 * 4 )

                off += 5*4

                attrName = compXmlString(xml,sitOff,stOff,attrNameSi)
                attrValue = str()
                if attrValueSi != -1:
                    attrValue = compXmlString(xml, sitOff, stOff, attrValueSi)
                else:
                    attrValue = "resourceID " + hex(attrResId) 
                sb += " " + attrName + "=\"" + attrValue + "\""
            finalXml += "<" + name + sb + ">"
        elif tag0 == endTag:
            off += 6*4
            name = compXmlString(xml, sitOff, stOff, nameSi)
            finalXml += "</" + name + ">"
        elif tag0 == endDocTag:
            break
        else:
            break
    return finalXml


def compXmlString( xml: bytearray, sitOff: int, stOff: int, strInd: int) -> str:
    if strInd < 0:
        return None
    strOff = stOff + LEW(xml, sitOff + strInd*4)
    return compXmlStringAt(xml, strOff)

def compXmlStringAt( arr: bytearray, strOff: bytearray) -> str:
    strlen = arr[strOff + 1] << 8 & 0xff00 | arr[strOff] & 0xff
    chars = bytearray()
    for i in range(strlen):
        chars.append(arr[strOff + 2 + i*2])
    return chars.decode("utf-8")

def LEW( arr: bytearray, off: int) -> int:
    c = arr[off + 3] << 24 & 0xff000000 | arr[off + 2] << 16 & 0xff0000 | arr[off + 1] << 8 & 0xff00 | arr[off] & 0xFF
    if c < -2147483648 or c > 2147483647:
        return int(-1)
    return c


def convertResult(str_res) -> str:
    str_convert = ''

    if str_res.find('resourceID') != -1:
        if str_res == 'resourceID 0x0':
            str_convert = 'False'
        elif str_res == 'resourceID -0x1':
            str_convert = 'True'
        else:
            str_convert = str_res[13:]


    return str_convert
