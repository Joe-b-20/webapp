from pywebio.input import input_group, textarea
from pywebio.output import put_text, put_markdown, put_scrollable
from pywebio import start_server
from job_scraper import get_jobs_posts_indeed
from openai_compatibility_evaluator import get_compatibility
import pywebio.input as inputt


def main():
    put_markdown("# Job Scraper and Compatibility Evaluator")

    job_title = input_group("Enter the job title:", inputs=[inputt.input(name='title', type=inputt.TEXT, required=True)])
    job_location = input_group("Enter the job location:", inputs=[inputt.input(name='location', type=inputt.TEXT, required=True)])

    resume = textarea("Enter your resume", required=True)

    put_markdown("## Scraping job listings from Indeed...")

    jobs = get_jobs_posts_indeed(job_title, job_location)

    if not jobs:
        put_markdown("No job listings found.")
    else:
        put_markdown("## Job Listings and Compatibility Evaluation:")
        for idx, job in enumerate(jobs):
            put_markdown(f"### {idx + 1}. {job['title']}")
            put_text(f"Company: {job['company']}")
            put_text(f"Location: {job['location']}")
            put_text(f"URL: {job['url']}")
            put_markdown("---")

            output = get_compatibility(resume, job['description'])
            put_markdown("#### Compatibility Rating:")
            put_text(output['rating'])
            put_markdown("#### Compatibility Summary:")
            put_text(output['summary'])
            put_markdown("#### Resume Suggestions:")
            put_text(output['suggestions'])
            put_markdown("#### Follow-up Email:")
            put_text(output['followup_email'])
            put_markdown("---")
if __name__ == '__main__':
    main()

