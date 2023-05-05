"""
download.py

This module contains functions for downloading exam files from the South African Department
of Education website. It includes functions for downloading a file from a given URL and
saving it to a specified folder, as well as functions for orchestrating the downloading
of matric exam files based on the fetched subject and exam links.
"""

import re
import aiofiles


async def download_file(url, session, folder, file_name, progress_bar):
    """
    Download a file from a given URL using an aiohttp session and save it to the 
    specified folder.
    
    TODO: Investigate why 403 is returned for docx and doc files. PDF downloads fine.
    """
    async with session.get(url) as response:
        content_type = response.headers.get("Content-Type", "")

        if "application/pdf" in content_type:
            file_extension = "pdf"
        elif "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in content_type:
            file_extension = "docx"
        elif "application/msword" in content_type:
            file_extension = "doc"
        else:
            content_disposition = response.headers.get(
                "Content-Disposition", "")
            file_extension_match = re.search(r"\.(\w+)", content_disposition)
            file_extension = file_extension_match.group(
                1) if file_extension_match else ""

        if file_extension:
            file_name += f".{file_extension}"

        async with aiofiles.open(f"{folder}/{file_name}", "wb") as file:
            await file.write(await response.read())
            progress_bar.update(1)
