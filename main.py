try:
    from playwright.sync_api import sync_playwright
    from time import sleep
    import os
    from bs4 import BeautifulSoup
    from bs4 import BeautifulSoup
    import pandas as pd
    import login
except:
    import os
    os.system("pip install playwright")
    os.system("playwright install")
    from playwright.sync_api import sync_playwright
    from time import sleep
    os.system("pip install bs4 pandas")
    from bs4 import BeautifulSoup
    import pandas as pd
    import login

# These are the parameters you can modify
url = "https://twitter.com/ABTAMembers"
no_of_scrolls = 15  #Modify the number of scrolls as much as tweets you want to scrape, more scrolls more data

# Initialize empty lists to store data
post_urls = []
post_texts = []
post_dates = []
post_times = []
post_views = []
post_likes = []
post_reposts = []
post_quotes = []
post_replies = []

# Main urls list
main_urls_list = []

def get_text(soup):
    
    element = soup.find(
        "div", {"dir": "auto", "lang": "en", "data-testid": "tweetText"})
    if element:
        # Extract and print the text from the element
        if element:
            text = element.get_text()
            return text
        else:
            return "Text not found!"

def get_date_time(soup):
    
    element = soup.find('time')
    
    # Extract the text inside the <time> element (date and time)
    date_and_time = element.get_text()
    datetime_attr = element['datetime']

    # Split the datetime attribute value to extract the time
    date, time_with_timezone = datetime_attr.split('T')
    time, timezone = time_with_timezone.split('.')

    return date, time


def get_other_details(soup, link):
    view_count = 0
    like_count = 0
    repost_count = 0
    quotes_count = 0
    reply_count = 0
    
    element = soup.find("span", {"data-testid" : "app-text-transition-container"})

    # Extract Views
    if element:
        try:
            if element.span.span.get_text():
                view_count = element.span.span.get_text()
        except:
            pass
    # Extract Likes 
    regx = link[19:] + "/likes"
    a = soup.find("a", {"href" : f"{regx}"})
    if a:
        span1 = a.find("span", {"data-testid" : "app-text-transition-container"})
        if span1.span.span.get_text() != None:
            like_count = span1.span.span.get_text()
    
    # Extract Reposts
    regx = link[19:] + "/retweets"
    a = soup.find("a", {"href" : f"{regx}"})
    if a:
        repost_count = a.div.span.span.span.get_text()
    
    # Extract Quotes 
    regx = link[19:] + "/retweets/with_comments"
    a = soup.find("a", {"href" : f"{regx}"})
    if a:
        quotes_count = a.div.span.span.span.get_text()
    
    # Extract Replies
    div1_element = soup.find("div", {
                    "role": "button", "data-testid" : "reply"})
    if div1_element:
        if div1_element.div.div:
            if div1_element.div.div.span:
                reply_count = div1_element.div.div.span.span.get_text()
    
    return view_count, like_count, repost_count, quotes_count, reply_count


def export_data_to_excel():
    filename = str(url.split("/")[-1]) + ".xlsx"

    # Create a DataFrame using Pandas
    data = {
        "URL": post_urls,
        'Text': post_texts,
        'Date': post_dates,
        'Time': post_times,
        'Views': post_views,
        'Likes': post_likes,
        'Reposts': post_reposts,
        'Quotes': post_quotes,
        'Replies': post_replies
    }
    if os.path.exists(filename):
        existing_df = pd.read_excel(filename)
        new_df = pd.DataFrame(data)

        # Append the new DataFrame to the existing DataFrame
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        
        # Write the combined DataFrame back to the Excel file
        combined_df.to_excel(filename, index=False)
                
    else:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)

    
    # Free up memory by clearing previous data from the lists
    post_urls.clear()
    post_texts.clear()
    post_dates.clear()
    post_times.clear()
    post_views.clear()
    post_likes.clear()
    post_reposts.clear()
    post_quotes.clear()
    post_replies.clear()


