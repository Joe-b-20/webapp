from pywebio.input import input_group, textarea
from pywebio.output import put_text, put_markdown, put_scrollable, use_scope
from pywebio import start_server
from job_scraper import get_jobs_posts_indeed, save_jobs_to_json, get_time_stamp
from openai_compatibility_evaluator import get_compatibility
import pywebio.input as inputt
import pywebio.output as outputt
import json
import os


def input_job_details():
    inputs = [
     inputt.input(name='title', type=inputt.TEXT, label = "Enter the job title:" ,required=True),
     inputt.input(name='location', type=inputt.TEXT, label = "Enter the job location:", required=True),
     inputt.textarea( label = "Enter your resume", name='resume', required=True)
     ]
    results = input_group("Enter Info", inputs)
    print(results["title"])
    return results["title"], results["location"], results["resume"]


def scrape_jobs(job_title, job_location):
    with outputt.put_loading():
        put_markdown("## Scraping job listings from Indeed...")
        jobs = get_jobs_posts_indeed(job_title= job_title, job_location= job_location)
    if not jobs:
        put_markdown("No job listings found.")
        return None
    else:
        with outputt.put_loading():
            put_markdown("## Saving job listings to JSON file...")
            save_jobs_to_json(jobs, 'indeed_jobs')
        return jobs


def display_jobs(jobs):
    with outputt.put_loading():
        put_text("## Reading job listings from JSON file...")
    # Get the current timestamp to construct the filename
        time_stamp = get_time_stamp()
        filename = f'indeed_jobs_{time_stamp}.json'
    # Check if the JSON file exists before attempting to read from it
    if not os.path.isfile(filename):
        put_markdown("No job listings found.")
    else:
        with open(filename) as f:
            jobs = json.load(f)

        put_markdown("## Job info")
        for idx, job in enumerate(jobs):
            outputt.put_link(name  =  f"{job['title']}",  url = f"{job['url']}")
            #put_markdown(f"### {idx + 1}. {job['title']}")
            put_text(f"Company: {job['company']}")
            put_text(f"Location: {job['location']}")
            
            
        return jobs


def calculate_compatibility(jobs, resume):
    
    
    for job in jobs:
        compatibility_rating_int , compatibility_summary_r , resume_suggestions_r , followup_email_r = get_compatibility(resume, job['description'])
       # compatibility_list.append(output)
        compatibility_list = [compatibility_rating_int , compatibility_summary_r , resume_suggestions_r , followup_email_r]
    return compatibility_list


def save_compatibility_to_file(compatibility_list):
    filename = f'compatibility_{get_time_stamp()}.json'
    print(f"Creating file: {filename}")
    with open(filename, 'w') as f:
        json.dump(compatibility_list, f, indent=4)
    print(f"File contents: {compatibility_list}")




def display_compatibility(jobs, resume):
    with outputt.put_loading():
        put_markdown("## Computing compatibility")
        compatibility_list = calculate_compatibility(jobs, resume)
        
    put_markdown("## Compatibility Info")
    outputt.put_scrollable(outputt.put_scope('output1'), height=350, keep_bottom=True)
    with use_scope('output1'):
       
            #put_markdown(f"### {idx + 1}. {jobs[idx]['title']} Compatibility Info")
            put_markdown("#### Compatibility Rating:")
            put_text(compatibility_list[0])
            put_markdown("#### Compatibility Summary:")
            put_markdown(compatibility_list[1])
            put_markdown("#### Resume Suggestions:")
            put_text(compatibility_list[2])
            put_markdown("#### Follow-up Email:")
            put_text(compatibility_list[3])
            put_markdown("---")



def main():
    put_markdown("# Job Scraper and Compatibility Evaluator")
    job_title, job_location, resume = input_job_details()
    jobs = scrape_jobs(job_title, job_location)
    if jobs:
        jobs = display_jobs(jobs)
        
        display_compatibility(jobs, resume)


if __name__ == '__main__':
    main()
