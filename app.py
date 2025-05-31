from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import pandas as pd
from time import localtime, strftime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class Application:
  def __init__(self):
    self.driverPath  = "chromedriver.exe"

  def run(self):
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
      #iterate over the elements and fetch dat
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
              titleText_Cleaned = str(titleText).replace('(i.redd.it)','')

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


      #plot
      with PdfPages("memes_report.pdf") as pdf:
        plt.figure(figsize=(10, 6))
        plt.bar(df['rank'].astype(str).tolist(), df['upvotes'].astype(int).tolist(), color='skyblue')
        plt.title(f"Top 20 r/memes upvote count in the past 24 hours - {now}")
        plt.ylabel("Upvotes")
        plt.xlabel("Ranking")
        plt.tight_layout()
        pdf.savefig()
        plt.close()

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