def main_sync():
    with sync_playwright() as p:
        app_data_path = os.getenv('LOCALAPPDATA')
        user_data_path = os.path.join(
            app_data_path, 'Chromium//User Data//Default')

        browser = p.chromium.launch_persistent_context(
            user_data_path)
        page = browser.new_page()

        page.goto(url)
        main_urls_list = []
        for i in range(0, no_of_scrolls):
            page.wait_for_selector(
                "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(3) > div > div > section")
            sleep(2)
            # Get the inner HTML of the page
            html = ''
            html = page.inner_html(
                '#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(3) > div > div > section')

            # Slicing string to remove extra elements from start which cause problems
            index = int(html.find("tweetText"))-189
            html = html[index:]
            html = html[:-88]  # Removes the closing tags of those elements

            index = html.find(f"{url[19:]}/status/")
            
            # Extract the post url
            while index > 0:
                index = html.find(f"{url[19:]}/status/")
                if index < 0:
                    break
                html = html[index:]
                link = "https://twitter.com" + html[:39]
                main_urls_list.append(link)
                html = html[(index+167):]
                
            main_urls_list = list(set(main_urls_list))
            print(f"Scrolling down key press {i+1} | URLs collected: {len(main_urls_list)}", end="\r")
            page.evaluate(
                '''() => {window.scrollTo(0, document.body.scrollHeight);}''')
            sleep(1)
        browser.close()
        print("\n")
        return main_urls_list
    
    
def browse_links(links):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        chunk = 1
        scraped = 0
        urls_not_loaded = []
        for i, link in enumerate(links):
            print(f"Extracting data from url: {i+1} | URLs Scraped: {scraped}", end="\r")
            page.goto(link)
            try:
                page.wait_for_selector(
                    "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > section > div > div > div:nth-child(1)")
            except:
                urls_not_loaded.append(link)
                continue
            
            sleep(1)
            html = ''
            html = page.inner_html(
                '#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > section > div > div > div:nth-child(1)')
            
            index = int(html.find("tweetText"))-189
            html = html[index:]
            html = html[:-88]
           
            soup = BeautifulSoup(html, "html.parser")
            text = get_text(soup)
            date, time = get_date_time(soup)
            views, likes, reposts, quotes, replies = get_other_details(soup, link)

            # Append to main lists
            post_urls.append(link)
            post_texts.append(text)
            post_dates.append(date)
            post_times.append(time)
            post_views.append(views)
            post_likes.append(likes)
            post_reposts.append(reposts)
            post_quotes.append(quotes)
            post_replies.append(replies)
            scraped += 1
            # Checks if the main lists have 50 entires then export them and free up memory
            if len(post_dates) >=50:
                print(f"\nExporting chunk of data: {chunk}")
                export_data_to_excel()
            
        # Checks that if there is data in the lists at last then also export that data
        if post_dates:
            print("\nExporting last chunk of data")
            export_data_to_excel()
        if urls_not_loaded:
            with open("urls_not_loaded.txt", "w") as file:
                for url in urls_not_loaded:
                    file.write(str(url) + "\n")
        else:
            if os.path.exists("urls_not_loaded.txt"):
                os.system("del urls_not_loaded.txt")
        
        browser.close()

def __main__():
    # Required to login twitter account first time
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("===============================")
        print("       Twitter Scraper")
        print("===============================")
        print("[1] Login")
        print("[2] Scrape Data")
        print("[3] Scrape Unloaded urls")
        print("[4] Exit")
        choice = input("\n>>")
        os.system("cls" if os.name == "nt" else "clear")
        try:
            choice = int(choice)
        except:
            print("Enter only integers!")
            exit()
            
        if choice == 1:
            login.login_twitter()
        elif choice == 2:
            main_urls_list = []
            main_urls_list = main_sync()    
            browse_links(main_urls_list)  
            input("\nPress any key to conntinue...")
        elif choice == 3:
            main_urls_list = []
            if os.path.exists("urls_not_loaded.txt"):
                with open("urls_not_loaded.txt", "r") as file:
                    for line in file:
                        url = line.strip()
                        main_urls_list.append(url)
                browse_links(main_urls_list)   
            else:
                print("urls_not_loaded.txt not found!")         
            input("Press any key to conntinue...")
        elif choice == 4:
            exit()
        else:
            print("Invalid choice!")
            input("Press any key to conntinue...")
            
__main__()
