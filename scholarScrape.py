
def system_clear():
    """
    Clears the console screen based on the operating system.
    """
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def request_url(urllink):
    """
    Sends a GET request to the specified URL and parses the HTML content.
    Args:
        urllink (str): The URL to send the GET request to.
    Returns:
        BeautifulSoup: Parsed HTML content of the response.
    Prints:
        int: The status code of the response.
    """
    headers = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"}
    page = requests.get(urllink,headers=headers)
    page_soup = bs4(page.text, "html.parser")
    page.status_code
    return page_soup


def contents(content, time, pages=0):
    """
    Fetches and parses Google Scholar search results based on the given content and time range.
    Args:
        content (str): The search query to be used on Google Scholar.
        time (str): The year for which the search results are to be fetched. Use "all" for all years.
        pages (int, optional): The page number of the search results to fetch. Defaults to 0.
    Returns:
        tuple: A tuple containing the following lists:
            - links (list): List of URLs to the search results.
            - title (list): List of titles of the search results.
            - cite (list): List of citation counts for the search results.
            - free_con (list): List indicating whether the content is free or not.
            - lin (list): List of URLs found within the search results.
            - date (list): List of publication dates of the search results.
    """
    links = []
    title = []
    cite = []
    free_con = []
    lin = []
    date = []
    start = pages * 10
    #url = "https://scholar.google.com/scholar?q=%22precipitable+water+vapor%22&hl=en&as_sdt=0%2C5&as_ylo=2020&as_yhi=2020"
    #https://scholar.google.com/scholar?q=gravitational+waves&hl=en&as_sdt=0%2C5&as_ylo=2019&as_yhi=2019
    if time != "all":
        url = f"https://scholar.google.com/scholar?start={start}&q={content}&hl=en&as_sdt=0,5&as_ylo={int(time)}&as_yhi={int(time)}"
        r = requests.get(url)
    elif time == "all":
        r = requests.get(f"https://scholar.google.com/scholar?hl=en&start={start}&as_sdt=0,5&q={content}")
    soup = bs4(r.content, "lxml")
    for div in soup.find_all("h3", class_="gs_rt"):
        for j in div.find_all("a"):
            title.append(j.getText())
            links.append(j.get("href"))
    for link in soup.find_all('a'):
        if link.find(string=lambda text: text and text.startswith('Cited by')):
            cite.append(link.get_text().replace("Cited by", ""))
    for div in soup.find_all("div", class_="gs_r gs_or gs_scl"):
        free_co = div.find('span').getText()
        if 'Save' in free_co:
            free_con.append(free_co.replace('Save', 'Non free'))
        elif '[' and ']' in free_co:
            free_con.append(free_co.strip('[]'))
        lin.append(div.find('a').get('href'))
    
    for div in soup.find_all("div", class_="gs_a"):
        free_co = div.getText()
        date.append(free_co.rsplit('-')[1].rsplit(',')[-1])
    
    result = list(zip(title, cite, date, free_con))
    col = ["Title", "Number_of_citation", "Published Date", "Available(Free or not)"]
    res = pd.DataFrame(result, columns=col)
    # Print the DataFrame with titles in green, number of citations in blue, and availability in red
    for index, row in res.iterrows():
        print(f"{index} {GREEN}{row['Title']}{RESET}, {YELLOW}Number of citation{RESET}: {BLUE}{row['Number_of_citation']}{RESET}, {ORANGE}Published Date{RESET}: {row['Published Date']}, {PURPLE}Available{RESET}: {RED}{row['Available(Free or not)']}{RESET}")
        # print("\n")
    # print(res)#.sort_values(by="Published Date", ascending=False))
    return links, title, cite, free_con, lin, date
 

