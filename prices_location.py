import pandas as pd
from pgeocode import Nominatim


def process_prices():
    # https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads
    df = pd.read_csv("./data/pp-2023.csv", usecols=[1, 2, 3], names=["price", "ts", "code"])  # type: ignore
    uk = Nominatim("gb")
    lat = list()
    lng = list()
    last = 0
    for code in df["code"]:
        if not pd.isna(code):
            res = uk.query_postal_code(code)
            lat.append(res["latitude"])
            lng.append(res["longitude"])
        else:
            lat.append(code)
            lng.append(code)

        percent = int(len(lat) * 100 / len(df)) 
        if percent != last:
            print(f"done {len(lat)} records: {percent}%")
            last = percent


    df["lat"] = lat
    df["lng"] = lng
    df.to_csv("./data/prices_with_location.csv")


if __name__ == "__main__":
    process_prices()
