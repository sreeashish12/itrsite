import os
import PyPDF2
import spacy
import re
from spacy.matcher import Matcher
import pandas as pd 
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib

def initialize():
    try:
        os.remove('result.csv')
    except:
        pass
        # Folder Path
        path = "media"

        # Change the directory
        os.chdir(path)

# Read pdf File
def read_pdf_file(file_path):
    pdfFileObj = open(file_path,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)
    text = pageObj.extractText()
    pdfFileObj.close()
    return text

def getDOB(text):
    pattern = '(\d+) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d+)'
    matches = re.findall(pattern, text)
    dob = ""
    for m in matches[2]:
        dob=dob + m + ' '
    return dob

def getGender(l):
    gender=""
    if "Male" in l:
        gender = "Male"
    else:
        gender = "Female"
    return gender

def getEmailID(nlp,text):
    matcher = Matcher(nlp.vocab)
    pattern = [{"LIKE_EMAIL": True}]
    matcher.add("EMAIL_ADDRESS", [pattern])
    doc = nlp(text)
    matches = matcher(doc)
    email = doc[matches[0][1]:matches[0][2]]
    return email

def getPhoneNumber(l,text):
    pattern = '\d{12}'  
    matches = re.findall(pattern, text)
    phone_number = matches[0]
    return phone_number

def getCurrentPosition(l):
    index_of_address = l.index("Address")
    return l[index_of_address+3]

def getCurrentCompany(l):
    index_of_address = l.index("Address")
    current_company= l[index_of_address+5]
    if l[index_of_address +6]!='':
        current_company+= l[index_of_address+6]
    return current_company

def getCurrentLocation(text,l):
    pattern = '\d+ yr \d+m'
    matches = re.findall(pattern, text)
    index_of_experience = l.index(matches[0]+' ')
    current_location = l[index_of_experience+4]
    return current_location

def getExperience(text):
    pattern = '\d+ yr \d+m'
    matches = re.findall(pattern, text)
    return matches[0]

def getSalary(text):
    pattern = '\d+.?\d+? Lac\(s\)'
    matches = re.findall(pattern, text)
    if matches:
        return matches[0]
    else:
        return 'NaN'

def getHighestDegree(l,text):
    pattern = '\d+ Days or less'
    matches = re.findall(pattern,text)
    index_of_notice_period = l.index(matches[0])
    return l[index_of_notice_period-4] + l[index_of_notice_period-3]+l[index_of_notice_period-2]

def getNoticePeriod(text):
    pattern = '\d+ Days or less'
    matches = re.findall(pattern,text)
    return matches[0]

def getPrefLocation(l):
    index_of_pref_loc = l.index("Pref Location:")
    pref_loc = l[index_of_pref_loc+1]
    return pref_loc

def getKeySkills(l):
    key_skills=""
    index_of_key_skills = l.index('Key skills:')
    if l[index_of_key_skills+2].startswith("Active:"):
        key_skills =  l[index_of_key_skills+1]
    else:
        key_skills = l[index_of_key_skills+1] +l[index_of_key_skills+2]
    return key_skills

def ResumeParser():
    #define headers for the excel sheet
    headers = ["Name","DOB","Gender","Email ID","Phone Number","Current Position","Current Company","Current Location","Experience","Salary","Highest Degree","Notice Period","Pref Location","Key Skills"]
    
    #using scapy / nlp for email address 
    nlp = spacy.load("en_core_web_sm")
    
    #define a df
    df = pd.DataFrame(columns=headers)
    
    # iterate through all file
    for file in os.listdir():
        
        # Check whether file is in text format or not
        if file.endswith(".pdf"):
            file_path = f"{file}"
            
            # call read text file function
            text = read_pdf_file(file_path)
    
            #split the text into a list
            l = list(text.split('\n'))
            index_of_address = l.index("Address") #using this index obtain the name
            
            #set dob using regular expression
            dob = getDOB(text)
            
            #set gender
            gender = getGender(l)
            
            #set email ID using scapy
            #email=getEmailID(nlp,text)
            
            #set phone number using regular expression
            phone_number = getPhoneNumber(l,text)
            
            #set current position
            current_position = getCurrentPosition(l)
            
            #set current company
            current_company = getCurrentCompany(l)
            
            #set current location
            current_location = getCurrentLocation(text,l)
            
            #set experience
            experience = getExperience(text)
            
            #set salary
            salary = getSalary(text)
            
            #set highest degree
            highest_degree = getHighestDegree(l,text)
            
            #set notice period
            notice_period = getNoticePeriod(text)
            
            #set pref location
            pref_loc =getPrefLocation(l)
            
            #set key skills, key skills can be more than 1 line 
            key_skills = getKeySkills(l)
            
            #append to data frame
            df = df.append({'Name':l[index_of_address+2],
                            'DOB':dob,
                            'Gender':gender,
                            'Email ID':'sreeashisharisetty@gmail.com',
                            'Phone Number':phone_number,
                            "Current Position":current_position,
                            "Current Company":current_company,
                            "Current Location":current_location,
                            "Experience":experience,
                            "Salary":salary,
                            "Highest Degree":highest_degree,
                            "Notice Period":notice_period,
                            "Pref Location":pref_loc,
                            "Key Skills":key_skills},ignore_index=True)
    #print df and save it
    print(df)
    df.to_csv('result.csv', header=headers)
