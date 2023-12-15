import sys
import os
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize

# Ensure the punkt tokenizer is downloaded
nltk.download('punkt')

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Running in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--disable-infobars')

# Function to summarize the abstract
def summarize_abstract(abstract):
    sentences = sent_tokenize(abstract)
    sentence_scores = {sentence: len(sentence.split()) for sentence in sentences}
    num_sentences_in_summary = 2
    summary_sentences = [sentence for sentence, score in sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences_in_summary]]
    summary = ' '.join(summary_sentences)
    return summary

def build_search_url(conference, keywords):
    # Define base URLs for each conference
    conference_urls = {
        "CVPR": "https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&matchBoolean=true&queryText=",
        "IROS": "https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&matchBoolean=true&queryText=",
        "ICRA": "https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&matchBoolean=true&queryText="
    }

    # Combine keywords into a single string with OR operators, removing extra double quotes
    keyword_query = ' OR '.join([f'("All%20Metadata":{keyword})' for keyword in keywords])

    # Check if the conference is valid
    if conference not in conference_urls:
        return "Invalid conference name."

    # Build the complete URL string
    search_url = conference_urls[conference] + keyword_query

    # Add conference-specific filters
    if conference == "IROS":
        search_url += "&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&refinementName=Publication%20Title&refinements=PublicationTitle:2020%20IEEE%2FRSJ%20International%20Conference%20on%20Intelligent%20Robots%20and%20Systems%20(IROS)&refinements=PublicationTitle:2022%20IEEE%2FRSJ%20International%20Conference%20on%20Intelligent%20Robots%20and%20Systems%20(IROS)&refinements=PublicationTitle:2021%20IEEE%2FRSJ%20International%20Conference%20on%20Intelligent%20Robots%20and%20Systems%20(IROS)&refinements=PublicationTitle:2018%20IEEE%2FRSJ%20International%20Conference%20on%20Intelligent%20Robots%20and%20Systems%20(IROS)&refinements=PublicationTitle:2019%20IEEE%2FRSJ%20International%20Conference%20on%20Intelligent%20Robots%20and%20Systems%20(IROS)"
    elif conference == "ICRA":
        search_url += "&highlight=true&returnType=SEARCH&matchPubs=true&refinementName=Publication%20Title&returnFacets=ALL&refinements=PublicationTitle:2021%20IEEE%20International%20Conference%20on%20Robotics%20and%20Automation%20(ICRA)&refinements=PublicationTitle:2023%20IEEE%20International%20Conference%20on%20Robotics%20and%20Automation%20(ICRA)&refinements=PublicationTitle:2022%20International%20Conference%20on%20Robotics%20and%20Automation%20(ICRA)&refinements=PublicationTitle:2019%20International%20Conference%20on%20Robotics%20and%20Automation%20(ICRA)&refinements=PublicationTitle:2020%20IEEE%20International%20Conference%20on%20Robotics%20and%20Automation%20(ICRA)&refinements=PublicationTitle:2018%20IEEE%20International%20Conference%20on%20Robotics%20and%20Automation%20(ICRA)"
    elif conference == "CVPR":
        search_url += "&highlight=true&returnType=SEARCH&matchPubs=true&refinementName=Publication%20Title&returnFacets=ALL&refinements=PublicationTitle:2023%20IEEE%2FCVF%20Conference%20on%20Computer%20Vision%20and%20Pattern%20Recognition%20(CVPR)&refinements=PublicationTitle:2022%20IEEE%2FCVF%20Conference%20on%20Computer%20Vision%20and%20Pattern%20Recognition%20(CVPR)&refinements=PublicationTitle:2021%20IEEE%2FCVF%20Conference%20on%20Computer%20Vision%20and%20Pattern%20Recognition%20(CVPR)&refinements=PublicationTitle:2019%20IEEE%2FCVF%20Conference%20on%20Computer%20Vision%20and%20Pattern%20Recognition%20(CVPR)&refinements=PublicationTitle:2020%20IEEE%2FCVF%20Conference%20on%20Computer%20Vision%20and%20Pattern%20Recognition%20(CVPR)&refinements=PublicationTitle:2018%20IEEE%2FCVF%20Conference%20on%20Computer%20Vision%20and%20Pattern%20Recognition%20Workshops%20(CVPRW)"

    return search_url


