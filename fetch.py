"""
fetch.py

This module contains functions for fetching data from the South African Department of 
Education website. It includes functions for fetching content from a URL,
obtaining subject links from the main page, and extracting exam links for each subject.
"""


from bs4 import BeautifulSoup


async def fetch(url, session):
    """Fetch the content of a given URL using an aiohttp session."""
    async with session.get(url) as response:
        return await response.text()


async def get_subject_links(session, target_url):
    """
    Fetch subject links from the main page using an aiohttp session.
    
    Args:
        session (aiohttp.ClientSession): The aiohttp session used to make requests.
        target_url (str): The URL of the main page containing subject links.
        
    Returns:
        list: A list of tuples containing subject names and their corresponding tables.
    """
    content = await fetch(target_url, session)
    soup = BeautifulSoup(content, "html.parser")
    subjects = [
        (subject.text.strip(), subject.find_next("table"))
        for subject in soup.select("span.eds_containerTitle")
    ]
    return [
        (subject_name, table) for subject_name, table in subjects
        if subject_name not in ("NON LANGUAGES", "LANGUAGES")
    ]


async def get_exam_links(table):
    """
    Fetch exam links for a specific subject using an aiohttp session.
    
    Args:
        session (aiohttp.ClientSession): The aiohttp session used to make requests.
        table (bs4.element.Tag): The BeautifulSoup object representing the subject's table.
        
    Returns:
        list: A list of tuples containing exam download links and their corresponding file names.
    """
    soup = BeautifulSoup(str(table), "html.parser")
    table_rows = soup.select("tr")

    exam_links = []
    for row in table_rows:
        title_cell = row.select_one(".TitleCell")
        download_cell = row.select_one(".DownloadCell")

        if title_cell and download_cell:
            title = title_cell.text
            download_link = download_cell.a["href"]
            file_name = title.replace(" ", "_") + ".pdf"
            exam_links.append((download_link, file_name))

    return exam_links
