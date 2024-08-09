import pandas as pd
from numpy import nan
from scipy import spatial


def process_prices():
    schools_df = pd.read_csv("./data/schools.csv")

    school_scores = list()
    schools = list()
    school_coordinates = list()
    private_schools = list()
    for idx in range(len(schools_df)):
        key = (schools_df["lat"][idx], schools_df["lng"][idx])
        if pd.isna(key[0]) or pd.isna(key[1]):
            continue

        try:
            score = float(schools_df["TALLPPE_ACAD_1618"][idx])
            school_scores.append(score)
            schools.append(schools_df["SCHNAME"][idx])
            school_coordinates.append(key)
            private_schools.append(schools_df["private"][idx])
        except Exception:
            continue

    tree = spatial.KDTree(school_coordinates)

    stations = pd.read_csv("./data/stations_with_prices.csv")
    lats = stations["lat"]
    lngs = stations["lng"]
    avg_ratings = list()
    max_ratings = list()
    school_names = list()
    for idx in range(len(stations)):
        coord = (lats.iloc[idx], lngs.iloc[idx])
        res = tree.query(coord, k=100, distance_upper_bound=0.05)

        names = list()
        private_ratings = list()
        public_ratings = list()
        ratings = list()
        for i, keyidx in enumerate(res[1]):
            if keyidx == len(schools) or pd.isna(school_scores[keyidx]):
                break

            if school_scores[keyidx] > 40:
                names.append(
                    f"{schools[keyidx]}({'private' if private_schools[keyidx] else 'public'}): {school_scores[keyidx]}@{res[0][i]:.3f}"
                )

            if private_schools[keyidx]:
                private_ratings.append(school_scores[keyidx])
            else:
                public_ratings.append(school_scores[keyidx])

            ratings.append(school_scores[keyidx])

        if not private_ratings or max(private_ratings) < 40 or not public_ratings or max(public_ratings) < 40:
            max_ratings.append(0)
            avg_ratings.append(0)
        else:
            avg_ratings.append(int(sum(ratings) / len(ratings)) if ratings else nan)
            max_ratings.append(int(max(ratings)) if ratings else nan)

        school_names.append(";".join(names))

    stations["max_ratings"] = max_ratings
    stations["avg_ratings"] = avg_ratings
    stations["school_names"] = school_names
    stations["price"] = stations["price"].apply(int)
    stations["dist"] = stations["dist"].apply(int)

    stations.dropna(inplace=True)

    stations = stations[stations["price"] < 1000000]
    stations = stations[stations["max_ratings"] > 40]
    stations = stations[stations["times"] < 75]
    stations = stations[stations["times"] < 75]

    stations.to_csv("./data/stations_with_prices_and_schools.csv")


if __name__ == "__main__":
    process_prices()