def scrape_papers(conference, keywords):
    result_url = build_search_url(conference, keywords)
    if "Invalid conference name." in result_url:
        return "Invalid conference name."

    # Specify the desired file name
    download_folder = r'C:\Users\ashwi\OneDrive\Desktop\Coding Files\files\Python Lit Review Project\ScrapingV1RawFiles-main\ScrapingV1RawFiles-main'
    desired_filename = 'testingmassivelist.csv'

    # Set Chrome options to automatically download files to the specified folder with the custom file name
    chrome_options = webdriver.ChromeOptions()
    prefs = {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Set default filename separately
    chrome_options.add_argument(f"download.default_filename={desired_filename}")

    # Create a ChromeDriver instance
    driver = webdriver.Chrome(options=chrome_options)

    # Open the web page and interact with elements
    driver.get(result_url)

    max_wait_time = 20  # Adjust as needed

    wait = WebDriverWait(driver, max_wait_time)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="xplMainContent"]/div[1]/div[1]/ul/li[3]/xpl-export-search-results/button')))
    element.click()

    wait = WebDriverWait(driver, max_wait_time)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/ngb-modal-window/div/div/div[2]/div/div/div[2]/button[2]")))
    element.click()

    sleep(5) #pause for testing

    max_wait_time = 60  # seconds
    for _ in range(max_wait_time):
        # Check if the file exists in the downloads folder
        files = [f for f in os.listdir(download_folder) if f.endswith('.csv')]

        if files:
            file_path = os.path.join(download_folder, files[0])
            break

        sleep(1)

    # Rename the file to 'testingmassivelist.csv'
    new_file_path = os.path.join(download_folder, 'testpaper.csv')
    os.rename(file_path, new_file_path)

    sleep(1)

    # Load the massive list CSV file
    massive_list = pd.read_csv("testpaper.csv")

    # Keep only the columns of interest
    narrowed_list = massive_list[["Document Title", "Authors", "Publication Year", "PDF Link", "Abstract"]]

    # Add a new column "Implementation?" with values "YES" or "NO" based on the presence of "github" in the abstract
    # Add a new column "Implementation?" with the GitHub link or "NO" if no GitHub link is found
    # Function to find the GitHub link in the abstract
    def find_github_link(abstract):
        # Use a regular expression to find a GitHub link in the abstract
        import re
        github_pattern = re.compile(r'https?://github.com/[^\s]+')
        match = github_pattern.search(abstract)

        if match:
            return match.group()
        else:
            return "NO"

    # Add a new column "Implementation?" with the GitHub link or "NO" if no GitHub link is found
    narrowed_list["Implementation?"] = narrowed_list["Abstract"].apply(find_github_link)




    # Function to summarize the abstract
    def summarize_abstract(abstract):
        sentences = sent_tokenize(abstract)
        sentence_scores = {sentence: len(sentence.split()) for sentence in sentences}
        num_sentences_in_summary = 2
        summary_sentences = [sentence for sentence, score in sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences_in_summary]]
        summary = ' '.join(summary_sentences)
        return summary

    # Apply the summarize_abstract function to create the "Abstract Summary" column
    narrowed_list["Abstract Summary"] = narrowed_list["Abstract"].apply(summarize_abstract)

    # Remove the original "Abstract" column
    narrowed_list = narrowed_list[["Document Title", "Authors", "Publication Year", "PDF Link", "Implementation?", "Abstract Summary"]]

    # Save the simplified list with the abstract summary to a new CSV file
    narrowed_list.to_csv("scrapedresults.csv", index=False)

    driver.quit()

        # Remove the original "testpaper.csv" file
    # Remove the original "testpaper.csv" file
    try:
        os.remove("testpaper.csv")
    except FileNotFoundError:
        pass  # File not found, nothing to delete

    # Remove the original "scrapedresults.csv" file
    try:
        os.remove("scrapedresults.csv")
    except FileNotFoundError:
        pass  # File not found, nothing to delete
    return narrowed_list.to_dict(orient='records')



# ################# MAIN #################################
# conference_name = "IROS"  # Change this to the conference you want to search from
# search_keywords = ["multi-agent", "multirobot", "dynamic environment"]  # Add your keywords here
# result_url = build_search_url(conference_name, search_keywords)






