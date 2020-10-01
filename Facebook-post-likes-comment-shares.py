#Insert each Post-ID in the Post-ID section, this program will scrape,
#Everything about that particular post such as date of post, content of post,
#List of people who liked the post, list of people who commented and shared the post respectively.

import requests
from bs4 import BeautifulSoup
import pandas as pd

username = "email"
password = "password"

class FaceBookBot():
    login_basic_url = 'https://mbasic.facebook.com/login'
    login_mobile_url = 'https://m.facebook.com/login'
    payload = {
            'email': username,
            'pass': password
        }
    post_ID = "2618383005050896"

    def parse_html(self, request_url):
        with requests.Session() as session:
            post = session.post(self.login_basic_url, data=self.payload)
            parsed_html = session.get(request_url)
        return parsed_html

    def post_content(self):
        REQUEST_URL = f'https://mbasic.facebook.com/story.php?story_fbid={self.post_ID}&id=415518858611168'
        
        soup = BeautifulSoup(self.parse_html(REQUEST_URL).content, "html.parser")
        content = soup.find_all('p')
        post_content = []
        for lines in content:
            post_content.append(lines.text)
        
        post_content = ' '.join(post_content)    
        return post_content

    def date_posted(self):
        REQUEST_URL = f'https://mbasic.facebook.com/story.php?story_fbid={self.post_ID}&id=415518858611168'
        
        soup = BeautifulSoup(self.parse_html(REQUEST_URL).content, "html.parser")
        date_posted = soup.find('abbr')
        return date_posted.text

    def post_likes(self):
        #If there is huge number of likes on any post, please vary the limit of likes scrapped below
        limit = 200
        REQUEST_URL = f'https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?limit={limit}&total_count=17&ft_ent_identifier={self.post_ID}'

        soup = BeautifulSoup(self.parse_html(REQUEST_URL).content, "html.parser")
        names = soup.find_all('h3')
        people_who_liked = []
        for name in names:
            people_who_liked.append(name.text)
        people_who_liked = [i for i in people_who_liked if i] 
        return people_who_liked
    
    def post_comments(self):
        REQUEST_URL = f'https://mbasic.facebook.com/story.php?story_fbid={self.post_ID}&id=689282774'
        soup = BeautifulSoup(self.parse_html(REQUEST_URL).content, "html.parser")
        names = soup.find_all('h3')
        people_who_commented = []
        for name in names:
            people_who_commented.append(name.text)
        people_who_commented = [i for i in people_who_commented if i] 
        return people_who_commented

    def post_shares(self):        
        REQUEST_URL = f'https://m.facebook.com/browse/shares?id={self.post_ID}'
        
        with requests.Session() as session:
            post = session.post(self.login_mobile_url, data=self.payload)
            parsed_html = session.get(REQUEST_URL)
        
        soup = BeautifulSoup(parsed_html.content, "html.parser")
        names = soup.find_all('span')
        people_who_shared = []
        for name in names:
            people_who_shared.append(name.text)
        return people_who_shared
    
bot = FaceBookBot()
Post_Content = bot.post_content()
Post_Date = bot.date_posted()
People_who_liked = bot.post_likes()
People_who_comment = bot.post_comments()
People_who_shared = bot.post_shares()

print("Post Contents: ", Post_Content)
print("Post Date: ", Post_Date)
print("People who Liked: ", People_who_liked)
print("People who commented: ", People_who_comment)
print("People who shared: ", People_who_shared)

dict = {'Post_Content' : [Post_Content], 'Post_Date' : [Post_Date], 'People_who_liked': [People_who_liked],
         'People_who_comment': [People_who_comment], 'People_who_shared': [People_who_shared]} 

df = pd.DataFrame.from_dict(dict)

df.to_csv('C:/Users/Desktop/Facebook Scrapping project/MM.csv')
        
#This saves the everything in form of .CSV Format.
#After scrapping required amount of post details, these csv files can be merged,
#In order to work on insights.
