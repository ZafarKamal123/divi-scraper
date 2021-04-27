from modules.DiviDataScraper import DataScraper
from modules.DiviSections import DiviSections
from modules.DiviPages import DiviPages


def main():
    # step 1: updating divi pages records
    print("Step 1: updating data")
    DataScraper.save_updated_data()

    # step 2: scraping pages code from divi and uploading them to airtable database
    print("Step 2: updating pages to airtable")
    DiviPages.update_pages()

    # step 3: updating sections corresponding to the uncompleted pages
    print("Step 3: updating sections to airtable")
    DiviSections.update_sections()


if __name__ == "__main__":
    main()
