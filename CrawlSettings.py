#!/usr/bin/python2.5.2
#-*- coding: utf8 -*-

import codecs

# QuoteLast ==> latest Price
# CashPerShareYear / BookValuePerShareYear
#"High52Week":"N/A",
#"Low52Week":"N/A",
#"DividendPerShare":"N/A",
#"DPSRecentYear":"N/A",
#"CurrentRatioYear":"CurrentAssets"/"CurrentLiabilities",
#"Float", "PE", "MarketCap", "EPS", "PriceClose", "QuoteLast", "BookValuePerShareYear", 
#"CurrentRatioYear", "NetProfitMarginPercent", "GrossMargin", "CashPerShareYear", 
#"DividentPerShare", "High52Week", "Low52Week","Volume"
#"Financial Ratios","Operating Metrics"
#"LT Debt to Equity (MRQ)","Total Debt to Equity (MRQ)","Interest Coverage (TTM)","Return on Assets (TTM)","Return on Assets - 5 Yr. Avg.","Return on Investment (TTM)"
#"Return on Investment - 5 Yr. Avg.","Return on Equity (TTM)","Return on Equity - 5 Yr. Avg."
#LT Debt to Equity (MRQ)          	    LTDebtToEquityQuarter
#Total Debt to Equity (MRQ)			    TotalDebtToEquityQuarter
#Interest Coverage (TTM) 			    AINTCOV
#Return on Assets (TTM)  			    ReturnOnAssetsTTM
#Return on Assets - 5 Yr. Avg. 		    ReturnOnAssets5Years
#Return on Investment (TTM) 			ReturnOnInvestmentTTM
#Return on Investment - 5 Yr. Avg. 	    ReturnOnInvestment5Years
#Return on Equity (TTM) 				ReturnOnEquityTTM
#Return on Equity - 5 Yr. Avg. 		    ReturnOnEquity5Years
#"Price50DayAverage","Price150DayAverage","Price200DayAverage","Price4WeekPercChange","Price13WeekPercChange","Price26WeekPercChange","LTDebtToAssetsYear",
#"LTDebtToAssetsQuarter","TotalDebtToAssetsYear","TotalDebtToAssetsQuarter","LTDebtToEquityYear","TotalDebtToEquityYear","ReturnOnInvestmentYear","ReturnOnAssetsYear","ReturnOnEquityYear"
 




# page setting for multiple websites for data comparison.
# the format is sites ====each===> multi-links ====each===> multi-patterns


