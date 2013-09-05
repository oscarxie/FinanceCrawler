#!/usr/bin/python2.5.2
#-*- coding: utf8 -*-

import sys
import codecs


class FinanceAutomationResult:
  ###  Save / Load / Generate the result comparison ###
  
  def PrintListLine(self, file, values):
    isFirst = True
    for val in values:
      if isFirst:
        print >> file, ("%s" % val)
        isFirst = False
      else:
        print >> file, ("\t%s" % val)
    print >> file, '\r\n'
      
  def SaveAsSiteResults(self, results, siteList, criteriaList, tickerList, fileName):
    ### results[site][criteria][ticker] 
    ###  Save as "result_site.txt": 
    ### ticker   criteria1 criteria2 .. 
    ### ticker1    1        2
    ### ticker2    1        2
    ###
    for site in siteList:
      try:
        myfile=codecs.open(fileName % site, 'w', 'utf-8')
        criteriaList = results[site].keys()
        
        print >> myfile, "ticker\t"
        #print >> myfile, ("%s\t" % ticker)
        self.PrintListLine(myfile, criteriaList)
        
        for ticker in tickerList:
          values = []
          values.append(ticker)
          for criteria in criteriaList:
            if site in results and \
               criteria in results[site] and \
               ticker in results[site][criteria]:
              values.append(results[site][criteria][ticker])
            else:
              values.append("NA")
          self.PrintListLine(myfile, values)
        myfile.close()
        
      except IOError:
        print >> sys.stderr, "ERROR: writing " + fileName % site
        
        
  def SaveAsCriteriaResults(self, results, siteList, criteriaList, tickerList, fileName):
    ### results[site][criteria][ticker] 
    ### Save as "result_criteria.txt": 
    ### ticker   site1     site2  .. 
    ### ticker1    1        2
    ### ticker2    1        2
    ###
    for criteria in criteriaList:
      try:
        myfile=codecs.open(fileName % criteria, 'w', 'utf-8')
        
        print >> myfile, "ticker\t"
        self.PrintListLine(myfile, siteList)

        for ticker in tickerList:
          values = []
          values.append(ticker)
          for site in siteList:
            if site in results and \
               criteria in results[site] and \
               ticker in results[site][criteria]:
              values.append(results[site][criteria][ticker])
            else:
              values.append("NA")
          self.PrintListLine(myfile, values)

        myfile.close()

      except IOError:
        print >> sys.stderr, "ERROR: writing " + fileName % site

  def CompareResult(self, results, siteList,criteriaList, tickerList):
    
    for criteria in criteriaList:
        myfile=codecs.open("Compare/US/Compare_yahoo_%s.txt" %criteria,'w','utf-8')
                
        print >> myfile, "ticker\t"
        self.PrintListLine(myfile, siteList)
        
        for ticker in tickerList:
            values=[]
            try:
                if ticker not in results["Google"][criteria]:
                    results["Google"][criteria][ticker] = "NA"
                if ticker not in results["yahoo"][criteria]:
                    results["yahoo"][criteria][ticker] = "NA"
                    
                if results["Google"][criteria][ticker] != \
                      results["yahoo"][criteria][ticker]:
                    values.append(ticker)
                    print values
                    for site in siteList:    
                    #if results["Google"][criteria][ticker]=='--' or results["Google"][criteria][ticker]=='NA':
                     #   results["Google"][criteria][ticker]=0
                    #if results["Reuters"][criteria][ticker]=='--' or results["Reuters"][criteria][ticker]=='NA':
                     #   results["Reuters"][criteria][ticker]=0
                        #values.append(ticker)
                        values.append(results[site][criteria][ticker])                    
                        print values
                    self.PrintListLine(myfile, values)

            except Exception, err:
                print ticker, err
                continue
                #values.append(ticker)
                #values.append(results[site][criteria][ticker]) 
    print "Compare Done"
          