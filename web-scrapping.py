"""
Created on Thu Jul  2 19:51:09 2020

@author: shruti_goel
"""

'''
Scrapping each page of glassdoor review for a company
'''
from requests import get
import urllib, sys
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import urllib.request, formatter, sys
import re
import math
import pandas as pd
import json
import ast

######################################## TOTAL NUMBER OF PAGES TP SCRAP ##############################################################

# url_for_page = 'https://www.glassdoor.co.in/Reviews/S-and-P-Global-Reviews-E1259396.htm'
url_for_page = 'https://www.glassdoor.co.in/Reviews/Moody-s-Analytics-Reviews-E392271.htm'
# url_for_page = 'https://www.glassdoor.co.in/Reviews/Platts-Reviews-E2724268.htm'
# url_for_page = 'https://www.glassdoor.co.in/Reviews/MSCI-Reviews-E14616.htm'
hdr_ = {'User-Agent': 'Mozilla/5.0'}
req_ = urllib.request.Request(url_for_page, headers=hdr_)
response_ = urllib.request.urlopen(req_)
data_ = response_.read()
soup_ = BeautifulSoup(data_, features='html.parser')
val = soup_.find("strong", class_="").text.split(",")
count_val = ''.join(val)
review_count = int(float(count_val))
len_loop = math.ceil(review_count / 10) + 1
company_name = soup_.find("h1", class_="eiReviews__EIReviewsPageStyles__newPageHeader col-sm-auto").text.replace(
    "Reviews", "")

####################################################### DEFINING LIST TO CONTAIN DATAFRAME #########################################################

df_list = []

##########################################################  ITERATING OVER PAGES ######################################################

