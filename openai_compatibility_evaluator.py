import openai

openai.api_key = ("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")

def get_respond_from_openai(message):
    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        temperature=0.7,
        max_tokens=1200,
        n = 1,
        stop = None,
        timeout = 15,
        frequency_penalty = 0,
        presence_penalty = 0
    )
    return completion.choices[0].text.strip()

def slice_text(text, start_word, end_word):
  start_index = text.find(start_word) + len(start_word)
  if end_word is None:
    end_index = len(text)
  else:
    end_index = text.find(end_word)
  return text[start_index:end_index]

def find_int(string):
  number = ""
  for char in string:
    if char.isdigit():
      number += char
  return int(number)

def break_down_openai_output(output,file_name):
   # write_to_text_file("file_name", f"raw_{output}")
    
    f = "\n"+ "_"*80+ "\n"
    
    compatibility_rating = (slice_text(output, "Compatibility rating = ", "Compatibility summary"))
    compatibility_rating_int = (find_int(compatibility_rating))
    compatibility_rating_str = (str(compatibility_rating) + f)
    compatibility_rating_str = (f + f"\nCompatibility rating = {compatibility_rating_str}")
    
    compatibility_summary_r = (slice_text(output, "Compatibility summary = ", "Suggestions for the resume"))
    compatibility_summary = (f"\nCompatibility summary:\n\n{compatibility_summary_r}" + f)

    resume_suggestions_r = (slice_text(output, "Suggestions for the resume = ", "Follow-up email"))
    resume_suggestions = (f"\nResume Suggestions:\n\n{resume_suggestions_r}" + f)
    
    followup_email_r = (slice_text(output, "Follow-up email = ", None))
    followup_email = (f"\nFollow-up email:\n\n{followup_email_r}" + f+f)
    
    final  = (compatibility_rating_str + compatibility_summary + resume_suggestions + followup_email)

   # write_to_text_file(file_name, final)
    
    return compatibility_rating_int , compatibility_summary_r , resume_suggestions_r , followup_email_r
    
def get_compatibility(resume, description):
    message = f"Please rate the compatibility between the following resume and job description on a scale of 0-100, provide a summary of the compatibility rating, provide suggestions for resume to best fit the job description, and provide a follow-up email to the employer.\n \
               Resume:  {resume} \n \
               Job Description:  {description}\n \
               Please rate the compatibility between the resume and job description on a scale of 0-100, provide a summary of the compatibility rating, provide suggestions for the resume to ensure the best fit for the job description, and craft a follow-up email to the employer.\n \
               Format the output as follows:\n \
               Compatibility rating = \n \
               Compatibility summary = \n \
               suggestions for the resume = \n \
               Follow-up email ="
                
    respond = get_respond_from_openai(message)
    sections = respond.split("\n\n\n")
   # if len(sections) < 4:
        #raise ValueError(f"Expected at least 4 sections in output, but found {len(sections)}:\n\n{respond}")
    return break_down_openai_output(respond,"file_name")


def evaluate_job_compatibility(resume,text):
         
    output = get_compatibility(resume, text)
    
    return output
# this file has major issues 
# there need to be more instractions regarding the tokens and prompt that is 
# sent to the api because they are not doing the job

#This test function uses the assert statement to check that the get_compatibility() 
#function returns a dictionary with the expected fields (rating, summary, suggestions, and followup_email).
#It also checks that the rating field is a valid integer between 0 and 100.
#If any of the assertions fail, an error message will be printed to the console indicating which field was not found in the output or which assertion failed.
def test_get_compatibility():
    resume = "John Smith\n123 Main Street\nAnytown, USA 12345\n(555) 555-5555\njohn.smith@email.com\n\nSummary:\nExperienced software engineer with a track record of success in developing high-quality, scalable software solutions.\n\nSkills:\n- Python\n- Java\n- JavaScript\n- SQL\n- Agile development\n\nExperience:\nSoftware Engineer\nABC Company\nJanuary 2018 - Present\n- Developed and maintained web applications using Python and Django\n- Designed and implemented RESTful APIs\n- Optimized database queries for improved performance\n\nEducation:\nBachelor of Science in Computer Science\nXYZ University\nMay 2017"
    description = "We are looking for a software engineer to join our team. The ideal candidate will have experience with Python, Java, and SQL, as well as familiarity with Agile development methodologies. Responsibilities include developing and maintaining web applications, designing and implementing RESTful APIs, and optimizing database queries for improved performance. Qualifications include a Bachelor's degree in Computer Science and at least 2 years of experience in software engineering."

    compatibility = get_compatibility(resume, description)

    assert 'rating' in compatibility, 'Compatibility rating not found in output'
    assert 'summary' in compatibility, 'Compatibility summary not found in output'
    assert 'suggestions' in compatibility, 'Suggestions for the resume not found in output'
    assert 'followup_email' in compatibility, 'Follow-up email not found in output'
    assert 0 <= int(compatibility['rating']) <= 100, 'Compatibility rating is not a valid number between 0 and 100'
if __name__ == '__main__':
    test_get_compatibility()
