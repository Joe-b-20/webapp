from pywebio.input import input_group, textarea
from pywebio.output import put_text, put_markdown, put_scrollable
from pywebio import start_server
from job_scraper import get_jobs_posts_indeed, save_jobs_to_json, get_time_stamp
from openai_compatibility_evaluator import get_compatibility
import pywebio.input as inputt
import json
import os


def input_job_details():
    job_title = input_group("Enter the job title:", inputs=[inputt.input(name='title', type=inputt.TEXT, required=True)])
    job_location = input_group("Enter the job location:", inputs=[inputt.input(name='location', type=inputt.TEXT, required=True)])
    resume = textarea("Enter your resume", required=True)
    return job_title, job_location, resume


def scrape_jobs(job_title, job_location):
    put_markdown("## Scraping job listings from Indeed...")
    jobs = get_jobs_posts_indeed(job_title={'name': job_title}, job_location={'name': job_location})
    if not jobs:
        put_markdown("No job listings found.")
        return None
    else:
        put_markdown("## Saving job listings to JSON file...")
        save_jobs_to_json(jobs, 'indeed_jobs')
        return jobs


def display_jobs(jobs):
    put_markdown("## Reading job listings from JSON file...")
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
            put_markdown(f"### {idx + 1}. {job['title']}")
            put_text(f"Company: {job['company']}")
            put_text(f"Location: {job['location']}")
            put_text(f"URL: {job['url']}")
            put_markdown("---")
        return jobs


def calculate_compatibility(jobs, resume):
    put_markdown("## Computing compatibility")
    compatibility_list = []
    for job in jobs:
        output = get_compatibility(resume, job['description'])
        compatibility_list.append(output)
    return compatibility_list


def save_compatibility_to_file(compatibility_list):
    filename = f'compatibility_{get_time_stamp()}.json'
    print(f"Creating file: {filename}")
    with open(filename, 'w') as f:
        json.dump(compatibility_list, f, indent=4)
    print(f"File contents: {compatibility_list}")




def display_compatibility(jobs, compatibility_list):
    put_markdown("## Compatibility Info")
    for idx, compatibility in enumerate(compatibility_list):
        put_markdown(f"### {idx + 1}. {jobs[idx]['title']} Compatibility Info")
        put_markdown("#### Compatibility Rating:")
        put_text(compatibility['rating'])
        put_markdown("#### Compatibility Summary:")
        put_markdown(compatibility['summary'])
        put_markdown("#### Resume Suggestions:")
        put_text(compatibility['suggestions'])
        put_markdown("#### Follow-up Email:")
        put_text(compatibility['followup_email'])
        put_markdown("---")



def main():
    put_markdown("# Job Scraper and Compatibility Evaluator")
    job_title, job_location, resume = input_job_details()
    jobs = scrape_jobs(job_title['title'], job_location['location'])
    if jobs:
        jobs = display_jobs(jobs)
        calculate_compatibility(jobs, resume)


if __name__ == '__main__':
    main()
