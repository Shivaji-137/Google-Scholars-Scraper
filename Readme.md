# Google Scholar Scraper

This command line script (works in windows, linux) allows you to search for authors and titles on Google Scholar, open URLs in a browser, download available PDFs, and clear the console screen. For better visualization, please maximize your terminal.

## Requirements

- Python 3.x
- Required Python packages:
  - `requests`
  - `beautifulsoup4`
  - `pandas`

You can install the required packages using:
```sh
pip install requests beautifulsoup4 pandas
```

## Usage

### Search by Author

```sh
python scholarScrape.py --author "Author Name"
```
or
```sh
python scholarScrape.py -a "Author Name"
```

### Search by Title

```sh
python scholarScrape.py "Title" [TIME]
```

- `TIME`: Year or "all" for all years.

### Examples

Search by author:
```sh
python scholarScrape.py --author "Neil Bohr"
```
or
```sh
python scholarScrape.py -a "Neil Bohr"
```

Search by title:
```sh
python scholarScrape.py "Machine Learning" 2021
```

## Contact

For any questions or issues, please contact:

Shivaji Chaulagain  
Email: shivajichaulagain@gmail.com

## License

This project is licensed under the MIT License.
```

Feel free to customize this `README.md` file as needed.