for num in range(1, len_loop):
    # empty list to contain respective data
    auth_profile_list = []
    review_date_list = []
    auth_loc_list = []
    work_life_balance_list = []
    review_date_time = []
    review_id_list = []
    review_date_time_list = []
    rating_overall_list = []
    rating_ceo_list = []
    rating_business_outlook_list = []
    rating_work_life_balance_list = []
    rating_culture_and_values_list = []
    rating_diversity_and_inclusion_list = []
    rating_senior_leadership_list = []
    rating_recommend_to_friend_list = []
    rating_career_opportunities_list = []
    rating_compensation_and_benefits_list = []
    heading_list = []
    review_link_list = []
    emp_status_list = []
    author_type_list = []
    duration_text_list = []
    isCurrentJob_list = []
    lengthOfEmployment_list = []
    employmentStatus_list = []
    jobEndingYear_list = []
    pros_list = []
    cons_list = []
    advice_management_list = []
    employer_response_list = []
    intial_url = 'https://www.glassdoor.co.in/Reviews/S-and-P-Global-Reviews-'
    company_code = 'E1259396'
    # intial_url = 'https://www.glassdoor.co.in/Reviews/Platts-Reviews-'
    # company_code = 'E2724268'
    # intial_url = 'https://www.glassdoor.co.in/Reviews/MSCI-Reviews-'
    # company_code = 'E14616'
    intial_url = 'https://www.glassdoor.co.in/Reviews/Moody-s-Analytics-Reviews-'
    company_code = 'E392271'
    page_no = '_P' + str(num) + '.htm?filter.iso3Language=eng'
    url = intial_url + company_code + page_no
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    data = response.read()
    soup = BeautifulSoup(data, features='html.parser')
    data_str = data.decode("utf-8")
    # file = "C:\Mywork\glassdoor-review-scraper-master\\" + company_code + str(num) + ".txt"
    # file1 = open(file,"w", encoding='utf-8')#write mode
    # file1.write(data_str)
    # file1.close()

    ###############################################################      AUTHOR INFO.       ###############################################################

    # 1.Review Date
    # 2.Author Location
    # 3.Author Profile
    # 4.Author name
    # 5.Employee Status
    # 6.Author Type

    author_info_div = soup.find_all("span", {"class": "authorInfo"})
    for ele in author_info_div:
        auth_review_date = \
        ele.find("span", class_="authorJobTitle middle common__EiReviewDetailsStyle__newGrey").text.split("-")[0]
        auth_profile = \
        ele.find("span", class_="authorJobTitle middle common__EiReviewDetailsStyle__newGrey").text.split("-")[1]
        auth_loc = ele.find("span", class_="authorLocation")
        if auth_loc is not None:

            auth_loc_list.append(auth_loc.text.split(",")[0])
        else:
            auth_loc_list.append(None)

        auth_profile_list.append(auth_profile)
        review_date_list.append(auth_review_date)

    # This code find employee status and author type
    emp_profile = [m.start() for m in re.finditer('"author":', data_str)]
    emp_profile_end = [m.start() for m in re.finditer(',"reviewBody"', data_str)]

    for i in range(len(emp_profile)):
        start_index = emp_profile[i] + 9
        end_index = emp_profile_end[i]
        emp_profile_details = data_str[int(start_index):int(end_index)]
        res = json.loads(emp_profile_details)
        emp_status = res['name'].split("-")[0]
        emp_status_list.append(emp_status)
        author_type_list.append(res['@type'])

    #############################################################         RATINGS               ######################################################################

    # 1. review_id
    # 2. review_date_time
    # 3. rating_overall
    # 4. rating_ceo
    # 5. rating_business_outlook
    # 6. rating_work_life_balance
    # 7. rating_culture_and_values
    # 8. rating_diversity_and_inclusion
    # 9. rating_senior_leadership
    # 10. rating_recommend_to_friend
    # 11. rating_career_opportunities
    # 12. rating_compensation_and_benefits

    ratings_index = [m.start() for m in re.finditer('__typename":"EmployerReview', data_str)]
    ratings_index_end = [m.start() for m in re.finditer(',"employer":{"__ref":"Employer:', data_str)]
    for i in range(1, len(ratings_index)):
        start_index = ratings_index[i] + len('__typename":"EmployerReview') + 2
        end_index = ratings_index_end[i]
        rating_details = '{' + data_str[int(start_index):int(end_index)] + '}'
        rating_data = json.loads(rating_details)
        review_id_list.append(rating_data['reviewId'])
        review_date_time_list.append(rating_data['reviewDateTime'].split("T")[0])
        rating_overall_list.append(rating_data['ratingOverall'])
        rating_ceo_list.append(rating_data['ratingCeo'])
        rating_business_outlook_list.append(rating_data['ratingBusinessOutlook'])
        rating_work_life_balance_list.append(rating_data['ratingWorkLifeBalance'])
        rating_culture_and_values_list.append(rating_data['ratingCultureAndValues'])
        rating_diversity_and_inclusion_list.append(rating_data['ratingDiversityAndInclusion'])
        rating_senior_leadership_list.append(rating_data['ratingSeniorLeadership'])
        rating_recommend_to_friend_list.append(rating_data['ratingRecommendToFriend'])
        rating_career_opportunities_list.append(rating_data['ratingCareerOpportunities'])
        rating_compensation_and_benefits_list.append(rating_data['ratingCompensationAndBenefits'])

    ################################################################ REVIEW LINK & SUMMARY ######################################################################

    # 1. review_id
    # 2. review_date_time

    review_link = soup.find_all("a", {"class": "reviewLink"})
    for a in review_link:
        if a.text:
            review_link_list.append(a['href'])
            heading_list.append(a.text)
        else:
            review_link_list.append(None)
            heading_list.append(None)

    ############################################################## JOB DURATION & OTHER DETAILS###################################################################################

    # 1. In years
    # 2. Duration in text string
    # 3. is in job currently
    # 3. length of employment
    # 4. employment status
    # 5. job ending year

    # Code for duration in text string
    duration_text_info = soup.find_all("span", {"class": "pt-xsm pt-md-0 css-1qxtz39 eg4psks0"})
    for a in duration_text_info:
        if a.text:
            duration_text_string = a.text.split(",")
            if len(duration_text_string) >= 2:
                duration_text_list.append(duration_text_string[1])
            else:
                duration_text_list.append(None)
        else:
            duration_text_list.append(None)

    # Code for other details about job
    string_to_search = '"isCurrentJob"'
    employement_index = [m.start() for m in re.finditer(string_to_search, data_str)]
    employement_index_end = [m.start() for m in re.finditer(',"jobTitle"', data_str)]

    for i in range(len(employement_index)):
        start_index = employement_index[i]
        end_index = employement_index_end[i]
        employement_details = "{" + data_str[int(start_index):int(end_index)] + "}"
        employement_data = json.loads(employement_details)
        isCurrentJob = employement_data['isCurrentJob']
        lengthOfEmployment = employement_data['lengthOfEmployment']
        employmentStatus = employement_data['employmentStatus']
        jobEndingYear = employement_data['jobEndingYear']
        isCurrentJob_list.append(isCurrentJob)
        lengthOfEmployment_list.append(lengthOfEmployment)
        employmentStatus_list.append(employmentStatus)
        jobEndingYear_list.append(jobEndingYear)

    ############################################################ REVIEW ###############################################################################

    # 1. Pros
    # 2. Cons
    # 3. Advice to Management
    # 4. Employer Advice

    review_details_info = soup.find_all("div", {"class": "v2__EIReviewDetailsV2__fullWidth"})

    for a in review_details_info:
        try:
            pros_text = a.find("span", {"data-test": "pros"})
            if pros_text.text is not None:
                pros_list.append(pros_text.text)
            else:
                pros_list.append(None)
        except:
            pass

    for a in review_details_info:
        try:
            cons_text = a.find("span", {"data-test": "cons"})
            if cons_text.text is not None:
                cons_list.append(cons_text.text)
            else:
                cons_list.append(None)
        except:
            pass

    # Advice to Management
    advice_index = [m.start() for m in re.finditer('"advice":', data_str)]
    advice_index_end = [m.start() for m in re.finditer('"adviceOriginal":', data_str)]
    for i in range(len(advice_index)):
        advice_text = data_str[advice_index[i] + len('"advice":'):advice_index_end[i] - 1]
        if advice_text == 'null':
            advice_management_list.append(None)
        else:
            advice_management_list.append(advice_text.replace('"', ""))

    # Employer Response
    employer_response_index = [m.start() for m in re.finditer('"employerResponses":', data_str)]
    employer_response_index_end = [m.start() for m in re.finditer('"featured":', data_str)]
    for i in range(len(employer_response_index)):
        employer_response_text = data_str[
                                 employer_response_index[i] + len('"employerResponses":'):employer_response_index_end[
                                                                                              i] - 1]
        employer_response_text = employer_response_text.replace('[', "").replace(']', "")
        if employer_response_text == '':
            employer_response_list.append(None)
        else:
            employer_response_code = \
            employer_response_text.replace('"', "").replace("{", "").replace("}", "").split(':')[2]
            temp = re.findall(r'\d+', employer_response_text)
            employer_response_code = "".join(list(map(str, temp)))
            str_to_find_response_code = '{"id":' + employer_response_code + ",".replace(" ", "")
            temp_start_index = data_str.index(str_to_find_response_code)
            temp_data_employer_respones = data_str[temp_start_index:len(data_str)]
            employee_response_start_index = temp_data_employer_respones.index(str_to_find_response_code)
            employee_response_end_index = temp_data_employer_respones.index(',"userJobTitle":')
            temp_data_response = temp_data_employer_respones[
                                 employee_response_start_index:employee_response_end_index] + "}"
            response_data_dict = json.loads(temp_data_response)
            employer_response_list.append(response_data_dict['response'])

    temp_df = pd.DataFrame(list(zip([company_name] * len(review_link_list),
                                    review_link_list,
                                    review_date_list,
                                    review_id_list,
                                    review_date_time_list,
                                    emp_status_list,
                                    auth_loc_list,
                                    auth_profile_list,
                                    author_type_list,
                                    duration_text_list,
                                    isCurrentJob_list,
                                    lengthOfEmployment_list,
                                    employmentStatus_list,
                                    jobEndingYear_list,
                                    rating_work_life_balance_list,
                                    rating_culture_and_values_list,
                                    rating_diversity_and_inclusion_list,
                                    rating_senior_leadership_list,
                                    rating_career_opportunities_list,
                                    rating_compensation_and_benefits_list,
                                    rating_overall_list,
                                    rating_recommend_to_friend_list,
                                    rating_ceo_list,
                                    rating_business_outlook_list,
                                    pros_list,
                                    cons_list,
                                    heading_list,
                                    advice_management_list,
                                    employer_response_list)),
                           columns=[
                               'Company',
                               'Review_Link',
                               'Review_Date',
                               'Review_Id',
                               'Review_Date_Time',
                               'Employee_Status',
                               'Location',
                               'Job_Profile',
                               'Type',
                               'Duration_Text',
                               'Company_Employee',
                               'Duration_Years',
                               'Status',
                               'Job_Year_End',
                               'Rating_Work_Life_Balance',
                               'Rating_Culture_And_Values',
                               'Rating_Diversity_Inclusion',
                               'Rating_Senior_Leadership',
                               'Rating_Career_Opportunities',
                               'Rating_Compensation_Benefits',
                               'Rating_Overall',
                               'Recommend_To_Friend',
                               'Ceo_Status',
                               'Business_Outlook_Status',
                               'Pros',
                               'Cons',
                               'Heading',
                               'Advice_to_Management',
                               'Employer_Response'])
    df_list.append(temp_df)
    df = pd.DataFrame(temp_df)

df = pd.concat(df_list)
df.to_excel(r"C:\Mywork\glassdoor-review-scraper-master" + "\\" + str(company_code) + ".xlsx", index=False)
