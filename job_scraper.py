from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

def get_jobs_posts_indeed(job_title={'name': 'Software Engineer'}, job_location={'name': 'Reston, VA'}, url=''):
    def is_not_blank(s):
        return bool(s and not s.isspace())

    stitle = job_title.get('name', '')
    slocation = job_location.get('name', '')

    if not url:
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
        driver.get('https://www.indeed.com/')

        if is_not_blank(stitle):
            job_title_input = driver.find_element(By.NAME, 'q')
            job_title_input.send_keys(stitle)

        location_input = driver.find_element(By.ID, 'text-input-where')
        location_input.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        location_input.send_keys(slocation)

        location_input.send_keys(Keys.ENTER)

        time.sleep(3)

    else:
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
        driver.get(url)
        time.sleep(3)

    job_listings = driver.find_elements(By.TAG_NAME, 'tbody')
    jobs = []
    count = 0

    for i in job_listings:
        if is_not_blank(i.text):
            try:
                url = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
                title = i.find_element(By.TAG_NAME, 'a').get_attribute('aria-label')
                company = i.find_element(By.CLASS_NAME, 'companyName').text
                location = i.find_element(By.CLASS_NAME, 'companyLocation').text
                description = get_job_description_indeed(url)
                jobs.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'url': url,
                    'description': description
                })
                count += 1
            except:
                pass
            
            if count == 1:
                break

    driver.close()

    return jobs[:1]



def get_job_description_indeed(url):
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
    driver.get(url)
    time.sleep(2)
    job_description = driver.find_element(By.ID, 'jobDescriptionText').text
    title = driver.find_element(By.TAG_NAME, 'h1').text
    driver.close()

    return title, job_description

def get_time_stamp():
    import datetime
    time = datetime.datetime.now()
    return time.strftime('%m_%d_%Y__%I_%M_%p')

# save data to json file
def save_jobs_to_json(jobs, filename):
    time_stamp = get_time_stamp()
    with open(f'{filename}_{time_stamp}.json', 'w') as f:
        json.dump(jobs, f, indent=4)


# test function
# test function
def test_get_jobs_posts_indeed():
    jobs = get_jobs_posts_indeed(job_title={'name': 'Software Engineer'}, job_location={'name': 'Reston, VA'})
    assert len(jobs) > 0, 'No job postings found'
    for job in jobs:
        assert 'title' in job, 'Title not found in job posting'
        assert 'company' in job, 'Company not found in job posting'
        assert 'location' in job, 'Location not found in job posting'
        assert 'url' in job, 'URL not found in job posting'
        assert 'description' in job, 'Description not found in job posting'
    print('Test passed')

#This will run the test_get_jobs_posts_indeed() function whenever the script is 
#executed. If all assertions pass, you should see Test passed.
# If any of the assertions fail, you will
#see an error message indicating which assertion failed.


if __name__ == '__main__':
    test_get_jobs_posts_indeed()
    jobs = get_jobs_posts_indeed(job_title={'name': 'Software Engineer'}, job_location={'name': 'Reston, VA'})
    save_jobs_to_json(jobs, 'indeed_jobs')