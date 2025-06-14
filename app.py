from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import pandas as pd
from time import localtime, strftime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import textwrap
import string
#import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

class Application:
  def __init__(self):
    #nltk.download('stopwords')
    #nltk.download('punkt_tab')
    self.driverPath  = "chromedriver.exe"
    #initilize connection to supabase
    load_dotenv()
    supabase_url = "https://vouudkpnerfgxkjbbpji.supabase.co"
    supabase_public_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZvdXVka3BuZXJmZ3hramJicGppIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkwMjI2NDUsImV4cCI6MjA2NDU5ODY0NX0.6Nrcm52DkUI0MQQChCUaFe_1qxtKI7XRi9_ArsSxE0Q"

    try:
        self.supabase: Client = create_client(supabase_url, supabase_public_key)
        print("connection to DB successfull")

    except Exception as e:
        print("connection to DB failed!")
        print(e)


  def run(self):
      #initialize selenium and chrome driver
      URL = f"https://old.reddit.com/r/memes/top/"
      options = ChromeOptions()
      options.add_argument("--window-size=1920,1080")
      options.add_argument("--headless")
      options.add_argument("--disable-gpu")
      options.add_argument(
          "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
      self.driver = webdriver.Chrome(options=options)
      self.driver.get(URL)

      #fetch the content main div
      elements = self.driver.find_elements(By.XPATH, "//div[starts-with(@id, 'thing_t3') and not(contains(@class, 'promoted'))]")

      #create dict store
      now = strftime("%Y-%m-%d", localtime())
      data = {now:{}}
      
      #list of titles for wordcloud, raw
      titles_list = []
      #iterate over the elements and fetch data
      counter = 1
      for elem in elements:
          if counter == 21:
              break
          try:
              score_elem = elem.find_element(By.CSS_SELECTOR, ".score.unvoted")
              upvotes_raw = score_elem.get_attribute("title")

              #sometimes old reddit displays dot as upvote count
              if upvotes_raw == "":
                 upvotes_raw = elem.get_attribute("data-score")

              title = elem.find_element(By.CLASS_NAME, "title")
              titleText = title.text
              titleText_Cleaned = str(titleText).replace(' (i.redd.it)','')
              titleText_Cleaned = titleText_Cleaned.replace(' (v.redd.it)','')
              
              #clean and append for wordcloud tokenizing
              titles_list.append(titleText_Cleaned)

              link = elem.find_element(By.CSS_SELECTOR, ".bylink.comments")
              link = link.get_attribute("href")
              link = str(link).replace('old.','')

              comments = elem.find_element(By.CSS_SELECTOR, ".bylink.comments").text
              comments = str(comments).replace(' comments','')

              op = elem.find_element(By.CSS_SELECTOR,".author").text

              data[now][counter] = {"upvotes":str(upvotes_raw),"title":titleText_Cleaned,"link":link,"comments":comments,"author":op}

          except:
              print("cant find div")
          counter += 1

      self.driver.quit()

      #convert data to pandas df for plotting purposes
      df = pd.DataFrame.from_dict(data[now], orient="index")
      df.index.name = "rank"
      df.reset_index(inplace=True)
      df['link'] = df['link'].str.wrap(50)


      #plot and save a pdf
      with PdfPages("memes_report.pdf") as pdf:


        plt.figure(figsize=(10, 5))
        plt.axis('off')

        paragraph = (
        "This report summarizes the top 20 posts from r/memes over the past 24 hours.\n\n"
        "The first page, which contains a bar chart, displays in descending order, the number of upvotes for each of the top 20 posts. The date of the scraping is in the title of the chart. This way, we can compare the top 20 upvote counts across different days, and track if there are any patterns. For example, if posts tend to fetch more upvotes on Friday compared to Monday.\n\n"
        "The second page, displays a wordcloud of the top 20 post titles. The wordcloud shows the frequency and prominence of the words, which could indicate common themes in the memes and its discussions.\n\n"
        "The third page shows a table with detailed data including how many comments were made on the post at the time of scraping, the title of the post, as well the link to view the post itself on reddit.\n\n"
        "Further improvements to the reddit crawler could be made, such as sifting through the top 5 comments of each of the 20 posts, and generating a word cloud from it. This way, we can see what the top comments are about, and identify key words. An analysis could be drawn if we find any commonly occuring words appearing across posts, suggesting that this is what redditors are interested in talking about, or find funny. But this will increase the waiting time of receiving the file on telegram. Food for thought."
        )
        #ensure linebreaks persists
        wrapped_text = textwrap.fill(paragraph, width=100,replace_whitespace=False)
        plt.text(0.05, 0.95, wrapped_text, va='top', ha='left', wrap=True, fontsize=10, transform=plt.gca().transAxes)
        pdf.savefig()
        plt.close()

        #bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(df['rank'].astype(str).tolist(), df['upvotes'].astype(int).tolist(), color='skyblue')
        plt.title(f"Top 20 r/memes upvote count in the past 24 hours - {now}")
        plt.ylabel("Upvotes")
        plt.xlabel("Ranking")
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        #word cloud (titles)
        tokens = []
        #unique set of english stopwords
        stop_words = set(stopwords.words('english'))
        unique_words= ["'","'",'',"",'’',]
        
        for sentence in titles_list:
            tokens.extend(word_tokenize(sentence.lower()))
        tokens_filtered = [x for x in tokens if x.lower() not in stop_words 
                           and x.lower() not in string.punctuation
                           and x.lower() not in unique_words]
        
        cloud_text = ' '.join(word for word in tokens_filtered)
        wordcloud = WordCloud(width=800, height=400,background_color='white',
                              collocations=False).generate(cloud_text)
        
        plt.figure(figsize=(10,6), dpi=900)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')  
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        #table
        df = df.drop(columns=['rank'],axis=1)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')
        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            loc='center',
            cellLoc='left'
        )
        table.scale(1.2, 1.5)
        table.auto_set_font_size(False)
        table.set_fontsize(6) 
        pdf.savefig(fig)
        plt.close(fig)

      #save the data to the supabase postgres db
      try:
        self.supabase.table("reddit_top_posts").insert({"data":data}).execute()
      except Exception as e:
        print(e)
        pass
