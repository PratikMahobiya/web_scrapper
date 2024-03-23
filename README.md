# IMdb Movies Scrapper

Scripts to fetch movie based on given Genre.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip install tqdm, bs4, requests
```

## Usage
To test the script use the bellow code.

```bash
python test_scrapper.py
```

**movie_scrapper.py** scripts in use to fetch the movies from IMdb site.

The IMdb site gives more than lacs of data for a given genre thats why we are taking **num_pages** (number of pages) to parse and fetch the movies.

While running **movie_scrapper.py** file the scripts ask you to provide a **genre** and **num_pages**.

```bash
python movie_scrapper.py.py

Enter genre or keyword (e.g., 'comedy', 'action'): comdey
Enter number of pages to scrape: 3


Fetching the movies list based on : 'comdey' . . .

100%|█████████████████████████████████████████████████████████████████| 3/3 [00:04<00:00,  1.45s/it]
2024-03-23 12:12:29,358 - INFO - Scraping completed. Data stored in 'imdb_movies.json'.

```
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)