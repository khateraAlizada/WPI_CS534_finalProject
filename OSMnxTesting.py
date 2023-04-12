import osmnx
import pandas as pd

# pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def main():
    city = "Boston, MA, USA"
    dist = 100000  # meters

    pois = osmnx.geometries_from_address(city, tags={"tourism": "attraction"}, dist=dist)

    print(pois)
    # print(pois.head(10))

    # print(roads)


if __name__ == "__main__":
    main()
