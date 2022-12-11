# import requests
# import scrapy
# #url = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&view_all_page_id=108448151941309&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=all"
# import requests
# url ="https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&view_all_page_id=108448151941309&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=all"
# api_key = "ug91heTGqrRQDI8bnJBAPh2DjFm9NQg0Pt1eP3goQFtB3MwXaazpoJGWuUHs5BrEUh8dlMtCSMQoWVms8f"
#
# print("HERE IS THE URL: ",requests.get(f"https://scraping.narf.ai/api/v1/?render_js=true&api_key={api_key}&url={url}").content)
#
# #URL IS https://scraping.narf.ai/api/v1/?render_js=true&api_key="ug91heTGqrRQDI8bnJBAPh2DjFm9NQg0Pt1eP3goQFtB3MwXaazpoJGWuUHs5BrEUh8dlMtCSMQoWVms8f"&url=https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&view_all_page_id=108448151941309&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=all
# print(f"https://scraping.narf.ai/api/v1/?render_js=true&api_key={api_key}&url={url}")
#
# #curl https://scraping.narf.ai/api/v1/usage/?api_key=ug91heTGqrRQDI8bnJBAPh2DjFm9NQg0Pt1eP3goQFtB3MwXaazpoJGWuUHs5BrEUh8dlMtCSMQoWVms8f
#
#
# # THAT CLASS IS TO MAKE COOKIES FUCK OFF
# #_42ft _4jy0 _9xo6 _4jy3 _4jy1 selected _51sy

import scrapy
from scrapy.http import Request, Response

class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = [
        "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&view_all_page_id=108448151941309&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=all"
    ]

    def parse(self, response):
        # Extract the cookies from the response
        cookies = response.headers.getlist('Set-Cookie')
        # Iterate over the cookies
        for cookie in cookies:
            # Check if the "secure" flag is set
            if "secure" in cookie:
                print("The website has cookies marked as 'secure'")
            # Check if the "HttpOnly" flag is set
            if "HttpOnly" in cookie:
                print("The website has cookies marked as 'HttpOnly'")