def search_author(author):
    """
    Searches for an author on Google Scholar and retrieves their details.
    Args:
        author (str): The name of the author to search for.
    Returns:
        tuple: A tuple containing three lists:
            - author_name (list of str): List of author names found.
            - affiliation (list of str): List of affiliations corresponding to the authors.
            - author_url (list of str): List of URLs to the authors' Google Scholar profiles.
    The function prints a DataFrame with the following columns:
        - Author: The name of the author.
        - Affiliated to: The affiliation of the author.
        - Subject Field: The subject field of the author.
    """
    headurl = "https://scholar.google.com"
    auth = author.split(" ")
    auth = "+".join(auth)
    prof_url = f"https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors={auth}&btnG="
    page_soup = request_url(prof_url)
    page_element = page_soup.find("div", id="gsc_sa_ccl").find_all("div", class_="gs_ai_t")
    author_name = []
    affiliation = []
    subject_field = []
    author_url = []
    for aut in page_element:
        if aut.find("h3",class_="gs_ai_name").find("a").find("span"):   #..................edit this line. put condition
            author_name.append(aut.find("a").text)
            affiliation.append(aut.find("div", class_="gs_ai_aff").text)
            subject_field.append(aut.find("div", class_ ="gs_ai_int").text)
            author_url.append(headurl+aut.find("a").get("href"))
    new_authorname = [f"{YELLOW}{name}{RESET}" for name in author_name]
    affiliation = [f"{GREEN}{name}{RESET}" for name in affiliation]
    subject_field = [f"{BLUE}{name}{RESET}" for name in subject_field]
    result_on = list(zip(new_authorname, affiliation, subject_field))
    
    show = pd.DataFrame(result_on, columns=["Author", "Affiliated to", "Subject Field"], index=range(1,len(result_on)+1))
    print(show)
    return author_name, affiliation, author_url, subject_field


def author_citation(affiliation,authorlink, show_nbr, field):
    """
    Fetches and prints the citation metrics for a given author from their Google Scholar profile.
    Args:
        affiliation (list): A list of affiliations corresponding to the authors.
        authorlink (str): The URL to the author's Google Scholar profile.
        show_nbr (int): The index number of the author to display (1-based index).
    Returns:
        None
    Prints:
        The author's name and affiliation, followed by a DataFrame containing the total citations, h-index, and i10-index.
    """
    citation = request_url(authorlink).find("div", class_="gsc_rsb").find("table",id="gsc_rsb_st").getText(separator="\n")
    citation = citation.split("\n")
    total_citation = int(citation[3])
    h_index = int(citation[6])
    i10_index = int(citation[9])
    print(authorname[show_nbr-1],":",affiliation[show_nbr-1])
    print("Research Area: ", field[show_nbr-1])
    print(pd.DataFrame({"Citations":total_citation, "h-index":h_index, "i10-index":i10_index}, index=[1]).to_string(index=False))

def selected_author_works(authorlink, page=0):
    """
    Fetches and processes the works of a selected author from Google Scholar.
    Args:
        authorlink (str): The URL link to the author's Google Scholar profile.
    Returns:
        tuple: A tuple containing two lists:
            - title (list of str): A list of titles of the author's works.
            - tilte_url (list of str): A list of URLs corresponding to the titles of the author's works.
    Example:
        titles, urls = selected_author_works("https://scholar.google.com/citations?user=XXXXXX")
    """
    pagesize = 15
    start = page*pagesize
    authorlink_contracted = authorlink + f"&cstart={start}&pagesize={pagesize}&view_op=list_works"
    selected_authoreq = request_url(authorlink_contracted)
    title = []
    year = []
    citations = []
    tilte_url = []
    for tr in selected_authoreq.find("table", id="gsc_a_t").find("tbody", id="gsc_a_b").find_all('tr'):
        title.append(tr.find("td", class_="gsc_a_t").find("a").text)
        year.append(tr.find("td", class_="gsc_a_y").text)
        citations.append(tr.find("td", class_="gsc_a_c").text)
        tilte_url.append( "https://scholar.google.com"+tr.find("td", class_="gsc_a_t").find("a").get("href"))
    result = list(zip(title, year, citations))
    df = pd.DataFrame(result, columns=["Title", "Year", "Citations"], index=range(1, len(result)+1))
    for index, row in df.iterrows():
        print(f"{index} {YELLOW}{row['Title'].upper()}{RESET}, {GREEN}Number of citation{RESET}: {BLUE}{row['Citations']}{RESET}, {ORANGE}Published Date{RESET}: {row['Year']}")
        # print("\n")
    # print(df)
    return title, tilte_url

