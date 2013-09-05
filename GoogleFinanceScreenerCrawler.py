#!/usr/bin/python2.5.2
#-*- coding: utf8 -*-

import time
import codecs
from SeleniumUtil import SeleniumUtil
from FinanceAutomationResult import FinanceAutomationResult
from CrawlSettings import CrawlSettings

PriceMap = {
  # put 万亿 before 亿/万
  r"万亿" : 1000000000000,
  r"亿" : 100000000,
  r"万" : 10000,
  r"B" : 1000000000,
  r"M" : 1000000,
  r"K" : 10000  
}
site = "Google"

debug=False

class GoogleFinanceScreenerCrawler:

  # get the company list when only add one criteria
  def GetResults(self, criteria, exchange, results):
    if site not in results:
      results[site] = {}
    each_page_number = 20
    endNo = 200
    roolUrl = "/finance/stockscreener"
    #roolUrl = "http://finance.google.com/finance/stockscreener"
    paramUrl = ("#c0=%s&region=us&exchange=%s" % #"?hl=zh-CN&gl=cn#c0=%s&region=cn&exchange=%s" % #
        (criteria, exchange))
    Url=roolUrl+paramUrl
    
    print "opening: ", roolUrl+paramUrl
    if not debug:
        sln = SeleniumUtil().GetSelenium("Google", "http://0.frontend-yiling_stockscreener-sfetest.sfe.scrooge.hs.borg.google.com/")#"http://0.frontend-canaryccn.sfe.scrooge.ug.borg.google.com:26103/") 
        sln.open(Url)
        time.sleep(10)
    
    page_index = 1
    googleResults = {}

    #print "opening: 2"

    for i in range(0, endNo):
      index = i % each_page_number

      tickerPath = ("//table[@class='results innermargin']/tbody/tr[%d]/td[2]/a"
              % (index + 2))
      valuePath = ("//table[@class='results innermargin']/tbody/tr[%d]/td[3]"
              % (index + 2))
      
      if not debug and sln.is_element_present(tickerPath):
        ticker=sln.get_text(tickerPath).strip().encode("utf-8")
        #print ticker
        #StockList=codecs.open(("Stock%s.txt",'a','utf-8') %criteria)
        #print >>("Stock%s.txt" %criteria),ticker
        value = sln.get_text(valuePath).strip().encode("utf-8")
        for key, scale in PriceMap.items():
          if value.endswith(key):
            value = float(value.replace(key, r"")) * float(scale)
            print " parse value: %s" % value
            break;
          
        googleResults[sln.get_text(tickerPath).strip()] = value
        
      else:
        googleResults["601398"] = "NA"
        break
      
      if index == each_page_number - 1:
        print "Got %s page %s companies." % (page_index, each_page_number)
        page_index=page_index+1
        if not debug:
            try:
                sln.click("//span[contains(text(),'Next')]")
                time.sleep(2)
            except:
                break            
      
    if not debug:
        sln.stop()
    #print googleResults
    results[site][criteria] = googleResults
    return googleResults
    

  def GetAllResults(self, criteriaList, results):
    for criteria in criteriaList:
      #GoogleFinanceScreenerCrawler().GetResults(criteria, "us", results)
    
      GoogleFinanceScreenerCrawler().GetResults(criteria, "NASDAQ", results)
    
      #GoogleFinanceScreenerCrawler().GetResults(criteria, "AMEX", results)
    
      #GoogleFinanceScreenerCrawler().GetResults(criteria, "NYSE", results)
      
      #GoogleFinanceScreenerCrawler().GetResults(criteria, "ALL_CN_A", results)
      
      #GoogleFinanceScreenerCrawler().GetResults(criteria, "SHA_A", results)
      
      #GoogleFinanceScreenerCrawler().GetResults(criteria, "SHA_B", results)
      
      #GoogleFinanceScreenerCrawler().GetResults(criteria, "SHE_A", results)
      
      #GoogleFinanceScreenerCrawler().GetResults(criteria, "SHE_B", results)
   
    
#criteriaList = ["MarketCap"]

#criteria=[]
#for criteria in criteriaList:
 #   print criteria
#GoogleFinanceScreenerCrawler().GetAllResults(criteriaList, results)
#print results

#print result



#allTickersList=[]
#for site,value in results.items():
#    for ticker,values in value.items():
#        allTickersList.append(ticker)
#print allTickersList
#print result
crawlProfile = CrawlSettings().GetCrawlProfile("test") 
criteriaList=crawlProfile["Criteria"] 
tickerFile = crawlProfile["TickerListFile"]
allTickersList= CrawlSettings().LoadTickerList(tickerFile)
resultFiles = crawlProfile["ResultFiles"]

#GoogleFinanceScreenerCrawler().GetAllResults(criteriaList, results)
#allTickersList=["600456","000690"]
#FinanceAutomationResult().SaveAsCriteriaResults(result, ["Google"], criteriaList,allTickersList,resultFiles)
#FinanceAutomationResult().SaveAsSiteResults(result, ["Google"], criteriaList, allTickersList, resultFiles)




