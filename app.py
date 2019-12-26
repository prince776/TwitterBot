from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class TwitterBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()

    def login(self):
        bot = self.bot
        bot.get("https://twitter.com/")
        time.sleep(5)
        # get the input boxes
        email = bot.find_element_by_class_name("email-input")
        password = bot.find_element_by_name("session[password]")
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

    def like_tweet(self, hashtag, scrollCount):
        bot = self.bot
        bot.get("https://twitter.com/search?q=" + hashtag + "&src=typed_query")
        time.sleep(3)

        for i in range(1, scrollCount + 1):
            bot.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)

            allLinks = [
                elem.get_attribute("href")
                for elem in bot.find_elements_by_xpath("//a[@dir='auto']")
            ]
            tweetLinks = list(filter(lambda x: "status" in x, allLinks))

            for link in tweetLinks:
                bot.get(link)
                time.sleep(3)
                try:
                    bot.find_element_by_xpath("//div[@data-testid='like']").click()
                    time.sleep(5)
                except Exception as ex:
                    time.sleep(10)


username = input("Enter Email: ")
password = input("Enter password: ")
hashtag = input("Enter hastag to like: ")
scrollCount = input(
    "How many pages you wanna scroll(More pages more tweets will be liked): "
)
scrollCount = int(scrollCount)

bot = TwitterBot(username, password)
bot.login()
bot.like_tweet(hashtag, scrollCount)
