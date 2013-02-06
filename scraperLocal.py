from bs4 import BeautifulSoup
from pymongo import MongoClient

YEAR = '2013'
SEMESTER = 'Spring'
SEMESTERCODE = '01'
SCHOOL = 'State University of New York at New Paltz'

def main():
  line = 'CPS'
  lineCount = 16
  getClasses(line, lineCount)

def getClasses(line,lineCount):
  
  db = MongoClient().test
  
  subject = None 
  crn = -1
  course = None
  sec = None
  title = None
  credits = None
  days1 = None
  time1 = None
  loc1 = None
  instructor1 = None
  attrib = None   # attributes
  avail = None    # seats available
  level = None    # grad or undergrad
  link = None  
  isRelated = None  # boolean value; is class in the 'related courses' section?
  
  days2 = None
  time2 = None
  loc2 = None     # 2nd location, if needed
  instructor2 = None
  
  check = 0       # I have no idea what this does
  counter = 0
 
  with open('subjects.txt', 'r') as inFile:
    i = 0
    for subjLine in inFile:
      subject = subjLine.strip()
      if subject == '':
        continue 
      i += 1
      if i == lineCount:
        break  

  print '   Processing ' + subject + '... ',

  with open(line + '.html', 'r') as inFile:
    soup = BeautifulSoup(inFile,'lxml')
    table = soup('table', {'class' : 'table'})[0]  # find the table

    trs = table.findAll('tr')                 # find all table rows
    
    for row in trs:
      counter = 0                        
      check = 0
      tds = row.findAll('td')                 # for each row, find all table data
      # This stupid loop tests whether or not the next line has a CRN, and if so, insert current line to db.
      # If not, there are additional meeting times, so wait til the next time around to insert. 
      # if crn != -1 ensures that it doesn't insert the first time around, when all values are null.
      for item in tds:
        field = item.string
        if field == None: field = ''
        if field.isdigit() == True and crn != -1:
          db.courses.insert({'classes':[{'instructor':instructor1,'time':time1,'days':days1,'location':loc1},{'instructor':instructor2,'time':time2,'days':days2,'location':loc2}],'course':course,'semester':SEMESTER,'section':sec,'year':YEAR,'subject':subject,'title':title,'credits':credits,'link':link,'isRelated':isRelated,'school':SCHOOL,'level':level,'attributes':attrib,'crn':crn,'seatsAvailable':avail})
        break
      for item in tds:
          field = item.string 
          if field == None: field = ''
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
         
            if counter == 0:
              try: crn = int(field)
              except ValueError: crn = field
              link = 'https://banner.newpaltz.edu/pls/PROD/bwckzschd.p_display_sect?p_term_code=' + YEAR + SEMESTERCODE + '&p_crn=' + str(crn)
            elif counter == 1:
              course = field
              try:
                num = int(course[3:])
                if num < 500:
                  level = 'undergraduate'
                else:
                  level = 'graduate'
              except ValueError:
                print 'ERROR: unknown course level' 
              isRelated = not(course[:3] == line) # if the course matches the subject code, it's not a related course
            elif counter == 2:
              sec = field
            elif counter == 3:
              title = field
            elif counter == 4:
              credits = field
            elif counter == 5:
              days1 = field
            elif counter == 6:
              time1 = field
            elif counter == 7:
              loc1 = item.get_text()
            elif counter == 8:
              instructor1 = field
            elif counter == 9:
              attrib = field
            elif counter == 10:
              try: avail = int(field)
              except ValueError: avail = 0
            
          else:
            # set main values
            if counter == 0:
              try: crn = int(field)
              except ValueError: crn = field
              link = 'https://banner.newpaltz.edu/pls/PROD/bwckzschd.p_display_sect?p_term_code=' + YEAR + SEMESTERCODE + '&p_crn=' + str(crn)
            elif counter == 1:
              course = field
              try:
                num = int(course[3:])
                if num < 500:
                  level = 'undergraduate'
                else:
                  level = 'graduate'
              except ValueError:
                print 'ERROR: unknown course level' 
              isRelated = not(course[:3] == line) # if the course matches the subject code, it's not a related course
            elif counter == 2:
              sec = field
            elif counter == 3:
              title = field
            elif counter == 4:
              credits = field
            elif counter == 5:
              days1 = field
            elif counter == 6:
              time1 = field
            elif counter == 7:
              loc1 = item.get_text()
            elif counter == 8:
              instructor1 = field
            elif counter == 9:
              attrib = field
            elif counter == 10:
              try: avail = int(field)
              except ValueError: avail = 0
          counter += 1

    # now insert the last class row
    db.courses.insert({'classes':[{'instructor':instructor1,'time':time1,'days':days1,'location':loc1},{'instructor':instructor2,'time':time2,'days':days2,'location':loc2}],'course':course,'semester':SEMESTER,'section':sec,'year':YEAR,'subject':subject,'title':title,'credits':credits,'link':link,'isRelated':isRelated,'school':SCHOOL,'level':level,'attributes':attrib,'crn':crn,'seatsAvailable':avail})
    print 'done'

if __name__ == '__main__':
  main()
