# PEP Scrapy Parser

## Description

This parser parses PEP documentation numbers, titles, and statuses from https://peps.python.org/.

The parsed data is saved in csv files.
- Information about each PEP standard: PEP number, titel, status;
- Number of PEP standards for each status + total number of all PEPs.

Additionally the parsed data is saved in sqlite database.


## Installation
- Clone the repository
  ```
  git clone https://github.com/TatianaBelova333/scrapy_parser_pep.git
  ```
- Install all dependencies and activate virtual enironment
  ```
  python -m venv venv
  ```
  ```
  pip install -r requirements.txt
  ```
- Navigate from the project root directory to pep_parse folder:
  ```
  cd pep_parse/
  ```
- To start the parser, run the following command
  ```
  scrapy crawl pep
  ```

### Authors
[Tatiana Belova](https://github.com/TatianaBelova333)