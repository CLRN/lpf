from collections import defaultdict
import pandas as pd
from numpy import nan
from scipy import spatial


def process_prices():
    clean = pd.read_csv("./data/prices_with_location.csv")
    # df = clean.copy()[["price", "lat", "lng"]].dropna()
    # avg = df.groupby(["lat", "lng"]).mean()

    # print(f"got {len(avg)} locations out of {len(clean)}, {len(df)} grouped")
    prices = defaultdict(list)
    for idx in range(len(clean)):
        key = (clean["lat"][idx], clean["lng"][idx])
        if pd.isna(key[0]) or pd.isna(key[1]):
            continue

        prices[key].append(clean["price"][idx])

    # for idx in range(len(avg)):
    #     key = (avg.index[idx][0], avg.index[idx][1])
    #     prices[key] = avg.iloc[idx, 0]

    keys = list(prices.keys())
    tree = spatial.KDTree(keys)

    stations = pd.read_csv("./data/stations_times.csv")
    lats = stations["lat"]
    lngs = stations["lng"]
    results = list()
    for idx in range(len(stations)):
        coord = (lats.iloc[idx], lngs.iloc[idx])
        res = tree.query(coord, k=100, distance_upper_bound=0.1)

        avg = list()
        for i, keyidx in enumerate(res[1]):
            if keyidx == len(keys):
                break

            for price in prices[keys[keyidx]]:
                avg.append(price)
            # print(f"from {keys[keyidx]} to {coord} is {res[0][i]}")

        results.append(sum(avg) / len(avg) if avg else nan)

    stations["price"] = results
    stations.to_csv("./data/stations_with_prices.csv")


if __name__ == "__main__":
    process_prices()
