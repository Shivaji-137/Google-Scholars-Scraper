# Google Scholar Scraper

This script allows you to search for authors and titles on Google Scholar, open URLs in a browser, download available PDFs, and clear the console screen.

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
python scholar.py --author "Author Name"
```
or
```sh
python scholar.py -a "Author Name"
```

### Search by Title

```sh
python scholar.py "Title" [TIME]
```

- `TIME`: Year or "all" for all years.

### Examples

Search by author:
```sh
python scholar.py --author "Neil Bohr"
```
or
```sh
python scholar.py -a "Neil Bohr"
```

Search by title:
```sh
python scholar.py "Machine Learning" 2021
```

## Contact

For any questions or issues, please contact:

Shivaji Chaulagain  
Email: shivajichaulagain@gmail.com

## License

This project is licensed under the MIT License.
```

Feel free to customize this `README.md` file as needed.