PageProfiles = (
  {
    "Name" : "baidu",
    "Link" : {
      # ticker type mapping to link, default "all"
      "sz" : "http://stock.baidu.com/cn/q.php?code=%s.sz",
      "sh" : "http://stock.baidu.com/cn/q.php?code=%s.sh",
    },
    "Pattern" : {
      "BookValuePerShareYear" : "//div[@id='dlCon']/div[1]/div[5]/table/tbody/tr[3]/td[4]",
      "QuoteLast" : "//div[@id='stockName']/table/tbody/tr/td[2]/span[1]",
      "PriceClose" : "//div[@id='stockName']/table/tbody/tr/td[3]/span[1]",
      "EPS" : "//div[@id='dlCon']/div[1]/div[5]/table/tbody/tr[3]/td[2]",
      "MarketCap" : "//div[@id='stockName']/table/tbody/tr/td[3]/span[9]",
      "PE" : "//div[@id='stockName']/table/tbody/tr/td[3]/span[7]",
      "CashPerShareYear":"//div[@id='dlCon']/div[1]/div[5]/table/tbody/tr[4]/td[2]",	
      "Float":"//div[@id='dlCon']/div[1]/div[5]/table/tbody/tr[2]/td[4]",
      "Volume":"//div[@id='stockName']/table/tbody/tr/td[3]/span[3]",
    },
    "PostProcess" : {
      "all" : {
        "RemoveString" : [r",", r"%", r"元"]
      },
      "BookValuePerShareYear" : {
        "ReplaceReg" : [r'(.*?)([\d\.,]+)元', r'\2'],
      },
      "MarketCap" : {
        "ReplaceReg" : [r'(.*?)([\d\.,]+)亿元', r'\2'],
        "Multiple" : 100000000
      },
      #"Price2Book":"QuoteLast"/"BookValuePerShareYear",
      "Float" : {
        "Multiple" : 10000
      },
     "Volume" : {
        "RemoveString" : [r","],
        "Multiple" : 100
      }
    }    
  },
  {
      "Name" : "Reuters",
      "Link" : {
        # ticker type mapping to link, default "all"
        "sz" : "http://www.reuters.com/finance/stocks/overview?symbol=%s.SZ",
        "sh" : "http://www.reuters.com/finance/stocks/overview?symbol=%s.SS",
        "all":"http://www.reuters.com/finance/stocks/overview?symbol=%s.O",#NASDAQ
        #"all":"http://www.reuters.com/finance/stocks/overview?symbol=%s.A",#AMEX
        #"all":"http://www.reuters.com/finance/stocks/overview?symbol=%s.N",#NYSE
      },
      "Pattern" : {
        #"BookValuePerShareYear" : "",
        "QuoteLast" : "//div[@id='priceQuote']/div[2]/span[1]",
        "PriceClose" : "//div[@id='quoteDetail']/div[1]/div[2]/span",
        "EPS" : "//div[@id='quoteDetail']/div[2]/div[5]/span",
        "MarketCap" : "//div[@id='quoteDetail']/div[2]/div[3]/span",
        "High52Week":"//div[@id='quoteDetail']/div[1]/div[5]/span",
        "Low52Week":"//div[@id='quoteDetail']/div[1]/div[6]/span",
        "PE" : "//div[@id='maincontent']/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/table/tbody/tr[2]/td[2]",
        #"CashPerShareYear":"",	
        #"Float":"",
        "Volume":"//div[@id='quoteDetail']/div[2]/div[1]/span",
      },
      "PostProcess" : {
        "all" : {
          "RemoveString" : [r",", r"%", r"元",r"¥"]#,r"楼"]
        },
       "Volume" : {
          "RemoveString" : [r","],
          "ReplaceReg" : [r'(.*?)([\d\.,]+)M', r'\2'],
          "Multiple" : 1000000
        }
      }    
  },
  {
      "Name" : "Reuters_Ratios",
      "Link" : {
        # ticker type mapping to link, default "all"
        "sz" : "http://www.reuters.com/finance/stocks/ratios?symbol=%s.SZ",
        "sh" : "http://www.reuters.com/finance/stocks/ratios?symbol=%s.SS",
        "all":"http://www.reuters.com/finance/stocks/ratios?symbol=%s.O",#NASDAQ
        #"all":"http://www.reuters.com/finance/stocks/ratios?symbol=%s.A",#AMEX
        #"all":"http://www.reuters.com/finance/stocks/ratios?symbol=%s.N",#NYSE
      },
      "Pattern" : {
        #"BookValuePerShareYear" : "",
        #"PE" : "",
        "PriceToBook":"//div[@id='maincontent']/div[2]/div[2]/div[1]/div[7]/div/div/div[2]/table/tbody[2]/tr[8]/td[2]",
        #"CashPerShareYear":"",	
        #"Float":"",
        "LTDebtToEquityQuarter":"//div[@id='maincontent']/div[2]/div[2]/div[1]/div[10]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]",
        "TotalDebtToEquityQuarter":"//div[@id='maincontent']/div[2]/div[2]/div[1]/div[10]/div/div/div[2]/table/tbody[2]/tr[4]/td[2]",
        "AINTCOV":"//div[@id='maincontent']/div[2]/div[2]/div[1]/div[10]/div/div/div[2]/table/tbody[2]/tr[5]/td[2]",
        "ReturnOnAssetsTTM":"//div[@id='maincontent']/div[2]/div[2]/div[1]/div[12]/div/div/div[2]/table/tbody[2]/tr[1]/td[2]",
        "ReturnOnAssets5Years":"//div[@id='maincontent']/div[2]/div[2]/div[1]/div[12]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]",
        "ReturnOnInvestmentTTM":"//div[@id='maincontent']/div[2]/div[2]/div[1]/div[12]/div/div/div[2]/table/tbody[2]/tr[4]/td[2]",
        "ReturnOnInvestment5Years":"//div[@id='maincontent']/div[2]/div[2]/div[1]/div[12]/div/div/div[2]/table/tbody[2]/tr[5]/td[2]",
        "ReturnOnEquityTTM":"//div[@id='maincontent']/div[2]/div[2]/div[1]/div[12]/div/div/div[2]/table/tbody[2]/tr[7]/td[2]",
        "ReturnOnEquity5Years" :"//div[@id='maincontent']/div[2]/div[2]/div[1]/div[12]/div/div/div[2]/table/tbody[2]/tr[8]/td[2]"
      },
      "PostProcess" : {
        "all" : {
          "RemoveString" : [r",", r"%", r"元",r"¥"]
        }
      }    
  },
  {
    "Name" : "Google_Finance",
    "Link" : {
      # ticker type mapping to link, default "all"
      "sz" : "http://finance.google.cn/finance?q=SHE:%s&client=ft",
      "sh" : "http://finance.google.cn/finance?q=SHA:%s&client=ft",
      "all":"http://finance.google.cn/finance?q=%s",
    },
    "Pattern" : {
      "MarketCap" : "id('ref_694653_mc')",
      "PE" : "id('ref_694653_pe')",

    },
    "PostProcess" : {
      "all" : {
        "RemoveString" : [r",", r"%", r"元",r"¥"]
      }
    }    
  },
  {
    "Name" : "baidu_other",
    "Link" : {
      #Criteria:CurrentRatioYear,NetProfitMarginPercent,GrossMargin
      "sz":"http://stock.baidu.com/cn/fa.php?code=%s.sz",
      "sh":"http://stock.baidu.com/cn/fa.php?code=%s.sh",
    },
    "Pattern" : {
      #"CurrentRatioYear":"CurrentAssets"/"CurrentLiabilities",
      #"CurrentAssets":"//table[@id='itprofile']/tbody/tr[23]/td[2]",
      #!"CurrentLiabilities":"//table[@id='itprofile']/tbody/tr[24]/td[2]",
            
      #"Profit":"//table[@id='itprofile']/tbody/tr[19]/td[2]",
      #"Income":"//table[@id='itprofile']/tbody/tr[13]/td[2]",
      #!"NetProfitMarginPercent":"Profit"/"Income",
      
      #"Gross":"//table[@id='itprofile']/tbody/tr[14]/td[2]",
      #!"GrossMargin":"Gross"/"Income",
    },
    "PostProcess" : {
      "all" : {
        "RemoveString" : [r",", r"%", r"元"]
      }
    }
  },
  {
    "Name" : "sina",
    "Link" : {
      "sz" : "http://finance.sina.com.cn/realstock/company/sz%s/nc.shtml",
      "sh" : "http://finance.sina.com.cn/realstock/company/sh%s/nc.shtml",
    },
    "Pattern" : {
      "PriceClose" : "//span[@id='itemPrevious2']",
      "QuoteLast" : "//h3[@id='itemCurrent']",
      "BookValuePerShareYear":"//td[@id='cwjk_mgjzc']",
      "EPS" : "//td[@id='cwjk_mgsy']",
      "MarketCap" :"//span[@id='totalMart2']",
      "PE" :"//td[@id='pe_ratio_lyr']",
      "Float":"//div[@id='con04-0']/table/tbody/tr[4]/td[2]",
      "CashPerShareYear" : "//div[@id='con04-0']/table/tbody/tr[2]/td[1]",
      "Volume":"//span[@id='itemVolume2']",
    },
    "PostProcess" : {
      "all" : {
        "RemoveString" : [r",", r"%", r"元"]
      },
      "MarketCap" : {
        "ReplaceReg" : [r'(.*?)([\d\.,]+)亿元', r'\2'],
        "Multiple" : 100000000
      },
      "Float" : {
        "ReplaceReg" : [r'(.*?)([\d\.,]+)万股', r'\2'],
        "Multiple" : 10000
      },
      "Volume" : {
        "Multiple" : 100
          }
    
      #"Price2Book":"QuoteLast"/"BookValuePerShareYear",
    }
  },
   {
    "Name" : "sina_DPSRecentYear",
    "Link" : {
      "all":"http://money.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/%s.phtml"
    },
    "Pattern" : {
      "DPSRecentYear" : "//table[@id='sharebonus_1']/tbody/tr[contains(.,'2008-')]/td[4]",	  
    },
    "PostProcess" : {
      "DPSRecentYear" : {
        "Multiple" : 0.1
      }
    }    
  },
  {
    "Name" : "sina_other",
    "Link" : {
      "all" : "http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/%s/displaytype/4.phtml"
    },
    "Pattern" : {
      "CurrentRatioYear" : "//table[@id='BalanceSheetNewTable0']/tbody/tr[21]/td[2]",
      "NetProfitMarginPercent" : "//table[@id='BalanceSheetNewTable0']/tbody/tr[42]/td[2]",
      # TODO: check if it is the same with the sina ones 经营毛利率(%) OperatingMargin
      "GrossMargin" : "//table[@id='BalanceSheetNewTable0']/tbody/tr[39]/td[2]",
      #"资产负债率(%)":"//table[@id='BalanceSheetNewTable0']/tbody/tr[60]/td[2]",
      #"长期负债资产比(%)":"//table[@id='BalanceSheetNewTable0']/tbody/tr[61]/td[2]",
      #"负债权益比(%)":"//table[@id='BalanceSheetNewTable0']/tbody/tr[26]/td[2]",
    }
  },
  {
    "Name" : "yahoo_special",
    "Link" : {
      "sz" : "http://finance.cn.yahoo.com/fin/finance_cngegu0710_more_zysjtj.html?s=%s.sz",
      "sh" : "http://finance.cn.yahoo.com/fin/finance_cngegu0710_more_zysjtj.html?s=%s.ss",
    },
    "Pattern" : {
      "MarketCap" : "//div[@id='line_img']/div[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]",
      "CashPerShareYear" : "//div[@id='line_img']/div[2]/table/tbody/tr/td[1]/table/tbody/tr[12]/td[2]",
      "High52Week" : "//div[@id='line_img']/div[2]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]",
      "Low52Week" : "//div[@id='line_img']/div[2]/table/tbody/tr/td[2]/table/tbody/tr[3]/td[2]",
    },
    "PostProcess" : {
      "all" : {
        "RemoveString" : [r",", r"%"]
      },
      "MarketCap" : {
        "RemoveString" : [r","],
        "Multiple" : 10000
      }
    }
  },
  {
    "Name" : "yahoo_normal",
    "Link" : {
      "sz" : "http://finance.cn.yahoo.com/q?s=%s.sz",
      "sh" : "http://finance.cn.yahoo.com/q?s=%s.ss",
    },
    "Pattern" : {
      "PriceClose" : "//ul[@id='price_ul']/li[6]/cite",
      "BookValuePerShareYear" : "//div[@id='important_data']/div[2]/ul/li[4]/cite",
      "QuoteLast":"//cite[@id='new_price']",
      #"Price2Book":"QuoteLast"/"BookValuePerShareYear",
      "EPS":"//div[@id='important_data']/div[2]/ul/li[3]/cite",
      "PE" : "//div[@id='important_data']/div[2]/ul/li[6]",
      "Float" : "//div[@id='important_data']/div[2]/ul/li[2]",
      "Volume" : "//ul[@id='price_ul']/li[4]/cite",
    },
    "PostProcess" : {
      "all" : {
        "RemoveString" : [r",", r"%", r"元", r"倍"]
      },
      "PE" : {
        "ReplaceReg" : [r'(.*?)([\d\.,]+)倍', r'\2'],
      },
      "Float" : {
        "ReplaceReg" : [r'(.*?)([\d\.,]+)万股', r'\2'],
        "RemoveString" : [r","],
        "Multiple" : 10000,
      },
      "Volume" : {
        "ReplaceReg" : [r'(.*?)([\d\.,]+)\(手\)', r'\2'],
        "RemoveString" : [r","],
        "Multiple" : 100
      }      
    }
  },
  {
    "Name" : "yahoo_DPSRecentYear",
    "Link" : {
      "sz" : "http://finance.cn.yahoo.com/fin/finance_cngegu0710_more_fhsg.html?s=%s.sz",
      "sh" : "http://finance.cn.yahoo.com/fin/finance_cngegu0710_more_fhsg.html?s=%s.ss",
    },
    "Pattern" : {
      # Note: div per 10 shares
      "DPSRecentYear" : u"//div[@id='line_img']/div[2]/table/tbody/tr/td/table/tbody/tr[contains(.,'2008')]/td[3]"
    },
    "PostProcess" : {
      "DPSRecentYear" : {
        "Multiple" : 0.1
      }
    }
  },
	{
	"Name" : "yahoo_Other",
    "Link" : {
	#Criteria:CurrentRatioYear,NetProfitMarginPercentPercent,GrossMargin
      "sz" : "http://finance.cn.yahoo.com/fin/finance_cngegu0710_more_cwzb.html?s=%s.sz",
      "sh" :"http://finance.cn.yahoo.com/fin/finance_cngegu0710_more_cwzb.html?s=%s.ss",
	 },
    "Pattern" : {
	  #Criteria 6
      "CurrentAssets":"//div[@id='line_img']/div[2]/table/tbody/tr/td/table[3]/tbody/tr[22]/td[2]",
      "CurrentLiabilities":"//div[@id='line_img']/div[2]/table/tbody/tr/td/table[3]/tbody/tr[23]/td[2]",
      #"CurrentRatioYear":"CurrentAssets"/"CurrentLiabilities",
      "Profit":"//div[@id='line_img']/div[2]/table/tbody/tr/td/table[3]/tbody/tr[18]/td[2]",
      "Income":"//div[@id='line_img']/div[2]/table/tbody/tr/td/table[3]/tbody/tr[12]/td[2]",
      #"NetProfitMarginPercent":"Profit"/"Income",
      "Gross":"//div[@id='line_img']/div[2]/table/tbody/tr/td/table[3]/tbody/tr[13]/td[2]",
      #"GrossMargin":"Gross"/"Income"
	 },
  },
  {
    "Name" : "yahoo_com",
    "Link" : {#Criteria:Return on Assets (ttm),Return on Equity (ttm),Total Debt/Equity (mrq)
      "all" : "http://finance.yahoo.com/q/ks?s=%s"
    },
    "Pattern" : {
      "ReturnOnAssetsTTM":"//table[@id='yfncsumtab']/tbody/tr[2]/td[1]/table[12]/tbody/tr/td/table/tbody/tr[2]/td[2]",
      "ReturnOnEquityTTM":"//table[@id='yfncsumtab']/tbody/tr[2]/td[1]/table[12]/tbody/tr/td/table/tbody/tr[3]/td[2]",
      "TotalDebtToEquityQuarter":"//table[@id='yfncsumtab']/tbody/tr[2]/td[1]/table[16]/tbody/tr/td/table/tbody/tr[5]/td[2]",
    },
    "PostProcess" : {
            "all" : {
              "RemoveString" : [r",", r"%", r"元",r"¥"]
            },
            "TotalDebtToEquityQuarter":{
              "Multiple" : 100 
            }          
    }   
    
  }  
)

