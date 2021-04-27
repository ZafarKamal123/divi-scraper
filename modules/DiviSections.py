from selenium.common.exceptions import NoSuchElementException
from functions import overwrite_file, get_module_names
from selenium.webdriver import Chrome, ChromeOptions
from Screenshot import Screenshot_Clipping
from modules.DiviPages import DiviPages
from modules.airtable import Airtable
from modules.Space import Space
import progressbar
from paths import *
import random
import json
import time
import os


class DiviSections:
    """
        This will handle taking screenshots and other divi section related logic
    """

    PROCESS_LIMIT = 10

    @staticmethod
    def get_code(template, i, name):

        data_keys = list(template.get('data').keys())
        template_data = template.get('data').get(data_keys[0])
        content = template_data.get('post_content')

        # splitting sections from the content
        sections = list(map(lambda c: c + "[/et_pb_section]", content.split("[/et_pb_section]")))
        random_id = random.randint(0, 200000000)
        required_section = sections[i]

        section_shortcode = {
            "context": "et_builder",
            "data": {},
            "presets": "",
            "images": template.get('images'),
        }

        section_shortcode['data'][str(random_id)] = str(required_section)

        return section_shortcode, required_section

    @staticmethod
    def update_sections(offset=""):

        layouts, current_offset = Airtable.get_layouts(offset)

        if not layouts:
            # this means an error while fetching layouts
            raise SystemExit('Error while fetching required layout records from airtable')

        # with mp.Pool(processes=DiviSections.PROCESS_LIMIT) as pool:
        #     pool.map(DiviSections.scrape_sections, [page for page in layouts])
        #     pool.close()

        section_progress_file = open(DIVI_SECTION_PROGRESS_PATH, 'r+')
        section_progress = json.load(section_progress_file)
        bar = progressbar.ProgressBar(maxval=len(layouts),
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        remaining_pages = []

        print(f'checking progress')

        bar.start()

        for page in layouts:

            fields = page.get('fields')
            page_name = fields.get('Page')

            print(page_name)

            if page_name in section_progress:
                continue

            remaining_pages.append(page)

        bar.finish()

        scraping_bar = progressbar.ProgressBar(maxval=len(remaining_pages),
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

        print(f'starting scraping')

        scraping_bar.start()

        for page in remaining_pages:
            DiviSections.scrape_sections(page)

        scraping_bar.finish()

        print(f"Finished scraping for offset {offset} proceeding to next offset")
        DiviSections.update_sections(current_offset)

    @staticmethod
    def scrape_sections(page):
        """
            Will scrape sections data from the given page code
            and update it to the airtable and space
        """
        fields = page.get('fields')
        code, pack, page_name, niche, page_url = fields.get('Page Code'), fields.get('Pack'), fields.get(
            'Page'), fields.get('Niche'), fields.get('Page Url')
        code_url = code[0].get('url')
        page_code = DiviPages.get_page_code(url=code_url)
        page_live_url = page_url + "/live-demo"

        chrome_options = ChromeOptions()
        chrome_options.headless = False
        
        driver = Chrome(chrome_options=chrome_options, executable_path=CHROME_WEBDRIVER)

        driver.get(page_live_url)

        time.sleep(2)

        driver.maximize_window()

        total_sections = driver.execute_script("return document.querySelectorAll('.et_pb_section').length")

        # for loading all lazy images
        SCROLL_PAUSE_TIME = 0.5
        i = 0
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            i += 1
            if i == 5:
                break

        driver.implicitly_wait(10)

        for i in range(0, total_sections):

            fields = page.get('fields')
            code, pack, page_name, niche, page_url = fields.get('Page Code'), fields.get('Pack'), fields.get(
                'Page'), fields.get('Niche'), fields.get('Page Url')
            code_url = code[0].get('url')
            page_code = DiviPages.get_page_code(url=code_url)
            page_live_url = page_url + "/live-demo"

            section_name = f"{pack}-{page_name}-section-{i}.png"
            section_code_name = f"{pack}-{page_name}-section-{i}.json"
            name = f"{pack}-{page_name}-section-{i}"

            try:
                # injecting css code
                driver.execute_script("""

                                let injectedScript = document.querySelector("#scraper-script");

                                if ( injectedScript ) {

                                    injectedScript.parentNode.removeChild(injectedScript);

                                }

                                let bodyElement = document.querySelector('head')

                                bodyElement.innerHTML = `<style id="scraper-script">

                                * {
                                    animation-duration: 0s !important;
                                    animation-delay: 0s !important;
                                }

                                #page-container {
                                    padding: 0px !important;
                                }

                                #main-footer, #main-header {
                                    display:none !important;
                                }

                                .et_pb_section:not(.et_pb_section_%s) {
                                    display: none !important;
                                }
                                

                                .et_animated.et-waypoint {
                                    opacity: 1 !important;
                                }

                                .et_animated {
                                    opacity: 1 !important;
                                }

                                .et_had_animation.et-waypoint {
                                    animation-duration: 0s !important;
                                    animation-delay: 0s !important;
                                }

                            </style> ${bodyElement.innerHTML} ` """ % (str(i)))

                section_element = driver.find_element_by_class_name(f"et_pb_section_{i}")
                root_save_path = TMP_DIRECTORY + f"/{pack}/{page_name}"
                screenshot_save_path = root_save_path + "/" + section_name

                # creating dir if not found
                if not os.path.exists(root_save_path):
                    os.makedirs(root_save_path)

                ob = Screenshot_Clipping.Screenshot()

                ob.get_element(
                    driver=driver,
                    element=section_element,
                    save_location=root_save_path,
                    name=section_name
                )

                section_shortcode, section_code = DiviSections.get_code(page_code, i, f"{pack}-{page_name}-section-{i}")
                code_save_path_root = TMP_DIRECTORY + f"/{pack}/{page_name}"
                code_save_path_full = code_save_path_root + f"/{section_code_name}"

                # creating a json content file if not found
                if not os.path.exists(code_save_path_full):
                    open(code_save_path_full, "x")

                with open(code_save_path_full, 'r+') as code_file:
                    overwrite_file(code_file, json.dumps(section_shortcode))
                    code_file.close()

                # from further this line i've both code/section
                # uploading media to space because airtable attaches
                # media by reading publicly readable/available endpoints

                space = Space()

                # uploading image
                is_image_uploaded = space.upload(path=screenshot_save_path, public_id=name + ".jpg",
                                                 c_type="image/jpeg")

                # uploading code
                is_code_uploaded = space.upload(path=code_save_path_full, public_id=section_code_name,
                                                c_type="application/json")

                if is_image_uploaded == False or is_code_uploaded == False:
                    raise SystemExit('Failed to upload code or image to the space')

                # deleting them from os because media has been uploaded to the space
                for media_path in [screenshot_save_path, code_save_path_full]:
                    if os.path.exists(media_path):
                        os.remove(media_path)

                screenshot_uploaded_url = space.proxy + name + ".jpg"
                code_uploaded_url = space.proxy + section_code_name

                # adding section to airtable
                response = Airtable.post_section(section={
                    'Title': name,
                    'Pack': pack,
                    'Section Screenshot': screenshot_uploaded_url,
                    'Section Code': code_uploaded_url,
                    'Page': page_name,
                    'Niche': niche,
                    'Url': page_url,
                    'Modules': get_module_names(section_code)
                })

                # deleting media
                for media_path in [screenshot_save_path, code_save_path_full]:
                    if os.path.exists(media_path):
                        os.remove(media_path)

                if response != True:
                    raise SystemExit('Failed to add sections in airtable')

            except NoSuchElementException:
                pass

            # this means section has been published successfully
            # updating progress
            with open(DIVI_SECTION_PROGRESS_PATH, 'r+') as section_progress_file:
                current_section_progress = json.load(section_progress_file)

                if page_name not in current_section_progress:
                    current_section_progress.append(page_name)
                    overwrite_file(section_progress_file, json.dumps(current_section_progress))
                    
                section_progress_file.close()

        driver.quit()
