# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import string
from scrapy.item import Field, Item

class DynamicItem(Item):
    def __init__(self, json_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in json_data.keys():
            self.fields[field_name] = Field()

# Main item that holds the job information we need
class JobsProjectItem(Item):
    slug = Field()
    language = Field()
    languages = Field()
    req_id = Field()
    title = Field()
    description = Field()
    location_name = Field()
    street_address = Field()
    city = Field()
    state = Field()
    country = Field()
    country_code = Field()
    postal_code = Field()
    location_type = Field()
    latitude = Field()
    longitude = Field()
    categories = Field()
    tags = Field()
    tags1 = Field()
    tags2 = Field()
    tags5 = Field()
    tags6 = Field()
    tags8 = Field()
    brand = Field()
    department = Field()
    recruiter_id = Field()
    posted_date = Field()
    posting_expiry_date = Field()
    promotion_value = Field()
    salary_frequency = Field()
    salary_currency = Field()
    salary_value = Field()
    salary_min_value = Field()
    salary_max_value = Field()
    benefits = Field()    
    employment_type = Field()
    work_hours = Field()
    hiring_organization = Field()
    source = Field()
    apply_url = Field()
    internal = Field()
    searchable = Field()
    applyable = Field()
    li_easy_applyable = Field()
    ats_code = Field()
    meta_data = Field()
    update_date = Field()
    create_date = Field()
    category = Field()
    full_location = Field()
    short_location = Field()

class MetaDataItem(Item):
    ats = Field()
    ats_id = Field()
    ats_instance = Field()
    career_sections = Field()
    client_code = Field()
    district_description = Field()
    domicile_location = Field()
    domicile_location_name = Field()
    extensions = Field()
    flow_config_name = Field()
    gqid = Field()
    import_source = Field()
    job_classification_ids = Field()
    meta_data = Field()
    referencenumber = Field()
    locale_id = Field()
    login = Field()
    login_url = Field()
    openingjobs = Field()
    partner_id = Field()
    question_sets = Field()
    questionnaires = Field()
    questionnaires_to_post = Field()
    questionservice = Field()
    #TODO make sure this fits to naming convention
    redirectOnApply = Field()
    session_hijacking = Field()
    region_description = Field()
    site_id = Field()
    youtube_id = Field()
    upload_answer_html = Field()
    source_tracking = Field()
    use_poltergeist = Field()
    googlejobs = Field()
    canonical_url = Field()
    last_mod = Field()
    gdpr = Field()

class GoogleJobsItem(Item):
    companyName = Field()
    jobName = Field()
    jobHash = Field()
    derivedInfo = Field()
    jobSummary = Field()
    jobTitleSnippet = Field()
    searchTextSnippet = Field()

class DerivedInfoItem(Item):
    jobCategories = Field()
    locations = Field()

class LocationsItem(Item):
    latLng = Field()
    locationType = Field()
    postalAddress = Field()
    radiusInMiles = Field()

class PostalAddressItem(Item):
    addressLines = Field()
    administrativeArea = Field()
    languageCode = Field()
    locality = Field()
    organization = Field()
    postalCode = Field()
    recipients = Field()
    regionCode = Field()
    revision = Field()
    sortingCode = Field()
    sublocality = Field()