SiteProfiles = {
  "baidu" : {  # website name
    "BaseLink" : "http://finance.baidu.com",
    "PageProfileNames" : ["baidu","baidu_other"]
  },
  "sina" : {
    "BaseLink" : "http://finance.sina.com.cn",
    "PageProfileNames" : ["sina","sina_DPSRecentYear","sina_other"]
  },
  "yahoo" : {
    "BaseLink" : "http://finance.cn.yahoo.com",
    "PageProfileNames" : ["yahoo_special", "yahoo_normal", "yahoo_DPSRecentYear","yahoo_Other","yahoo_com"]
  },
  "Reuters":{
    "BaseLink" :"http://www.reuters.com/finance/stocks",
    "PageProfileNames" :["Reuters","Reuters_Ratios"]
  }
}

CrawlProfiles = {
  "test_baidu_normal_page" : {
    "Sites" : ["baidu"], #, "yahoo", "sina"],
    "Criteria" : ["Float",  "QuoteLast", "CashPerShareYear", "PE", "MarketCap", "EPS", "PriceClose","BookValuePerShareYear"],
     #,"PE", "EPS", "Float","MarketCap"
    "TickerListFile" : "tickerList.txt",
    "ResultFiles" : "result_%s.txt",
    "NumTickerPerSite" : "2"
  },
  "test_sina_normal_page" : {
    "Sites" : ["sina"],
    "Criteria" : ["Float", "PE", "MarketCap", "EPS", "PriceClose", "QuoteLast", "BookValuePerShareYear", "CashPerShareYear"],
    "TickerListFile" : "tickerList.txt",
    "ResultFiles" : "result_%s.txt",
    "NumTickerPerSite" : "2"
  },
  "test_sina_another_page" : {
    "Sites" : ["sina"],
    "Criteria" : ["CurrentRatioYear", "NetProfitMarginPercent", "GrossMargin"],
    "TickerListFile" : "tickerList.txt",
    "ResultFiles" : "result_%s.txt",
    "NumTickerPerSite" : "2"
  },
  "test_sina_DPSRecentYear" : {
    "Sites" : ["sina"],
    "Criteria" : ["DPSRecentYear"],
    "TickerListFile" : "tickerList.txt",
    "ResultFiles" : "result_%s.txt",
    "NumTickerPerSite" : "2"
  },
  "test_yahoo_DPSRecentYear" : {
    "Sites" : ["yahoo"],
    "Criteria" : ["DPSRecentYear"],
    "TickerListFile" : "tickerList.txt",
    "ResultFiles" : "result_%s.txt",
    "NumTickerPerSite" : "2"
  },
  "test_yahoo_normal" : {
    "Sites" : ["yahoo"],
    "Criteria" : ["PriceClose", "BookValuePerShareYear", "CurrentRatioYear",
                  "CashPerShareYear", "High52Week", "Low52Week", "PE", "EPS", 
                  "MarketCap", "Float"],  
    "TickerListFile" : "tickerList.txt",
    "ResultFiles" : "result_%s.txt",
    "NumTickerPerSite" : "2"
  },
  "test_" : {
      "Sites" : ["baidu","sina","yahoo"],
      "Criteria" : ["MarketCap"],#["Float", "PE", "MarketCap", "EPS", "PriceClose", "QuoteLast", "BookValuePerShareYear", 
                    #"CurrentRatioYear", "NetProfitMarginPercent", "GrossMargin", "CashPerShareYear", 
                    #"DPSRecentYear", "High52Week", "Low52Week","Volume"],  
      "TickerListFile" : "tickerList.txt",
      "ResultFiles" : "result_%s.txt",
      "NumTickerPerSite" : "20"
    },
  "test_realtime" : {
      "Sites" : ["baidu","sina","yahoo"],
      "Criteria" : ["PE", "MarketCap", "PriceClose", "QuoteLast","High52Week", "Low52Week","Volume"],  
      "TickerListFile" : "tickerList.txt",
      "ResultFiles" : "result_%s.txt",
      "NumTickerPerSite" : "20"
    },  
  "test_notrealtime" : {
      "Sites" : ["baidu","sina","yahoo"],
      "Criteria" : ["Float","BookValuePerShareYear","EPS", "CurrentRatioYear", "NetProfitMarginPercent", "GrossMargin", 
                    "CashPerShareYear","DPSRecentYear",],  
      "TickerListFile" : "tickerList.txt",
      "ResultFiles" : "result_%s.txt",
      "NumTickerPerSite" : "20"
    },
  "test__" : {
      "Sites" : ["baidu","sina","yahoo","Reuters"],#
      "Criteria" : ["Volume","QuoteLast","PriceClose","EPS","MarketCap","High52Week","Low52Week","PE","PriceToBook",
                    "LTDebtToEquityQuarter","TotalDebtToEquityQuarter","AINTCOV","ReturnOnAssetsTTM","ReturnOnAssets5Years",
                    "ReturnOnInvestmentTTM","ReturnOnInvestment5Years","ReturnOnEquityTTM","ReturnOnEquity5Years"],  
      "TickerListFile" : "tickerList.txt",
      "ResultFiles" : "result_%s.txt",
      "NumTickerPerSite" : "20"
    },
  "test_Reuters" : {
      "Sites" : ["Reuters"],#
      "Criteria" : ["AINTCOV"],
                    #[#"Volume","QuoteLast","PriceClose","EPS","MarketCap","High52Week","Low52Week","PE","PriceToBook",
                    #"LTDebtToEquityQuarter"],#"TotalDebtToEquityQuarter","AINTCOV","ReturnOnAssetsTTM","ReturnOnAssets5Years",
                    #"ReturnOnInvestmentTTM","ReturnOnInvestment5Years","ReturnOnEquityTTM","ReturnOnEquity5Years"],  
      "TickerListFile" : "Ticker/US/ticker_AMEX_AINTCOV.txt",
      "ResultFiles" : "Result/US/Result_AMEX_%s.txt",
      "NumTickerPerSite" : "100"
    },    
  "test" : {
    "Sites" : ["yahoo"],#_yahoo.com
    "Criteria" : ["TotalDebtToEquityQuarter"],#["ReturnOnAssetsTTM","ReturnOnEquityTTM","TotalDebtToEquityQuarter"],
    "TickerListFile" : "ticker_NASDAQ_TotalDebtToEquityQuarter.txt",
    "ResultFiles" : "result_Yahoo_%s.txt",
    "NumTickerPerSite" : "100"
  },
  "test_yahoo_Reuters" : {
    "Sites" : ["yahoo","Reuters"],#
    "Criteria" : ["ReturnOnAssetsTTM","ReturnOnEquityTTM","TotalDebtToEquityQuarter"],
    "TickerListFile" : "tickerList1.txt",
    "ResultFiles" : "result_%s.txt",
    "NumTickerPerSite" : "20"
  }
}

