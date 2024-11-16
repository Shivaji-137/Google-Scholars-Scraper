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

MIT License

Copyright (c) 2024 Shivaji Chaulagain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
