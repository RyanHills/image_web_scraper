# image_web_scraper
# Web Scraper Tool

This repository contains a web scraper tool that scrapes images from websites and categorizes them into folders based on their content.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Running the Web Scraper](#running-the-web-scraper)
  - [Categorizing Images](#categorizing-images)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/ryanhills/image_web_scraper.git
    cd image_web_scraper
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

      ```sh
      venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```sh
      source venv/bin/activate
      ```

4. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Running the Web Scraper

1. **Create a seed URLs file:**

    Create a text file named `seed_urls.txt` in the root directory of the project. Add your initial seed URLs, one per line. For example:

    ```plaintext
    https://example.com
    https://example.org
    https://example.net
    ```

2. **Run the web scraper:**

    ```sh
    python web_scraper_tool.py
    ```

    This script will read the initial seed URLs from `seed_urls.txt`, dynamically update the list of seed URLs during the crawling process, and continuously run with a delay between each scraping cycle.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
