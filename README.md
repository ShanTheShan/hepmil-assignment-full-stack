# hepmil-assignment

# bot username: @Hepmil_assignment_bot

## tech stack

### python - selenium, matplotlib, pandas

### supabase - postgres (json)

to run then script:

1. create a virtual environment and install pips via requirements.txt
2. download chrome driver (if the provided driver, doesnt match your version of chrome)
3. run main.py in your virtual env
4. use the telegram bot

## Thought process

Firstly, I had to decide what data I actually want to crawl and scrape from Reddit memes. So I visited the website and decided on the title, the upvote count, the link, the number of comments, and the author. Then, I launched the web browser console and looked at the divs. The divs that contained the desired elements and data, such as upvote counts, had a easily accessible class name or div name. Perfect for scraping.

Now i knew what i wanted to scrape and how, i decided on the tech stack. I chose python selenium as its a great way to crawl websites and scrape data, and write scripts with, furthermore I have experience with selenium. I decide to store the database using postgres in a json format, using Supabase, an open source, scalable cloud firebase alternative. This way, if we decide to send the data through an API, JSON format would be the ideal way to send from server and query from client side. Using xpath queries, I was able to crawly the dom, fetch the data, generate a pdf report through matplotlib, and insert the data into Supabase.

Finally, I had to create the telegram bot to server the data. This was the learning point for me, as I had never created a telegram bot before. I followed a YouTube tutorial to set-up my telegram bot and then proceed to integrate it into my script, through the use of classes and calling its relevant methods.

## Improvements

Improvements could be made to the crawler by scraping the comments of each posts as well. This way, we can know what the redditors are discussing in the comment sections, as a visualization through a frequency graph or word cloud. Thus, we can learn the context and discussion going on. But this will increase the waiting time of the bot service. So its a give and take situation.

## AI was not used for this assignment, as I have performed such scripting, scraping and database setup before. However, a YouTube tutorial was followed to create a telegram bot. Below is the link to the video I followed.

https://www.youtube.com/watch?v=vZtm1wuA2yc&t=910s