def about_author_listoftitle(title_url):
    """
    Extracts and returns details about an author's publication from a given URL.
    Args:
        title_url (str): The URL of the publication to extract details from.
    Returns:
        tuple: A tuple containing the following details:
            - s (str): The title of the publication.
            - journallink[0] (str): The URL link to the journal or publication.
            - author (str): The author of the publication.
            - publication_date (str): The publication date.
            - journal (str): The journal in which the publication appeared.
            - free_available[0] (str): Availability status of the publication (e.g., "Not available" or link to free version).
    """
    title_details = []
    titlecontent = request_url(title_url)
    for title in titlecontent.find("div", id="gsc_oci_table").find_all("div", class_ ="gs_scl"):
        title_details.append(title.find("div", class_ ="gsc_oci_value").text)
    
    s = title.find("div", class_="gsc_oci_merged_snippet").find("a").text
    journallink = []
    free_available = []
    for free in titlecontent.find_all("div",id="gsc_oci_title_wrapper"):
        if free.find("div", id="gsc_oci_title_gg") is None:
            journallink.append(title_url)
        elif free.find("div", id="gsc_oci_title_gg") is not None:
            journallink.append(free.find("div", id="gsc_oci_title_gg").find("a").get('href'))
        if free.find("div", id="gsc_oci_title_gg") is None:
            free_available.append("Not available")
        elif free.find("div", id="gsc_oci_title_gg") is not None:
            free_available.append(free.find("div", id="gsc_oci_title_gg").find("a").text)
    titles = title_details[-1]
    author = title_details[0]
    publication_date = title_details[1]
    journal = title_details[2]
    # abstract = title_details[5]
    return s, journallink[0], author, publication_date, journal, free_available[0]

def openbrowser_download(key,title_name, title_url, availability):
    """
    Handles different actions based on the provided key:
    Args:
        key (str): The action key ('o' for open, 'd' for download, 'c' for clear).
        title_name (str): The name of the title to be used for the file name.
        title_url (str): The URL of the title to be opened or downloaded.
        availability (str): The availability status of the title (e.g., "Not available", "PDF available").
    If key == 'o':
        Opens the provided URL in a new browser tab.
    If key == 'd':
        Downloads the content from the provided URL if the availability status indicates that a PDF is available.
        - If availability is "Not available", it prints a message indicating that the file cannot be downloaded.
        - If 'PDF' is in availability, it downloads the content from the URL and saves it as a PDF file with the title name.
        - Otherwise, it prints a message indicating that the file cannot be downloaded as a PDF.
    If key == 'c':
        Clears the console screen.
        - If the operating system is Windows (os.name == "nt"), it uses the 'cls' command.
        - Otherwise, it uses the 'clear' command.
    """
    if key == 'o':
        print("Opening in browser....")
        webbrowser.open_new_tab(title_url)
    elif key == 'd':
        if availability == "Not available":
            print("You can't download this file as it is not available free.")
        elif 'PDF' in availability:
            with open(f"{title_name[:35]}_paper.pdf","wb") as f:
                content = requests.get(f'{title_url}').content
                f.write(content)
                print("Downloaded successfully")
        else:
            print("You can't download this file as pdf is not available.")
    elif key == 'c':
        system_clear()  
        # continue     

