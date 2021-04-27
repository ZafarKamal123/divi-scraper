import json


def overwrite_file(file, new_content):
    # Will overwrite all file content
    file.seek(0)
    file.write(new_content)
    file.truncate()


def insert_json_record(file, record):
    # Will insert the json record in the given file path
    with open(file, 'r+') as json_file:
        # reading the current json data
        json_data = json.load(json_file)

        # appending new record
        json_data.append(record)

        # over writing the json file
        overwrite_file(json_file, json.dumps(json_data))


def delete_json_record(file, target_id):
    # Delete the record matching the given id from the json file
    with open(file, 'r+') as json_file:

        # reading the current json data
        json_data = json.load(json_file)

        # appending the desired record that matches the id
        updated_json_data = []

        for entry in json_data:
            entry_id = entry.get('id')

            if entry_id != target_id:
                updated_json_data.append(entry)

        # over writing the json file
        overwrite_file(json_file, json.dumps(updated_json_data))


def insert_json_record_by_id(file, record) -> bool:
    with open(file, 'r+') as json_file:

        # reading the file
        json_data = json.load(json_file)

        record_exists = False

        # checking if record with the id already exists
        for entry in json_data:
            entry_id = entry.get('id')
            record_id = record.get('id')

            if entry_id == record_id:
                record_exists = True
                break

        if record_exists:
            return False

        # appending otherwise
        json_data.append(record)

        # overwriting again
        overwrite_file(json_file, json.dumps(json_data))


def update_json_record(file, record):
    with open(file, "r+") as json_file:

        # reading file
        json_data = json.load(json_file)

        updated_json_data = []

        for entry in json_data:

            entry_id = entry.get('id')
            record_id = record.get('id')

            if entry_id == record_id:
                updated_json_data.append(record)
            else:
                updated_json_data.append(entry)

        overwrite_file(json_file, json.dumps(updated_json_data))


def get_module_names(shortcode):
    """
    Will check what modules the given shortcode contains
    Returns:
        array: modules slug 
    """

    divi_modules = {
        "et_pb_accordion": "accordion",
        "et_pb_audio": "audio",
        "et_pb_counters": "bar_counters",
        "et_pb_blog": "blog",
        "et_pb_blurb": "blurb",
        "et_pb_button": "button",
        "et_pb_cta": "call_to_action",
        "et_pb_circle_counter": "circle_counter",
        "et_pb_code": "code",
        "et_pb_comments": "comment",
        "et_pb_contact_form": "contact_form",
        "et_pb_countdown_timer": "countdown",
        "et_pb_divider": "divider",
        "et_pb_signup": "email_optin",
        "et_pb_filterable_portfolio": "filterable_portfolio",
        "et_pb_gallery": "gallery",
        "et_pb_image": "image",
        "et_pb_login": "login",
        "et_pb_map": "map",
        "et_pb_menu": "menu",
        "et_pb_number_counter": "number_counter	",
        "et_pb_person": "person",
        "et_pb_portfolio": "portfolio",
        'et_pb_post_content': 'post_content',
        "et_pb_post_nav": "post_navigation",
        "et_pb_post_slider": "post_slider",
        "et_pb_post_title": "post_title",
        "et_pb_pricing_tables": "pricing_tables",
        "et_pb_search": "search",
        "et_pb_shop": "shop",
        "et_pb_sidebar": "sidebar",
        "et_pb_slider": "slider",
        "et_pb_social_media_follow": "social_media_follow",
        "et_pb_tabs": "tabs",
        "et_pb_testimonial": "testimonial",
        "et_pb_team_member": "team_member",
        "et_pb_text": "text",
        "et_pb_toggle": "toggle",
        "et_pb_video": "video",
        "et_pb_video_slider": "video_slider",
        "et_pb_fullwidth_code": "full_width_code",
        "et_pb_fullwidth_header": "full_width_header",
        "et_pb_fullwidth_image": "full_width_image",
        "et_pb_fullwidth_map": "full_width_map",
        "et_pb_fullwidth_menu": "full_width_menu",
        "et_pb_fullwidth_portfolio": "full_width_portfolio",
        "et_pb_fullwidth_post_content": "full_width_post_content",
        "et_pb_fullwidth_post_slider": "full_width_post_slider",
        "et_pb_fullwidth_post_title": "full_width_post_title",
        "et_pb_fullwidth_slider": "full_width_slider",
    }

    modules_found = []

    for slug, name in divi_modules.items():

        if shortcode.find(slug) != -1:
            modules_found.append(divi_modules[slug])

    return modules_found

