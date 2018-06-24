from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json

browser = webdriver.Chrome()

browser.get('https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor?TOKENIDX=5343575873&CONSTITUENCY=WBDF&type=P&pid=UT-LGRQ&PROCESS=-UTAUTH01')

username = input('Central Login ID: ')
password = input('Password: ')

browser.find_element_by_id('USER_NAME').send_keys(username)
browser.find_element_by_id('CURR_PWD').send_keys(password)
browser.find_element_by_id('CURR_PWD').submit()

browser.get('https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor?TOKENIDX=5343575873&CONSTITUENCY=WBST&type=P&pid=ST-WESTS04A')

courses = [x for x in browser.find_element_by_id('LIST_VAR1_1').find_elements_by_tag_name('option')]

subjects = {}

for element in courses[1:]:
    course_name = element.get_attribute('text')

    # select term    
    Select(browser.find_element_by_id('VAR1')).select_by_visible_text('F18 - Fall 2018')

    # select course
    Select(browser.find_element_by_id('LIST_VAR1_1')).select_by_visible_text(course_name)

    # get results
    browser.find_element_by_name('SUBMIT2').click()

    # list of all sections for a given subject
    sections = []

    # get classes
    for row in browser.find_element_by_id('GROUP_Grp_WSS_COURSE_SECTIONS').find_elements_by_tag_name('tr')[1:]:
        cells = row.find_elements_by_tag_name('td')
        
        # an individual section for a given subject
        section = {}
        
        section['status'] = cells[4].text
        section['name'] = cells[5].text # todo manipulate name
        
        times = cells[7].text.split('\n')
        sessions = []

        for i in range(0, len(times) - 1, 3):
            ses = {}
            ses['type'] = times[i][:3]
            ses['days'] = times[i][4:].split(', ')
            ses['time'] = times[i + 1]
            ses['room'] = times[i + 2]

            sessions.append(ses)

        section['sessions'] = sessions

        section['professor'] = cells[8].text

        availability = cells[9].text
        section['available'] = int(availability.split(' / ')[0])
        section['capacity'] = int(availability.split(' / ')[1])

        # append the section to the list of sections
        sections.append(section)

    subjects[course_name.split(' -')[0].lower()] = sections

    with open('courses.json', 'w') as outfile:
        json.dump(subjects, outfile)