if __name__ == "__main__":
    try:
        import requests
        import os
        from bs4 import BeautifulSoup as bs4
        import webbrowser
        import sys
        import pandas as pd
        import time
    except ImportError as e:
        print(f"Required module {e.name} not found. You can install it using 'pip install {e.name}'.")

    import argparse
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    RESET = '\033[0m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    ORANGE = '\033[96m'
    PINK = "\033[35m"

    parser = argparse.ArgumentParser(description="Google Scholar Scraper")
    parser.add_argument('-a', '--author', type=str, help='Author name for search')
    parser.add_argument('query', type=str, nargs='?', help='Search query')
    parser.add_argument('time', type=str, nargs='?', help='Year or "all" for all years')
    args = parser.parse_args()

    if args.author:
        query = args.author
        queries = query.replace(' ', '+')
        page = 0
        page_history = []
        print("WELCOME TO GOOGLE SCHOLARS SCRAPING PYTHON for personal purposes only, by Shivaji Chaulagain")
        print("-------------------------------------------------------------------->>")
        
        authorname, affiliation, author_url, subject_field = search_author(queries)
        print("\n")
        show_nbr = int(input("Enter the number associated with author you want to search for: "))
        author_show = author_url[show_nbr-1]
        while True:
            system_clear()
            if page == 0:
                author_citation(affiliation, author_show, show_nbr, subject_field)
                print("\n")
                print("List of the research works")
                print("........................................................................")
            titleauthor, title_url = selected_author_works(author_show, page=page)
            print("\n")
            try:
                input_ask = input(f"{ORANGE}Enter the number of the title you want to continue with or 'o' for visiting the author profile in browser or 'n' for the next page of work list, 's' for choosing another author or 'e' for exiting the script:{RESET} ")
                if input_ask.lower() == 'n':
                    system_clear()
                    page_history.append(page)
                    page += 1
                    print(f"                                                 Page:{page+1}")
                    print("\n")
                    continue
                elif input_ask.lower() == 'e':
                    sys.exit(1)
                elif input_ask.lower() == 'o':
                    webbrowser.open_new_tab(author_show)
                    continue
                elif input_ask.lower() == 's':
                    authorname, affiliation, author_url, subject_field = search_author(queries)
                    show_nbr = int(input("Enter the number associated with author you want to search for: "))
                    author_show = author_url[show_nbr-1]
                    continue
                input_nbr = int(input_ask)
                title_url_show = title_url[input_nbr-1]

            except IndexError:
                print("Invalid number input. Index out of range. Please enter a valid number.")
                time.sleep(3)
                system_clear()
                continue
            subject, journallink, author, publication_date, journal, free_available = about_author_listoftitle(title_url_show)
            print("\n")
            print(".................................................................................................")
            print(f"{YELLOW}Title:{RESET} ", subject)
            print(f"{YELLOW}Author:{RESET}  ", author)
            print(f"{YELLOW}Published Date:{RESET}  ", publication_date)
            print(f"{YELLOW}Journal:{RESET}  ", journal)
            print(f"{YELLOW}Availability:{RESET}  ", free_available)
            print("................................................................................................")
            continue_ = input(f"{ORANGE}Enter 'o' for visiting that title link in browser or 'd' for downloading that title or 'c' for continue searching in terminal:{RESET} ")
            openbrowser_download(continue_, subject, journallink, free_available)

    elif args.query and args.time:
        query = args.query
        queries = query.replace(' ', '+')
        time = args.time
        page = 0
        page_history = []
        print("WELCOME TO GOOGLE SCHOLARS SCRAPING PYTHON for personal purposes only, by Shivaji Chaulagain")
        print("-------------------------------------------------------------------->>")
        while True:
            links, titles, cite, free_con, lin, date = contents(queries,time, page)
            print("\n")
            link_choice = input(f"{YELLOW}Enter the number of the link you want to continue with title, 'n' for the next page, or 'b' for the previous page: or 'e' for the exit:{RESET}")
            if link_choice.isdigit() and int(link_choice) <= len(links):
                  print("-------------------------------------------------------------------------")
                  print(f"Title of number {link_choice}: | ", end=" ")
                  print(f"'{titles[int(link_choice)]}'")
                  print("------------------------------------------------------------------------")
                  print(f"Number of citation: {cite[int(link_choice)]}, Published Date: {date[int(link_choice)]}, Available: {free_con[int(link_choice)]}")
                  print("---------------------------------------------------------------------")
                  continue_ = input(f"{ORANGE}Enter 'o' for visiting that title link in browser or 'd' for downloading that title or 'c' for continue searching in terminal:{RESET} ")
                  openbrowser_download(continue_, titles[int(link_choice)], lin[int(link_choice)], free_con[int(link_choice)])
                  
            elif link_choice.lower() == 'n':
                  system_clear()
                  page_history.append(page)
                  page += 1
                  print(f"                                                 Page:{page+1}")
                  print("\n")
            elif link_choice.lower() == 'b':
                system_clear()
                if page_history:
                        page = page_history.pop()
                else:
                   print("You are already on the first page.")
                print(f"                                                   page: {page+1}")
            elif link_choice.lower() == 'e':
                 sys.exit(1)
    
            else:
                print("Invalid input. Please enter a valid number, 'n' for the next page, or 'b' for the previous page.")
                system_clear()
    else:
        print("Invalid arguments. Use -h for help.")