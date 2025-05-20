# Samsung Product Scraper

This project is a Python-based scraper targeting a Samsung storefront. It extracts product metadata and pricing using `requests` and `beautifulsoup4`, storing the data in a PostgreSQL backend defined via SQLAlchemy. Stock levels and promotions are maintained in the same database but populated through separate mechanisms.

## Overview

- Scrapes product listings and prices from Samsung’s online catalog.
- Uses `requests` for HTTP access and `beautifulsoup4` for HTML parsing.
- Interacts with a PostgreSQL database using SQLAlchemy.
- Provided schema includes additional fields (e.g., promotions, stock levels) not populated by this script.

## Status

The scraper is no longer maintained or operational due to changes in the target website and internal project deprecation.

## Disclaimer

This code is presented as an artifact of engineering capability. It is not designed for reuse, contains no setup instructions, and is not supported. It used unofficial scraping methods without Samsung's permission.

## Notes

- Project emphasizes structured data extraction, database integration, and modular design.
- Support for non-scraped data such as stock and promotions is handled externally.
- Do not file issues or expect continued updates.
