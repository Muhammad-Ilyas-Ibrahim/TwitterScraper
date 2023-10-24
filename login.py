try:
    from playwright.sync_api import sync_playwright
    from time import sleep
    import os
except:
    import os
    os.system("pip install playwright")
    os.system("playwright install")
    from playwright.sync_api import sync_playwright
    from time import sleep

url = "https://twitter.com/i/flow/login"

def login_twitter():
    with sync_playwright() as p:
        app_data_path = os.getenv('LOCALAPPDATA')
        user_data_path = os.path.join(
            app_data_path, 'Chromium//User Data//Default')

        # Launch a persistent context with a specific user data directory
        browser = p.chromium.launch_persistent_context(
            user_data_path, headless=False, slow_mo=1000)
        page = browser.new_page()
        page.goto(url)
        sleep(120)
        browser.close()

if __name__ == '__main__':
    login_twitter()