#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# see main.py for copyright, contacts and version information
#
# Hinweis: uebergebene Strings muessen im UTF-8-Encoding sein

class SnomXML:
    def SnomIPPhoneLED(number="", state=""):
        header='''<SnomIPPhoneText>
            <Title>LED Control</Title>
            <Prompt>Prompt Text</Prompt>
            <Led number="%s">%s</Led>
            <Fetch mil="1000">snom://mb_exit</Fetch>''' % (number, state)
        footer='</SnomIPPhoneText>'
        content="<Text>LED %s: %s</Text>" % (number, state)
        return header + content + footer
    SnomIPPhoneLED=staticmethod(SnomIPPhoneLED)

    
    def SnomIPPhoneText(Text, Title="", Prompt=""):
        header='''<SnomIPPhoneText>
            <Title>%s</Title>
            <Prompt>%s</Prompt>''' % (Title, Prompt)
        footer='''<SoftKeyItem>
                    <Name>F1</Name>
                    <SoftKey>F_CANCEL</SoftKey>
                    </SoftKeyItem>
                    <SoftKeyItem>
                    <Name>F4</Name>
                    <Label>Exit</Label>
                    <URL>snom://mb_exit</URL>
                  </SoftKeyItem>                  
                </SnomIPPhoneMenu>'''
        content="<Text>%s</Text>" % Text
        return header + content + footer
    SnomIPPhoneText=staticmethod(SnomIPPhoneText)

    
    def SnomIPPhoneDirectory(Title="", Prompt="", DirectoryEntries=[]):
        header='''<SnomIPPhoneDirectory>
            <Title>%s</Title>
            <Prompt>%s</Prompt>''' % (Title, Prompt)
        footer='</SnomIPPhoneDirectory>'
        content=""
        for i in DirectoryEntries:
            content+='''<DirectoryEntry>
            <Name>%s</Name>
            <Telephone>%s</Telephone>
            </DirectoryEntry>''' % i
        return header + content + footer
    SnomIPPhoneDirectory=staticmethod(SnomIPPhoneDirectory)

    
    def SnomIPPhoneMenu(Title="", MenuItems=[]):
        header='''<SnomIPPhoneMenu>
            <Title>%s</Title>''' % (Title)
        footer='''<SoftKeyItem>
                    <Name>F1</Name>
                    <SoftKey>F_CANCEL</SoftKey>
                    </SoftKeyItem>
                    <SoftKeyItem>
                    <Name>F4</Name>
                    <Label>Exit</Label>
                    <URL>snom://mb_exit</URL>
                  </SoftKeyItem>                  
                </SnomIPPhoneMenu>'''
        content=""
        for i in MenuItems:
            content+='''<MenuItem>
            <Name>%s</Name>
            <URL>%s</URL>
            </MenuItem>''' % i
        return header + content + footer
    SnomIPPhoneMenu=staticmethod(SnomIPPhoneMenu)

    
    def SnomIPPhoneMenuIcon(Title="", MenuItems=[]):
        # <Icon>http://192.168.1.133/light-on.png</Icon>
                    # <SoftKey>F_CANCEL</SoftKey>
        header='''<SnomIPPhoneMenu>
            <Title>%s</Title>''' % (Title)
        footer='''<SoftKeyItem>
                    <Name>F1</Name>
                    <SoftKey>F_CANCEL</SoftKey>
                    </SoftKeyItem>
                    <SoftKeyItem>
                    <Name>F4</Name>
                    <Label>Exit</Label>
                    <URL>snom://mb_exit</URL>
                  </SoftKeyItem>                  
                </SnomIPPhoneMenu>'''
        content=""
        for i in MenuItems:
            # print(i) 
            content+='''
            <MenuItem><Icon>%s</Icon><Name>%s</Name><URL>%s</URL></MenuItem>''' % i
        return header + content + footer
    SnomIPPhoneMenuIcon=staticmethod(SnomIPPhoneMenuIcon)

    
    def SnomIPPhoneMenuIconLED(Title="", MenuItems=[]):
        # <Icon>http://192.168.1.133/light-on.png</Icon>
        header='''<SnomIPPhoneMenu track="yes">
            <Title>%s</Title>''' % (Title)
        footer='''<SoftKeyItem>
                    <Name>F1</Name>
                    <SoftKey>F_CANCEL</SoftKey>
                    </SoftKeyItem>
                    <SoftKeyItem>
                    <Name>F4</Name>
                    <Label>Exit</Label>
                    <URL>snom://mb_exit</URL>
                  </SoftKeyItem>                  
                </SnomIPPhoneMenu>'''
        content=""
        for i in MenuItems:
            print(i) 
            content+='''
            <Led number="%s" color="red">%s</Led>
            <MenuItem><Icon>%s</Icon><Name>%s</Name><URL>%s</URL></MenuItem>''' % i
        return header + content + footer
    SnomIPPhoneMenuIconLED=staticmethod(SnomIPPhoneMenuIconLED)

    
    def SnomIPPhoneInput(URL, QueryStringParam, Title="", Prompt="", DisplayName="", InputFlags="a"):
        content='''<SnomIPPhoneInput>
                   <Title>%s</Title>
                   <Prompt>%s</Prompt>
                   <URL>%s</URL>
                   <InputItem>
                   <DisplayName>%s</DisplayName>
                   <QueryStringParam>%s</QueryStringParam>
                   <DefaultValue/>
                   <InputFlags>%s</InputFlags>
                   </InputItem>
                   </SnomIPPhoneInput>''' % (Title, Prompt, URL, DisplayName, QueryStringParam, InputFlags)
        return content
    SnomIPPhoneInput=staticmethod(SnomIPPhoneInput)

    
    # <?xml version="1.0" encoding="UTF-8"?>
    # <SnomIPPhoneImageFile>
    # <LocationX>0</LocationX>
    # <LocationY>0</LocationY>
    # <URL>http://www.snom.com/minibrowser/snom320.bmp</URL>
    # </SnomIPPhoneImageFile>    
    def SnomIPPhoneImageFile(picture):
        header='''<SnomIPPhoneImageFile>
                  <LocationX>0</LocationX>
                  <LocationY>0</LocationY>
                  <URL>%s</URL>''' % (picture)
        footer='</SnomIPPhoneImageFile>'
        return header + footer
    SnomIPPhoneImageFile=staticmethod(SnomIPPhoneImageFile)
    # <URL>%s</URL><fetch mil="100">http://172.20.4.107:8083/webcam0</fetch>''' % (picture)

    
    # <SoftKeyItem>
     # <Name>5</Name>
      # <URL>http://www.snom.com/minibrowser/start.xml</URL>
    # </SoftKeyItem>    
    # def SoftKeyItem(name, url):
        # header='''<SoftKeyItem>
                  # <Name>%s</Name>
                  # <URL>%s</URL>''' % (name, url)
        # footer='</SoftKeyItem>'
        # return header + footer
    # SoftKeyItem=staticmethod(SoftKeyItem)

    # <SoftKeyItem>
     # <Name>F2</Name>
      # <Label>BACK</Label>
     # <Softkey>F_MINIBROWSER_BACK</Softkey>
    # </SoftKeyItem>
    def SoftKeyItem(name, url):
        header='''<SoftKeyItem>
                  <Name>%s</Name>
                  <Label>BACK</Label>
                  <Softkey>F_MINIBROWSER_BACK</Softkey>'''
        footer='</SoftKeyItem>'
        return header + footer
    SoftKeyItem=staticmethod(SoftKeyItem)
        
        
    def SnomIPHeader():
        return '<?xml version="1.0" encoding="UTF-8"?>\n'
    SnomIPHeader=staticmethod(SnomIPHeader)

