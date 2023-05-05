# South African Department of Education Past Exam Papers Downloader

This Python script downloads past exam papers from the South African Department of Education website.

It is designed to work with the specific structure of the website and stores the downloaded papers in an organized folder structure based on the year and subject.

## Requirements

- Python 3.7 or later
- aiohttp
- aiofiles
- beautifulsoup4
- tqdm

You can install the required packages by running:

```bash
pip install -r requirements.txt
```

## Usage

To use the script, execute download_pdfs.py from the command line and provide the year and URL for the exam papers you want to download:

```bash
python download_pdfs.py
```

You will be prompted to enter the year of the exam papers and the URL to fetch the exam papers:

```bash
Enter the year of the exam papers: 2019
Enter the URL to fetch the exam papers: https://www.education.gov.za/2019JuneNSCExamPapers.aspx
```

The script will then download the exam papers and save them in a folder structure like this:

```markdown
2019/
    Subject_1/
        Exam_Paper_1.pdf
        Exam_Paper_2.pdf
        ...
    Subject_2/
        Exam_Paper_1.pdf
        Exam_Paper_2.pdf
        ...
    ...
```

## Limitations

- This script is tailored for the South African Department of Education website and might not work if the website's structure changes.
- The script ignores subjects titled "NON LANGUAGES" and "LANGUAGES".
- The script uses concurrency to speed up downloads but is limited to 5 concurrent downloads. You can change this limit by modifying the `LIMIT_CONCURRENT_DOWNLOADS` variable in the script.

## License

This project is released under the MIT License. For more information, please refer to the LICENSE file.