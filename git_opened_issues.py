############################################################################
# Project Goal: Create a repository on GitHub and write a program in any programming language that will do the following:

#Input : 
#       User can input a link to any public GitHub repository
#Output :
#       Your UI should display a table with the following information -
#       Total number of open issues
#       Number of open issues that were opened in the last 24 hours
#       Number of open issues that were opened more than 24 hours ago but less than 7 days ago
#       Number of open issues that were opened more than 7 days ago.
#
# Date of Submission: 29-03-2016
# Author: Sundeep Kondaveeti
##############################################################################
import re, urllib, time, datetime

class GitWS:

    def __init__(self):

        self.list_git_path = ['https://github.com/Shippable/support/issues?page=1&q=is%3Aissue+is%3Aopen',
                              'https://github.com/Shippable/support/issues?page=2&q=is%3Aissue+is%3Aopen']
        self.context = ""
        self.total_opened_issues = 0
        self.diff_hours = []
        self.dict_issue_status = {'D': 0, 'W': 0, 'M': 0}
        self.list_submitted_date = []
        self.list_formatted_date_time = []

    def time_compare(self):
        '''Function for calculating the current time and comparing with the issue open time '''
        for opened_time in self.list_formatted_date_time:
            curr_time = time.strftime('%Y-%m-%dT%H:%M:%SZ')

            curr_time = time.strptime(curr_time, '%Y-%m-%dT%H:%M:%SZ')
            given_time = time.strptime(opened_time, '%Y-%m-%dT%H:%M:%SZ')

            curr_time = time.mktime(curr_time)
            given_time = time.mktime(given_time)
            # Calculating the time difference
            difference_time = curr_time - given_time
            # Converting time to hours
            diff_hours = int(difference_time)/60 /60
            self.diff_hours.append(diff_hours)

    def get_context(self):
        '''Function will retrive the opened issue and time of submission'''
        for path in self.list_git_path:
            self.context = urllib.urlopen(path).read()
            # The below regular expression is used to fetch the total open issues using the ID.
            #pattern_id = re.compile(r'#\d{4}\s | #\d{3}\s | #\d{2}\s')
            #issue_ids = pattern_id.findall(self.context)
            #self.total_opened_issues = self.total_opened_issues + len(issue_ids)
            pattern_date = re.compile(r'time datetime="\w{4}-\w{2}-\w{5}:\w{2}:\w{3}"')
            date_time = pattern_date.findall(self.context)
            self.list_submitted_date.extend(date_time)

    def format_time_date(self):
        '''Function will format the date time '''
        for date_time in self.list_submitted_date:
            date_time = date_time.split('\"')
            self.list_formatted_date_time.append(date_time[1])

    def update_final_data(self):
        '''Function for updating the issues based upon the timeline '''
        for hour in self.diff_hours:
            if hour < 24:
                self.dict_issue_status['D'] = self.dict_issue_status['D'] + 1
            elif 24 < hour < 168:
                self.dict_issue_status['W'] = self.dict_issue_status['W'] + 1
            else:
                self.dict_issue_status['M'] = self.dict_issue_status['M'] + 1  

    def display_output(self):
        '''Function will display the output '''
        print "-----------------------------------------------------------------------------------------------------------------------------"
        print "Total number of open issues:                                                            {}".format(len(self.list_submitted_date))
        print "-----------------------------------------------------------------------------------------------------------------------------"
        print "Number of open issues that were opened in the last 24 hours:                            {}".format(self.dict_issue_status['D'])
        print "-----------------------------------------------------------------------------------------------------------------------------"
        print "Number of open issues that were opened more than 24 hours ago but less than 7 days ago: {}".format(self.dict_issue_status['W'])
        print "-----------------------------------------------------------------------------------------------------------------------------"
        print "Number of open issues that were opened more than 7 days ago:                            {}".format(self.dict_issue_status['M'])
        print "-----------------------------------------------------------------------------------------------------------------------------"

if __name__ == "__main__":
    obj = GitWS()
    obj.get_context()
    obj.format_time_date()
    obj.time_compare()
    obj.update_final_data()
    obj.display_output()
