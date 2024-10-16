#https://developer.android.com/guide/topics/manifest/supports-screens-element
#https://gist.github.com/handstandsam/7a572d0fbb39416cca3d036d71405f41
#https://gist.github.com/karnauskas/81260e09b94e7f308ec1eedcfbca8c51

from xml.dom.minidom import parseString
from xml.dom import minidom 
import sys
from configparser import ConfigParser
from axml import decompressXML,convertResult
from zipfile import ZipFile 

def extract_significant_properties(file_name: str, outFile: str):
    """
    This function reads the manifest file from a manifest filename or an APK package filename - passed in argument and generates an xml file with the desired tags and attributes.
    The config file axml.ini contains the tags and attributes to be extracted.

    Parameters:
    file_name (str): The name of the manifest file or the .apk file.
    outFile (str): The name of the output xml file.

    Returns:
    None
    """

    if file_name.upper().find(".XML") == -1:
        with ZipFile(file_name, 'r') as apkfile: 
            apkfile.extract("AndroidManifest.xml") 
        apkfile.close()
        file_name = "AndroidManifest.xml"

    
    config = ConfigParser()
    config.read('axml.ini')
    nb = config.getint('nb', 'nb')
    elements_to_extract = []
    for i in range(1, nb + 1):
        element = config.get('tag', str(i))
        elements_to_extract.append(element)    
    
    data = decompressXML(open(file_name,'rb').read())
    dom = parseString(data) # parse file contents to xml dom

    root = minidom.Document()
    xml = root.createElement('root')  
    root.appendChild(xml)
    productChild = root.createElement(file_name)
    xml.appendChild(productChild) 

    for element in elements_to_extract:
        element_name = element.split('@')[0]
        element_attributes = element.split('@')[1:]
        tag_element = dom.getElementsByTagName(element_name)
        if len(tag_element) != 0:
            for ele in tag_element:
                for i in range(len(element_attributes)):
                    value = ele.getAttribute(element_attributes[i])
                    productChild = root.createElement(element_name)
                    if value != "":
                        if value.startswith("resourceID"):
                            value = convertResult(value)
                        # insert user data into element
                        productChild.setAttribute(element_attributes[i], value) 
                        xml.appendChild(productChild) 
                        print(element_name + "@" + element_attributes[i] + f": {value}" )
                    else:
                        productChild.setAttribute(element_attributes[i], "absent") 
                        xml.appendChild(productChild)
                        print(element_name + "@" + element_attributes[i] + ": absent")
        else:
            for i in range(len(element_attributes)):
                    productChild = root.createElement(element_name)
                    # insert user data into element
                    productChild.setAttribute(element_attributes[i], "absent" ) 
                    xml.appendChild(productChild) 
                                    
                    print(element_name + "@" + element_attributes[i] + ": absent")

    xml_str = root.toprettyxml(indent ="\t") 
    
    # save file
    save_path_file = outFile
    
    with open(save_path_file, "w") as f: 
        f.write(xml_str) 


if __name__ == "__main__":
    
    if len(sys.argv) == 3:
        extract_significant_properties(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        extract_significant_properties(sys.argv[1], "result.xml")
    else:
        raise Exception("Invalid number of arguments")