ExchangesProfiles={	
	"UK":"LON",
    "HongKong":"HKG",
	"Canada":["CVE","TSE"],
	"France":"EPA",
	"Italy":["ISE","BIT"],
	"TaiWan":"TPE",
	# "China Mainland":["SHA","SHE"],	
	"US":["AMEX","NASDAQ","NYSE"],	
	# "Japan":["TGE","OSE","NSE","TSE"],
	# "Korea":"KSE",	
	# "Singapore":["SES","SIMEX"]	
	# "South Africa":["JSE","SAFEX"],
	# "Australia":["SFE","ASX"],
	# "India":["NSE","BSE"],
	# "Germany":"FSE",
	# "Brazil":"SPSE",
	# "BE":"EBR",
	# "IN":"BOM",
	# "IT":"BIT",
	# "NL":"AMS",
	# "NZ":"NZE",
	# "PT":"ELI"
}

class CrawlSettings:
  
  def GetCrawlProfile(self, name):
    if name in CrawlProfiles:
      return CrawlProfiles[name]
    return None
  
  def GetSiteProfile(self, name):
    if name in SiteProfiles:
      return SiteProfiles[name]
    return None
  
  def GetPageProfile(self, name):
    for prof in PageProfiles:
      if prof["Name"] == name:
        return prof
    return None
  
  def LoadTickerList(self, filename):
    f = codecs.open(filename, 'r', 'utf-8')
    list = []
    for line in f:
      list.append(line.strip())

    f.close()
    return list

  def GetStockType(self, ticker):
      if str(ticker)[0]=='0' or  str(ticker)[0]=='2':
          return "sz"
      elif str(ticker)[0]=='6' or str(ticker)[0]=='9':
          return "sh"
      else:
          return "all"
    
  def GetExchangeProfile(self,name):
    for name  in ExchangesProfiles:
        return ExchangesProfiles[name]
    return None
