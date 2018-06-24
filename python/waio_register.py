from selenium import webdriver
from selenium.webdriver.support.ui import Select

def get_course_name(course_name):
    if course_name == 'CIS':
        return 'CIS - Computing & Information Sci.'

browser = webdriver.Chrome()

browser.get('https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor?TOKENIDX=5343575873&CONSTITUENCY=WBDF&type=P&pid=UT-LGRQ&PROCESS=-UTAUTH01')

username = input('Central Login ID: ')
password = input('Password: ')

browser.find_element_by_id('USER_NAME').send_keys(username)
browser.find_element_by_id('CURR_PWD').send_keys(password)
browser.find_element_by_id('CURR_PWD').submit()

browser.get('https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor?TOKENIDX=5343575873&CONSTITUENCY=WBST&type=P&pid=ST-WESTS04A')

term_short = input('Term (ex. F18): ')

term = ''
if term_short[0] == 'F': # fall
    term = term_short + ' - Fall 20' + term_short[1] + term_short[2]
elif term_short[0] == 'W': # winter
    term = term_short + ' - Winter 20' + term_short[1] + term_short[2]
else: # summer
    term = term_short + ' - Summer 20' + term_short[1] + term_short[2]

# select term
Select(browser.find_element_by_id('VAR1')).select_by_visible_text(term)

course_name = input('Course (ex. CIS*2750): ')
course_short, course_number = course_name.split('*') 

Select(browser.find_element_by_id('LIST_VAR1_1')).select_by_visible_text(get_course_name(course_short))

browser.find_element_by_id('LIST_VAR3_1').send_keys(course_number)
browser.find_element_by_id('LIST_VAR3_1').submit()
    

