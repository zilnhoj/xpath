import requests
from urllib2 import urlopen
import urllib2
import pandas as pd
import lxml
from lxml import html
import pandas.io.ga as ga

url = 'https://www.gov.uk/health-conditions-and-driving'

pge = requests.get(url)

tree = html.fromstring(pge.text)
hcode = tree.xpath('//div[@class="inner"]/p[.]/a[.]/@href')
df = pd.DataFrame(hcode)


df[0] = [str(x) for x in df[0]] #to convert each entry in the dataframe to a string


#define the dimensions and metrics to use on the analytics api
dimensions = ['pagePath']
metrics = ['pageviews', 'uniquePageviews', 'entrances', 'bounceRate', 'exitRate']
start_date = '2014-08-01'
end_date = '2014-08-31'


df1 = pd.DataFrame(columns=['pageviews']) #dataframe with one series [column] - nameing the column pageviews
count = 0 #create a counter variable


for i in df[0]: #loop through the dataframe df column to pass each slug into the analytics filter field separately
    hwy = ga.read_ga(metrics=metrics, #api call
            dimensions=dimensions,
            start_date=start_date,
            end_date=end_date,
            filters=['pagePath=='+i],
            account_id='26179049')
    df1 = df1.append(hwy) #each time the api is called a dataframe [hwy] is created - we append this dataframe to df1 on each pass of the loop
    count+=1 #counts the number of times the loop is run through
    print count #prints out the number of times the loop is run through


print df1.head() #checks the first 5 results in the dataframe 
