from pymongo import MongoClient
from bs4 import BeautifulSoup

def blah():
  db = MongoClient().test
  db.examples.insert({'name':'jesse'})
  db.examples.insert({'name':'kurt'})
  db.examples.insert({'_id':'12345'})
 
  

def main():
  
  db = MongoClient().test
  
  subject = 'Anthropology'  # change for each subject
  crn = 0
  course = None
  sec = None
  title = None
  credits = None
  days = None
  time = None
  loc1 = None
  instructor = None
  attrib = None   # attributes
  avail = None    # seats available
  level = None    # grad or undergrad
  
  days2 = None
  time2 = None
  loc2 = None     # 2nd location, if needed
  instructor2 = None
  
  check = 0
  counter = 0
 
  mainArray = ['crn','course','sec','title','credits','days','time','loc1','instructor','attrib','avail']
  secondArray = ['days2','time2','loc2','instructor2']

  with open('BIO.html', 'r') as inFile:
    soup = BeautifulSoup(inFile,'lxml')
    table = soup('table', {'class' : 'table'})[0]  # find the table

    trs = table.findAll('tr')                 # find all table rows

    print 'Doing lots of stuff... '
    for row in trs:
      counter = 0                        
      check = 0
      tds = row.findAll('td')                 # for each row, find all table data
      #ths = row.findAll('th')
      for item in tds:
        if item.string.isdigit() == True:
            db.spring2013.insert({'crn':crn,'course':course,'sec':sec,'title':title,'credits':credits,'days':days,'time':time,'loc1':loc1,'instructor':instructor,'attrib':attrib,'avail':avail,'days2':days2,'time2':time2,'loc2':loc2,'instructor2':instructor2})
        break
      for item in tds:
          field = item.string 
          if field == None: field = ''
          #print field
          if (field.isdigit() == False and counter == 0) or check == 1:
            # set other values
            if counter == 0:
              days2 = field
              check = 1
            elif counter == 1:
              time2 = field
            elif counter == 2:
              loc2 = item.get_text()
            elif counter == 3:
              instructor2 = field
              check = 0
          elif crn != 0:
            #db.spring2013.insert({'crn':crn,'course':course,'sec':sec,'title':title,'credits':credits,'days':days,'time':time,'loc1':loc1,'instructor':instructor,'attrib':attrib,'avail':avail,'days2':days2,'time2':time2,'loc2':loc2,'instructor2':instructor2}) 
            days2 = None
            time2 = None
            loc2 = None
            instructor2 = None
         
            if counter == 0: crn = field
              #crn = field
            elif counter == 1: course = field
              #course = field
            elif counter == 2: sec = field
              #sec = field
            elif counter == 3:
              title = field
            elif counter == 4:
              credits = field
            elif counter == 5:
              days = field
            elif counter == 6:
              time = field
            elif counter == 7:
              loc1 = item.get_text()
            elif counter == 8:
              instructor = field
            elif counter == 9:
              attrib = field
            elif counter == 10:
              avail = field
            
          else:
            # set main values
            if counter == 0:
              crn = field
            elif counter == 1:
              course = field
            elif counter == 2:
              sec = field
            elif counter == 3:
              title = field
            elif counter == 4:
              credits = field
            elif counter == 5:
              days = field
            elif counter == 6:
              time = field
            elif counter == 7:
              loc1 = item.get_text()
            elif counter == 8:
              instructor = field
            elif counter == 9:
              attrib = field
            elif counter == 10:
              avail = field
          counter += 1
    print 'Done'

if __name__ == '__main__':
  main()

