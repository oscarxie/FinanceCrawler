#!/usr/bin/python2.5.2
#-*- coding: utf8 -*-

#import os
import sys
import re
import codecs

from SeleniumUtil import SeleniumUtil 
from CrawlSettings import CrawlSettings
from FinanceAutomationResult import FinanceAutomationResult
from GoogleFinanceScreenerCrawler import GoogleFinanceScreenerCrawler

debug = False

class FinanceAutomationCrawler:
  ### Crawl the data according the configurations, such as:
  ###   "Sites" : ["baidu"],
  ###   "Criteria" : ["PE", "EPS", "FLOAT"],
  ###   "TickerListFile" : "tickerList.txt",
  ###   "ResultFiles" : "result_%s.txt",
  ###   "NumTickerPerSite" : "2"
  ### 
  ### Crawling process:
  ###   ProcessSchedule => ProcessSite => ProcessPage => Preprocess + PostProcess
  ###
  
  # pass in the string value and process it to corresponding value(double)
  def PostProcess(self, value, postProcessProfile):
    if postProcessProfile == None:
      return value
    
    if debug: print "-------Post process profile: ", postProcessProfile

    try:
      # first replace, then remove, last multiple
      if "ReplaceReg" in postProcessProfile:
        if debug: print "..........ReplaceReg", value
        
        value = re.sub(postProcessProfile["ReplaceReg"][0],
                       postProcessProfile["ReplaceReg"][1],
                       value)
      
      if "RemoveString" in postProcessProfile:
        if debug: print "..........RemoveString", value
        
        for str in postProcessProfile["RemoveString"]:
          value = value.replace(str, "")
      
      if "Multiple" in postProcessProfile:
        if debug: print "..........Multiple", value
        
        value = float(value) * float(postProcessProfile["Multiple"])

    except Exception, ex:
      print >> sys.stderr, ("ERROR: Post-process %s on %s: %s" %
                      (value, postProcessProfile, ex))
                      
    if debug: print "-------Post process result: ", value
    return value

  
  def GetPostProcessProfile(self, pageProfile, criteria):
    if "PostProcess" in pageProfile:
      if criteria in pageProfile["PostProcess"]:
        return pageProfile["PostProcess"][criteria]
      elif "all" in pageProfile["PostProcess"]:
        return pageProfile["PostProcess"]["all"]
    return None
  
  def ProcessPage(self, selen, pageName, tickerList, criteriaList, siteResults):
    #get base link of the page:

    setting = CrawlSettings()
    page = setting.GetPageProfile(pageName)
    linkSetting = page["Link"]

    # check whether there are settings for the criteria in this page profile
    hasCriteria = False
    for criteria in criteriaList:
      if criteria in page["Pattern"]:
        hasCriteria = True
        break
    if not hasCriteria:
      return
    
    for ticker in tickerList:
      print "---- criteria %s for ticker: %s" % (criteriaList, ticker)
      stockType = setting.GetStockType(ticker)
      if setting.GetStockType(ticker) in linkSetting:
        link = linkSetting[setting.GetStockType(ticker)] % ticker
      elif "all" in linkSetting:
        link = linkSetting["all"] % ticker
      else:
        print "Skip link for ticker: %s, type: %s" % (ticker, stockType)
        continue

      if not debug: 
        try:
          selen.open(link)
        except Exception, ex:
          print >> sys.stderr, ("ERROR: Selenium open link %s: %s" %
              (link, ex))
      
      # open the page and get all criteria
      for criteria, pattern in page["Pattern"].items():
        if criteria not in criteriaList:
          continue
          
        print ("------ %s, link: %s, pattern: %s" % (criteria, link, pattern.encode('utf-8')))

        try:
          if debug:
            content = u"111" #元"
            content = content.encode("utf-8")
          else:
            content = selen.get_text(pattern).encode("utf-8")
            print ("------ %s" % content)

          if criteria not in siteResults:
            siteResults[criteria] = {}
          siteResults[criteria][ticker] = \
              self.PostProcess(content, \
                               self.GetPostProcessProfile(page, criteria))

        except Exception, err:
          print >> sys.stderr, ("ERROR: crawling %s on %s for %s of %s: %s" % (pattern, link, criteria, ticker, err))


  def ProcessSite(self, site, tickerList, criteriaList, siteResults):
    print ("+ processing site: %s" % site)
    siteProfile = CrawlSettings().GetSiteProfile(site)
    if siteProfile != None:
      baseLink = siteProfile["BaseLink"]
      pages = siteProfile["PageProfileNames"]
      
      if debug:
        sln = None
      else:
        sln = SeleniumUtil().GetSelenium(site, baseLink)

      for page in pages:
        print ("-- page: %s" % page)
        self.ProcessPage(sln, page, tickerList, criteriaList, siteResults)

      if not debug:
        SeleniumUtil().StopSelenium(site)

  def ProcessSchedule(self, taskName, results):
    crawlProfile = CrawlSettings().GetCrawlProfile(taskName)    
    if crawlProfile == None:
      print "No setting for profile: %s" % taskName
      return
     
    numTickerPerSite = int(crawlProfile["NumTickerPerSite"])
    criteriaList = crawlProfile["Criteria"]
    tickerFile = crawlProfile["TickerListFile"]
    sitesList = crawlProfile["Sites"]
    resultFiles = crawlProfile["ResultFiles"]
    allTickersList = CrawlSettings().LoadTickerList(tickerFile)
    
    tickerslist = []
    i = 0
    for ticker in allTickersList:
      tickerslist.append(ticker)
      i = i + 1
      if i == numTickerPerSite:
        for site in sitesList:
          siteResults = {}
          self.ProcessSite(site, tickerslist, criteriaList, siteResults)
          results[site] = siteResults
        i = 0
        tickerslist = []
    #FinanceAutomationResult().SaveAsCriteriaResults(
     #   results, sitesList, criteriaList, allTickersList, resultFiles)
    #FinanceAutomationResult().SaveAsSiteResults(
     #   results, sitesList, criteriaList, allTickersList, resultFiles)
    #return results

def main():
  results = {}
  crawlProfile = CrawlSettings().GetCrawlProfile("test")    
  numTickerPerSite = int(crawlProfile["NumTickerPerSite"])
  criteriaList = crawlProfile["Criteria"]
  tickerFile = crawlProfile["TickerListFile"]
  sitesList = crawlProfile["Sites"]
  sitesList.append("Google")
  resultFiles = crawlProfile["ResultFiles"]
  allTickersList = CrawlSettings().LoadTickerList(tickerFile)
  
  
  FinanceAutomationCrawler().ProcessSchedule("test", results)
  GoogleFinanceScreenerCrawler().GetAllResults(criteriaList, results)
  FinanceAutomationResult().SaveAsCriteriaResults(
    results, sitesList, criteriaList, allTickersList, resultFiles)
  #FinanceAutomationResult().SaveAsSiteResults(
   # results, sitesList, criteriaList, allTickersList, resultFiles)

  FinanceAutomationResult().CompareResult(results,sitesList,criteriaList,allTickersList)
                
  print "!!!DONE!!!"


if __name__ == "__main__":
  try:
    #app.run()
    main()
  except KeyboardInterrupt:
    sys.exit(1)
