#!/usr/bin/python2.5.2
#-*- coding: utf8 -*-

from selenium import selenium

class SeleniumUtil:
  seleniums = {}
  
  def StartSeleniumForUrl(self, url):
    sel = selenium("172.30.123.132", 4444,"*chrome", url) #172.30.124.44
    sel.start()
    sel.set_timeout("90000")
    return sel

  def GetSelenium(self, websiteName, url):
    #if websiteName in self.seleniums:
     # return self.seleniums[websiteName]
    self.seleniums[websiteName] = self.StartSeleniumForUrl(url)
    return self.seleniums[websiteName]
  
  def StopSelenium(self, websiteName):
    if websiteName in self.seleniums:
      self.seleniums[websiteName].stop()
    
