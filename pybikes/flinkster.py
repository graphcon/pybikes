# -*- coding: utf-8 -*-
# Copyright (C) 2017, Raul Pinto <raul.pinto@graphity-consulting.com>
# Distributed under the AGPL license, see LICENSE.txt
import json

from .base import BikeShareSystem, BikeShareStation
from . import utils

__all__ = ['Flinkster', 'FlinksterStation']

BASE_URL = 'https://api.deutschebahn.com/flinkster-api-ng/v1/bookingproposals?providernetwork=2&lat=50.11095&lon=8.66734&expand=rentalobject&limit=100'


class Flinkster(BikeShareSystem):

    authed = True

    meta = {
        'system': 'Flinkster',
        'company': ['DB Connect GmbH']
    }

    def __init__(self, tag, meta, key):
        super(Flinkster, self).__init__(tag, meta)
        self.url = BASE_URL
        self.api_key = key

    def update(self, scraper=None):
        if scraper is None:
            scraper = utils.PyBikesScraper()

        scraper.headers['Authorization'] = 'Bearer {api_key}'.format(api_key=self.api_key)
        rentalobjects = json.loads(scraper.request(self.url))
        self.stations = [
            FlinksterStation(a) for a in rentalobjects['items']
        ]


class FlinksterStation(BikeShareStation):
    def __init__(self, info):
        super(FlinksterStation, self).__init__()
        self.latitude = float(info['position']['coordinates'][1])
        self.longitude = float(info['position']['coordinates'][0])

        self.name = info['rentalObject']['attributes']['licenseplate']
        self.bikes = 1
        self.free = True
        self.extra = {
            'bookingLink': info['_links'][0]['href'],
            'rentalModel': info['rentalObject']['rentalModel']
        }
