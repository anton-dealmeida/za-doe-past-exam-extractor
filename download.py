"""
download.py

This module contains functions for downloading exam files from the South African Department of Education website.
It includes functions for downloading a file from a given URL and saving it to a specified folder, as well as
functions for orchestrating the downloading of matric exam files based on the fetched subject and exam links.
"""

import aiofiles


async def download_file(url, session, folder, file_name, progress_bar):
    """
    Download a file from a given URL using an aiohttp session and save it to the 
    specified folder.
    """
    async with session.get(url) as response:
        async with aiofiles.open(f"{folder}/{file_name}", "wb") as file:
            await file.write(await response.read())
            progress_bar.update(1)