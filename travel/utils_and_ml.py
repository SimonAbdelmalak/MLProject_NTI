import webbrowser
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from data_preprocessing import clean_text

def create_google_maps_url(row):
    latitude = row.get("Latitude", np.nan)
    longitude = row.get("Longitude", np.nan)

    try:
        if pd.notna(latitude) and pd.notna(longitude):
            return f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    except Exception:
        pass

    hotel_name = clean_text(row.get("HotelName", ""))
    city = clean_text(row.get("cityName", ""))
    country = clean_text(row.get("countryName", ""))
    query = " ".join(part for part in [hotel_name, city, country] if part)

    return f"https://www.google.com/maps/search/?api=1&query={query.replace(' ', '+')}"

def create_booking_url(row):
    possible_columns = ["BookingURL", "BookingUrl", "BookingLink", "booking_url", "bookingUrl"]

    for column in possible_columns:
        if column in row.index:
            value = row[column]
            if pd.notna(value):
                value = str(value).strip()
                if value.startswith("http://") or value.startswith("https://"):
                    return value

    hotel_name = clean_text(row.get("HotelName", ""))
    city = clean_text(row.get("cityName", ""))
    country = clean_text(row.get("countryName", ""))
    query = " ".join(part for part in [hotel_name, city, country] if part)

    return f"https://www.booking.com/searchresults.html?ss={query.replace(' ', '+')}"

def open_link(url):
    webbrowser.open(url)

def compute_recommendations(hotel_df, selected_country, selected_city, selected_rating_numeric, selected_facilities, normalize_text_func):
    country_normalized = normalize_text_func(selected_country)
    city_normalized = normalize_text_func(selected_city)

    country_mask = hotel_df["countryName"].map(normalize_text_func) == country_normalized
    city_mask = hotel_df["cityName"].map(normalize_text_func) == city_normalized

    rating_mask = np.isclose(
        hotel_df["RatingNumericClean"],
        selected_rating_numeric,
        equal_nan=False
    )

    candidates = hotel_df.loc[country_mask & city_mask & rating_mask].copy()
    used_fallback_rating = False

    if candidates.empty:
        candidates = hotel_df.loc[country_mask & city_mask].copy()
        used_fallback_rating = True

    if candidates.empty:
        return pd.DataFrame(), used_fallback_rating

    X = candidates[selected_facilities].astype(float).values
    user_vector = np.ones((1, len(selected_facilities)))
    n_neighbors = len(candidates)

    knn = NearestNeighbors(n_neighbors=n_neighbors, metric="hamming")
    knn.fit(X)

    distances, indices = knn.kneighbors(user_vector)

    recommended = candidates.iloc[indices[0]].copy()
    recommended["KNN_Distance"] = distances[0]
    recommended["MatchScore"] = (100 * (1 - recommended["KNN_Distance"])).clip(0, 100).round(1)

    recommended = recommended.sort_values(
        by=["MatchScore", "KNN_Distance"],
        ascending=[False, True]
    ).head(5)

    return recommended, used_fallback_rating