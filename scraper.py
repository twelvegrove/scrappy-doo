import mechanize
import urllib2
from bs4 import BeautifulSoup

URL = 'https://banner.newpaltz.edu/pls/PROD/bwckzschd.p_dsp_search?p_term=201301'
SOUP = BeautifulSoup(urllib2.urlopen(URL).read(), 'lxml')


def main():

  print '\n***********************************'
  print 'SCRAPER  JAN 2012'
  print '***********************************\n'
  getSubjects()
  getPeople()
  mech()
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
  print 'Wrote subjects to subjects.txt'
  SubjectFile.close()

# Get 3-letter major codes for form submission
  for option in subjects.findAll('option'):
    #print option.get('value')
    p_subjFile.write(option.get('value')+'\n')
  print 'Wrote p_subj to p_subj.txt'
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
  print 'Wrote p_instr_pidm to p_instr.txt'
  p_instrFile.close()

#==========================================================
# submit the form for each subject code
def mech():

  br = mechanize.Browser()
  p_subjFile = open('p_subj.txt', 'r')
  
  for line in p_subjFile:
    line = line.strip()
    if line == '': continue
    br.open(URL)
    br.select_form(name='search')  # form name 
    br['p_subj'] = [line]          # field to select from
    print 'Submitting ' + line + '... ',
    response = br.submit()         # submit the form
    with open(line + '.html', 'w') as outFile:
      outFile.write(response.read())
    print 'wrote ' + line + '.html'
    #getSchedule(line)

  p_subjFile.close()

#==========================================================    
# ****** TO BE REPLACED WITH SCRAPERMONGO.PY *************
def getSchedule(line):
  with open(line + '.html', 'r') as inFile:
    soup = BeautifulSoup(inFile,'lxml')
    table = soup('table', {'class' : 'table'})[0]  # find the table

    trs = table.findAll('tr')                 # find all table rows

    for row in trs:                        
      tds = row.findAll('td')                 # for each row, find all table data
      for item in tds:
        if item.find('abbr'):                 # if td includes 'abbr' tag (i.e. it is the classroom field)
        #print item.find('abbr').string,
          print item.get_text(),
        else:
          print item.string,
        print '|',
      print '' 

#==========================================================
def toJSON():
  print 'json comes from here'  

  
if __name__ == '__main__':
  main()


