import pandas as pd
from pgeocode import Nominatim


def process_geo():
    df = pd.read_csv("./data/2022-2023/england_ks5final.csv")
    uk = Nominatim("gb")
    lat = list()
    lng = list()
    for code in df["PCODE"]:
        if not pd.isna(code):
            res = uk.query_postal_code(code)
            lat.append(res["latitude"])
            lng.append(res["longitude"])
        else:
            lat.append(code)
            lng.append(code)

    df["lat"] = lat
    df["lng"] = lng

    # TALLPPE_ACAD_1618 - avg score
    # PTAAB_2FAC - The percentage of A-Level students achieving at least three levels at grades AAB or better
    subset = df[["SCHNAME", "GEND1618", "PCODE", "lat", "lng", "TALLPPE_ACAD_1618", "PTAAB_2FAC"]]
    subset.to_csv("./data/schools.csv")


if __name__ == "__main__":
    process_geo()
