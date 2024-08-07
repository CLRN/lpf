import pandas as pd
import requests


def load() -> pd.DataFrame:
    content = requests.get("https://www.allthestations.co.uk/map/allthestations-js-ie.php").content.decode()
    content = content[content.find("oaMarkers[1] =") :]
    pos = 0

    items = []
    while pos != -1:
        pos = content.find("] =", pos)
        begin = content.find("({", pos)
        end = content.find("})", begin)
        pos = content.find("] =", end)

        body = content[begin:end]

        lines = body.split("\n")
        where = [line for line in lines if line.find("position") != -1][0]
        title = [line for line in lines if line.find("title") != -1][0]

        parts = where.split(" ")
        parts = ["".join([c for c in s if c in ".-" or c.isdigit()]) for s in parts]
        lat, lng = list(map(float, filter(str, parts)))

        station = title.split("'")[1]
        beg = station.rfind("(")
        end = station.rfind(")")
        code = station[beg + 1 : end]
        station = station[: beg - 1]

        items.append({"code": code, "name": station, "lat": lat, "lng": lng})

    return pd.DataFrame(items)


def main():
    df = load()
    df.to_csv("data/stations.csv")


if __name__ == "__main__":
    main()
