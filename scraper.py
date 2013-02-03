import mechanize
import urllib2
from pymongo import MongoClient
from bs4 import BeautifulSoup

URL = None
SOUP = None
YEAR = None
SEMESTER = None
SCHOOL = None

def main():

  global URL
  global SOUP
  global YEAR
  global SEMESTER
  global SCHOOL

  print '\n***********************************'
  print 'SCRAPER  JAN 2012'
  print '***********************************\n'
  
  valid = False
  while valid == False:
    number = raw_input('Enter a year:\n')
    try:
      YEAR = int(number)
      YEAR = str(YEAR)
      valid = True
    except ValueError:
      print 'ERROR: Not a valid year!'

  valid = False
  while valid == False:
    number = raw_input('Select a semester: 1) Spring 2) Summer 3) Fall 4) Winter\n')
    try:
      number = int(number)
      print ''
      if number == 1:
        semesterCode = '01'
        SEMESTER = 'Spring'
        valid = True
      elif number == 2:
        semesterCode = '06'
        SEMESTER = 'Summer'
        valid = True
      elif number == 3:
        semesterCode = '09'
        SEMESTER = 'Fall'
        valid = True
      elif number == 4:
        semesterCode = '00'
        SEMESTER = 'Winter'
        valid = True
      else:
        print 'ERROR: Please enter a valid choice'
    except ValueError:
        print 'ERROR: Please select a number'        
  
  URL = 'https://banner.newpaltz.edu/pls/PROD/bwckzschd.p_dsp_search?p_term=' + YEAR + semesterCode
  SOUP = BeautifulSoup(urllib2.urlopen(URL).read(), 'lxml')

  SCHOOL = SOUP.find('h1')  # finds the school name, which is an h1 heading
  h1s = SOUP.findAll('h1')  # finds the next h1, which is the semester name e.g. Spring 2013
  
  print SCHOOL.string
  print h1s[1].string + '\n'

  getSubjects()
  getPeople()
  mechSubmit()
  print '\n...DONE!\n'

#==========================================================
def getSubjects():

  SubjectFile = open('subjects.txt', 'w')
  p_subjFile = open('p_subj.txt', 'w')
  subjects = SOUP.find(id = 'p_subj')

# Get full names of majors, output to file 
  for row in subjects:
    if row.string != 'All': 
      #print row.string
      SubjectFile.write(row.string)  
  print 'Wrote subject names to subjects.txt'
  SubjectFile.close()

# Get 3-letter major codes for form submission
  for option in subjects.findAll('option'):
    #print option.get('value')
    p_subjFile.write(option.get('value')+'\n')
  print 'Wrote subject codes to p_subj.txt'
  p_subjFile.close()

#==========================================================
def getPeople():

  peopleFile = open('people.txt', 'w')
  p_instrFile = open('p_instr_pidm.txt', 'w')
  people = SOUP.find(id = 'p_instr_pidm')

# Get full names of professors, output to file 
  for row in people:
    if row.string != 'All': 
      #print row.string
      peopleFile.write(row.string)  
  print 'Wrote names to people.txt'
  peopleFile.close()

# Get professors' codes for submission
  for option in people.findAll('option'):
    #print option.get('value')
    p_instrFile.write(option.get('value')+'\n')
  print 'Wrote instructor ids to p_instr.txt\n'
  p_instrFile.close()

#==========================================================
# submit the form for each subject code
def mechSubmit():

  br = mechanize.Browser()
  p_subjFile = open('p_subj.txt', 'r')
  subjFile = open('subjects.txt', 'r')
  lineCount = 0

  for line in p_subjFile:
    lineCount += 1
    line = line.strip()
    if line == '':
      lineCount -= 1
      continue
    br.open(URL)
    br.select_form(name='search')  # form name 
    br['p_subj'] = [line]          # field to select from
    print 'Submitting ' + line + '... ',
    response = br.submit()         # submit the form
    with open(line + '.html', 'w') as outFile:
      outFile.write(response.read())
    print 'wrote ' + line + '.html'
    getSchedule(line, lineCount)

  p_subjFile.close()

#==========================================================    
def getSchedule(line, lineCount):
  
  db = MongoClient().test
  
  subject = None 
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
 
  with open('subjects.txt', 'r') as inFile:
    i = 0
    for subjLine in inFile:
      subject = subjLine.strip()
      if subject == '':
        continue 
      i += 1
      if i == lineCount:
        break  

  with open(line + '.html', 'r') as inFile:
    soup = BeautifulSoup(inFile,'lxml')
    table = soup('table', {'class' : 'table'})[0]  # find the table

    trs = table.findAll('tr')                 # find all table rows
    print 'Adding ' + subject + ' classes to database...',
    
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
            db.spring2013.insert({'subject':subject,'crn':crn,'course':course,'sec':sec,'title':title,'credits':credits,'days':days,'time':time,'loc1':loc1,'instructor':instructor,'attrib':attrib,'avail':avail,'days2':days2,'time2':time2,'loc2':loc2,'instructor2':instructor2})
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

    # now insert the last class row
    db.spring2013.insert({'subject':subject,'crn':crn,'course':course,'sec':sec,'title':title,'credits':credits,'days':days,'time':time,'loc1':loc1,'instructor':instructor,'attrib':attrib,'avail':avail,'days2':days2,'time2':time2,'loc2':loc2,'instructor2':instructor2})
    print ' done'


  
if __name__ == '__main__':
  main()
