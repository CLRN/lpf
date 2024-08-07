from datetime import datetime
from functools import partial

import numpy as np
import pandas as pd
import requests
from dateutil.parser import parse as parse_dt
from parse import logging
from requests_html import HTMLSession


# vectorized haversine function
def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371):
    """
    slightly modified version: of http://stackoverflow.com/a/29546836/2901002

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)

    All (lat, lon) coordinates must have numeric dtypes and be of equal length.

    """
    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

    a = np.sin((lat2 - lat1) / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2.0) ** 2

    return earth_radius * 2 * np.arcsin(np.sqrt(a))


class TimeResults:
    def __init__(self, pages):
        self.pages = pages

    def diff(self, dep, arr):
        return int((datetime.strptime(arr, "%H:%M") - datetime.strptime(dep, "%H:%M")).total_seconds() / 60)

    def get_best(self):
        fastest = 180
        departure_time = ""

        for page in self.pages:
            for row in page.html.find("tr"):
                data = [r.strip() for r in row.text.split("\n")]
                if len(data) < 6:
                    continue

                try:
                    diff = self.diff(data[0], data[3])
                    if diff < fastest:
                        fastest = diff
                        departure_time = data[0]
                except:
                    pass

        return fastest, departure_time


class Parser:
    def __init__(
        self, src: str, distance: float = 100, time_range=["0730", "0745", "0800", "0815", "0830"], date="130319"
    ):
        self.destination = src
        self.max_distace = distance
        self.time_range = time_range
        self.date = date
        self.url_pattern = "http://ojp.nationalrail.co.uk/service/timesandfares/{}/{}/{}/{}/dep"
        self.session = HTMLSession()

    def make_url(self, src, dst, time_start):
        return self.url_pattern.format(src, dst, self.date, time_start)

    def _distance(self, from_lat, from_lng, row):
        return haversine(from_lat, from_lng, row["lat"], row["lng"])

    def run(self):
        df = pd.read_csv("data/stations.csv")
        src = (df[df["code"] == self.destination]).iloc[0]
        df["dist"] = df.apply(partial(self._distance, src["lat"], src["lng"]), axis=1)
        df = df[df["dist"] < self.max_distace]
        df.to_csv("data/stations_dist.csv")

        times = list()
        for src in df["code"]:
            # Execute the query on the transport
            min_time = 9999
            try:
                logging.info(f"working on {src}")
                result = requests.post(
                    "https://jpservices.nationalrail.co.uk/journey-planner",
                    json={
                        "origin": {"crs": src, "group": False},
                        "destination": {"crs": self.destination, "group": False},
                        "outwardTime": {"travelTime": "2024-08-08T08:00:00+01:00", "type": "DEPART"},
                        "fareRequestDetails": {
                            "passengers": {"adult": 1, "child": 0},
                            "fareClass": "ANY",
                            "railcards": [],
                        },
                        "directTrains": False,
                        "reducedTransferTime": True,
                        "onlySearchForSleeper": False,
                        "overtakenTrains": True,
                        "useAlternativeServices": False,
                        "increasedInterchange": "ZERO",
                    },
                ).json()

                for journey in result["outwardJourneys"]:
                    ts_from = parse_dt(journey["timetable"]["scheduled"]["departure"])
                    ts_to = parse_dt(journey["timetable"]["scheduled"]["arrival"])
                    minutes = (ts_to - ts_from).total_seconds() // 60
                    min_time = min(min_time, minutes)

                logging.info(f"{src} -> {self.destination} = {min_time} minutes")
            except Exception:
                logging.exception(f"failed to calc for {src}")

            times.append(min_time)

        df["times"] = times
        df.to_csv("data/stations_times.csv")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = Parser("VIC")
    parser.run()
