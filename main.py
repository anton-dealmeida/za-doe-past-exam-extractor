"""
main.py

This script is the entry point for downloading matric exam papers from the South African
Department of Education website. It utilizes functions defined in the `fetch.py` and
`download.py` modules to scrape exam paper links, create directories, and download
the exam files. The user can input the desired year and URL to fetch the exam papers.

Usage:
    1. Run the script.
    2. Enter the year of the exam papers.
    3. Enter the URL to fetch the exam papers.
"""


import os
import asyncio
from urllib.parse import urljoin
import aiohttp
from fetch import get_subject_links, get_exam_links
from tqdm.asyncio import tqdm
from download import download_file

LIMIT_CONCURRENT_DOWNLOADS = 5


async def main(year, target_url):
    """Main function to orchestrate the downloading of matric exam files."""
    async with aiohttp.ClientSession() as session:
        subject_links = await get_subject_links(session, target_url)

        download_tasks = []
        with tqdm(total=len(download_tasks), desc="Downloading", ncols=100) as progress_bar:
            for subject_name, table in subject_links:
                folder = f"{year}/{subject_name}"
                os.makedirs(folder, exist_ok=True)

                exam_links = await get_exam_links(table)
                download_tasks.extend([
                    download_file(urljoin(target_url, exam_link),
                                  session, folder, file_name, progress_bar)
                    for exam_link, file_name in exam_links
                ])

            progress_bar.total = len(download_tasks)  # Update the total count
            for i in range(0, len(download_tasks), LIMIT_CONCURRENT_DOWNLOADS):
                await asyncio.gather(*download_tasks[i:i + LIMIT_CONCURRENT_DOWNLOADS])

if __name__ == "__main__":
    input_year = input("Enter the year of the exam papers: ")
    input_target_url = input("Enter the URL to fetch the exam papers: ")
    asyncio.run(main(input_year, input_target_url))
