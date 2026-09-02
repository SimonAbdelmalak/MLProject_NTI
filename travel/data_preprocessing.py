import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import pandas as pd

DATA_FILENAME = "Hotel_Dataset_Final.xlsx"
ALLOWED_COUNTRIES = ["Egypt", "Spain", "France", "Switzerland"]

required_columns = {
    "countryName",
    "cityName",
    "HotelName",
    "HotelRating"
}

facility_columns = [
    "WiFi", "Parking", "SwimmingPool", "Gym", "Spa", "Restaurant", "Bar",
    "RoomService", "AirportShuttle", "PetsAllowed", "NonSmoking",
    "AirConditioning", "Sauna", "Terrace", "Laundry", "WheelchairAccessible",
    "24HourFrontDesk", "Elevator", "Golf", "KidsPool"
]

def resolve_data_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(script_dir, DATA_FILENAME)

    if os.path.exists(candidate):
        return candidate

    if os.path.exists(DATA_FILENAME):
        return os.path.abspath(DATA_FILENAME)

    root_probe = tk.Tk()
    root_probe.withdraw()

    messagebox.showinfo(
        "Locate Dataset",
        f"Couldn't find '{DATA_FILENAME}' next to the script.\n"
        "Please select the hotel dataset Excel file."
    )

    chosen = filedialog.askopenfilename(
        title="Select Hotel Dataset",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

    root_probe.destroy()

    if not chosen:
        messagebox.showerror(
            "No File Selected",
            "The app cannot start without the hotel dataset."
        )
        sys.exit(1)

    return chosen

def clean_text(value):
    if pd.isna(value):
        return ""
    value = str(value)
    value = value.replace("\xa0", " ")
    return " ".join(value.split()).strip()

def normalize_text(value):
    return clean_text(value).casefold()

def load_and_preprocess_data():
    data_path = resolve_data_path()
    try:
        hotel_df = pd.read_excel(data_path)
    except Exception as error:
        raise ValueError(f"Could not read the dataset at '{data_path}'.\nDetails: {error}")

    missing_required = required_columns - set(hotel_df.columns)
    if missing_required:
        raise ValueError(f"The dataset is missing required columns: {missing_required}")

    available_facilities = [col for col in facility_columns if col in hotel_df.columns]

    if len(available_facilities) < 3:
        raise ValueError("The dataset does not contain enough facility columns.")

    # Text cleaning
    hotel_df["countryName"] = hotel_df["countryName"].map(clean_text)
    hotel_df["cityName"] = hotel_df["cityName"].map(clean_text)
    hotel_df["HotelName"] = hotel_df["HotelName"].map(clean_text)

    if "Address" in hotel_df.columns:
        hotel_df["Address"] = hotel_df["Address"].map(clean_text)
    if "Description" in hotel_df.columns:
        hotel_df["Description"] = hotel_df["Description"].map(clean_text)

    # Filter allowed countries
    allowed_normalized = {normalize_text(c) for c in ALLOWED_COUNTRIES}
    hotel_df = hotel_df.loc[
        hotel_df["countryName"].map(normalize_text).isin(allowed_normalized)
    ].copy()
    hotel_df.reset_index(drop=True, inplace=True)

    if hotel_df.empty:
        raise ValueError("After filtering countries, no rows remained.")

    # Clean facilities
    for col in available_facilities:
        hotel_df[col] = pd.to_numeric(hotel_df[col], errors="coerce").fillna(0)
        hotel_df[col] = hotel_df[col].astype(float).clip(0, 1)

    # Rating logic
    has_rating_numeric = "HotelRatingNumeric" in hotel_df.columns
    if has_rating_numeric:
        hotel_df["HotelRatingNumeric"] = pd.to_numeric(hotel_df["HotelRatingNumeric"], errors="coerce")
        rating_source = hotel_df["HotelRatingNumeric"]
    else:
        rating_source = pd.to_numeric(hotel_df["HotelRating"], errors="coerce")

    hotel_df["RatingNumericClean"] = rating_source

    def stars_for(numeric_rating):
        try:
            n = int(round(float(numeric_rating)))
        except (TypeError, ValueError):
            return "Unrated"
        n = max(0, min(n, 5))
        if n == 0:
            return "Unrated"
        return "\u2605" * n + "\u2606" * (5 - n)

    hotel_df["RatingDisplay"] = hotel_df["RatingNumericClean"].map(stars_for)

    return hotel_df, available_facilities