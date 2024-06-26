import uuid
from dataclasses import dataclass
import requests
import uuid
from .models import Property, ListingType, SiteName


@dataclass
class ScraperInput:
    location: str
    listing_type: ListingType
    radius: float | None = None
    mls_only: bool | None = None
    proxy: str | None = None
    last_x_days: int | None = None
    date_from: str | None = None
    date_to: str | None = None
    foreclosure: bool | None = None


class Scraper:
    def __init__(
        self,
        scraper_input: ScraperInput,
        session: requests.Session = None,
    ):
        self.location = scraper_input.location
        self.listing_type = scraper_input.listing_type

        if not session:
            self.session = requests.Session()
            self.session.headers.update(
                {
                    "auth": f"Bearer {self.get_access_token()}",
                    "apollographql-client-name": "com.move.Realtor-apollo-ios",
                }
            )
        else:
            self.session = session

        if scraper_input.proxy:
            proxy_url = scraper_input.proxy
            proxies = {"http": proxy_url, "https": proxy_url}
            self.session.proxies.update(proxies)

        self.listing_type = scraper_input.listing_type
        self.radius = scraper_input.radius
        self.last_x_days = scraper_input.last_x_days
        self.mls_only = scraper_input.mls_only
        self.date_from = scraper_input.date_from
        self.date_to = scraper_input.date_to
        self.foreclosure = scraper_input.foreclosure

    def search(self) -> list[Property]: ...

    @staticmethod
    def _parse_home(home) -> Property: ...

    def handle_location(self): ...

    def get_access_token(self):
        url = "https://graph.realtor.com/auth/token"

        payload = f'{{"client_app_id":"rdc_mobile_native,24.20.4.149916,iphone","device_id":"{str(uuid.uuid4()).upper()}","grant_type":"device_mobile"}}'
        headers = {
            "Host": "graph.realtor.com",
            "x-client-version": "24.20.4.149916",
            "accept": "*/*",
            "content-type": "Application/json",
            "user-agent": "Realtor.com/24.20.4.149916 CFNetwork/1410.0.3 Darwin/22.6.0",
            "accept-language": "en-US,en;q=0.9",
        }
        response = requests.post(url, headers=headers, data=payload)

        data = response.json()
        return data["access_token"]
