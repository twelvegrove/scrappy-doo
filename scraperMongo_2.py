from pymongo import MongoClient
from bs4 import BeautifulSoup

def blah():
  db = MongoClient().test
  db.examples.insert({'name':'jesse','information':[{'age':24,'weight':249}]})
#  db.examples.update({'name':'jesse','information':[{'age':24,'weight':249,'hello':'hello'}]})
  db.examples.insert({'name':'kurt'})
  #db.examples.insert({'name':'kurt'})
  #db.examples.insert({'_id':'12345'})
 
def blah2():
  test = "CPS333"
  number = test[:3]
  print number

def main():
  #getSchedule()  
  #blah()
  blah2()
def getSchedule():
  
  db = MongoClient().test
 
  SCHOOL = 'SUNY'
  YEAR = 2013
  SEMESTER = 'Spring' 
  subject = 'Anthropology'  # change for each subject
  crn = -1
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
 
  with open('ANC.html', 'r') as inFile:
    soup = BeautifulSoup(inFile,'lxml')
    table = soup('table', {'class' : 'table'})[0]  # find the table

    trs = table.findAll('tr')                 # find all table rows
    prevSuject = None
    prevCourse = None
    print 'Doing lots of stuff... '
    for row in trs:
      counter = 0                        
      check = 0
      tds = row.findAll('td')                 # for each row, find all table data
     
      # This loop tests whether or not the next row has a CRN, and if so, insert the current row to db.
      # If not, it's part of the same CRN (additional meeting time) so wait til the next time around to insert.
      # if crn != -1 ensures that it does not insert the first time around, when all values are null.
      for item in tds:
        field = item.string
        if field == None: field = ''
        if field.isdigit() == True and crn != -1 and prevSuject == None and prevCourse == None:
            db.spring2013.insert({'schools':[{'schoolName':SCHOOL,'years':[{'year':YEAR,'semesters':[{'semester':SEMESTER,'subjects':[{'subjectName':subject,'courses':[{'course':course,'sections':[{'section':sec,'sectionInfo':[{'crn':crn,'title':title,'credits':credits,'days':days,'attributes':attrib,'seatsAvail':avail,'time':time,'loc1':loc1,'loc2':loc2,'days2':days2,'time2':time2,'instructor':instructor,'instructor2':instructor2}]}]}]}]}]}]}]})
            prevSuject = subject
            prevCourse = course
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
          elif crn != -1:
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
    # now submit the last class row
    db.spring2013.insert({'crn':crn,'course':course,'sec':sec,'title':title,'credits':credits,'days':days,'time':time,'loc1':loc1,'instructor':instructor,'attrib':attrib,'avail':avail,'days2':days2,'time2':time2,'loc2':loc2,'instructor2':instructor2})
    print 'Done'

if __name__ == '__main__':
  main()

