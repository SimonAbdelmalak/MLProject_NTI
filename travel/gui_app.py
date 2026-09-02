import tkinter as tk
from tkinter import ttk, messagebox
from data_preprocessing import load_and_preprocess_data, clean_text, normalize_text
from utils_and_ml import create_google_maps_url, create_booking_url, open_link, compute_recommendations

def run_app():
    hotel_df, available_facilities = load_and_preprocess_data()

    root = tk.Tk()
    root.title("TravelMate ✈ - Hotel Recommendation System")

    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 850
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.minsize(1000, 700)

    # Colors & Theme
    BG_COLOR = "#F6F1E7"
    CARD_COLOR = "#FFFFFF"
    HEADER_BG = "#123C54"
    HEADER_BG_DARK = "#0C2B3D"
    ACCENT_COLOR = "#D98E3C"
    ACCENT_DARK = "#B9721F"
    TEXT_COLOR = "#1F2937"
    SECONDARY_TEXT = "#6B7280"
    BORDER_COLOR = "#E7DFCB"
    SUCCESS_COLOR = "#1F9D55"
    MISSING_COLOR = "#B4B9C2"
    MATCH_BADGE_BG = "#FCEBD3"
    MATCH_BADGE_FG = "#B9721F"
    NEUTRAL_BUTTON_BG = "#EFEAE0"
    NEUTRAL_BUTTON_FG = "#123C54"

    FONT_FAMILY = "Segoe UI"
    root.configure(bg=BG_COLOR)

    def add_hover(widget, normal_bg, hover_bg):
        widget.bind("<Enter>", lambda e: widget.configure(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.configure(bg=normal_bg))

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # Header
    header = tk.Frame(root, bg=HEADER_BG, height=110)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    tk.Label(header, text="TravelMate ✈", font=(FONT_FAMILY, 27, "bold"), bg=HEADER_BG, fg="white").pack(pady=(18, 0))
    tk.Label(header, text="Smart Hotel Recommendations for Egypt · Spain · France · Switzerland", font=(FONT_FAMILY, 11), bg=HEADER_BG, fg="#F2D9B3").pack(pady=(2, 10))
    tk.Frame(root, bg=ACCENT_COLOR, height=4).pack(fill="x", side="top")

    # Scrollable area
    outer_container = tk.Frame(root, bg=BG_COLOR)
    outer_container.pack(fill="both", expand=True)

    main_canvas = tk.Canvas(outer_container, bg=BG_COLOR, highlightthickness=0)
    scrollbar = ttk.Scrollbar(outer_container, orient="vertical", command=main_canvas.yview)
    main_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    main_canvas.pack(side="left", fill="both", expand=True)

    main_frame = tk.Frame(main_canvas, bg=BG_COLOR)
    canvas_window = main_canvas.create_window((0, 0), window=main_frame, anchor="nw")

    main_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
    main_canvas.bind("<Configure>", lambda e: main_canvas.itemconfig(canvas_window, width=e.width))
    main_canvas.bind_all("<MouseWheel>", lambda e: main_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    # Filter Card
    filter_card = tk.Frame(main_frame, bg=CARD_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=1)
    filter_card.pack(fill="x", padx=35, pady=25)
    tk.Frame(filter_card, bg=ACCENT_COLOR, height=4).pack(fill="x", side="top")

    tk.Label(filter_card, text="Find Your Perfect Hotel", font=(FONT_FAMILY, 18, "bold"), bg=CARD_COLOR, fg=HEADER_BG).pack(anchor="w", padx=25, pady=(20, 0))
    tk.Label(filter_card, text=f"{len(hotel_df):,} hotels across {hotel_df['countryName'].nunique()} countries and {hotel_df['cityName'].nunique()} cities", font=(FONT_FAMILY, 9), bg=CARD_COLOR, fg=SECONDARY_TEXT).pack(anchor="w", padx=25, pady=(2, 15))

    form_frame = tk.Frame(filter_card, bg=CARD_COLOR)
    form_frame.pack(fill="x", padx=25, pady=(0, 20))
    form_frame.columnconfigure((0, 1, 2), weight=1)

    def make_field(parent, label_text, column, padx):
        frame = tk.Frame(parent, bg=CARD_COLOR)
        frame.grid(row=0, column=column, sticky="ew", padx=padx, pady=5)
        tk.Label(frame, text=label_text, font=(FONT_FAMILY, 10, "bold"), bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 5))
        var = tk.StringVar()
        combo = ttk.Combobox(frame, textvariable=var, state="readonly", font=(FONT_FAMILY, 11))
        combo.pack(fill="x", ipady=6)
        return var, combo

    country_var, country_combo = make_field(form_frame, "Country", 0, (0, 10))
    city_var, city_combo = make_field(form_frame, "City", 1, (10, 10))
    rating_var, rating_combo = make_field(form_frame, "Hotel Rating", 2, (10, 0))
    rating_label_to_value = {}

    # Facilities
    facility_section = tk.Frame(filter_card, bg=CARD_COLOR)
    facility_section.pack(fill="x", padx=25, pady=(0, 20))
    tk.Label(facility_section, text="Preferred Facilities", font=(FONT_FAMILY, 11, "bold"), bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 8))

    facility_grid = tk.Frame(facility_section, bg=CARD_COLOR)
    facility_grid.pack(fill="x")
    facility_vars = {}

    for index, facility in enumerate(available_facilities):
        var = tk.BooleanVar(value=False)
        facility_vars[facility] = var
        check = tk.Checkbutton(facility_grid, text=facility, variable=var, bg=CARD_COLOR, fg=TEXT_COLOR, activebackground=CARD_COLOR, activeforeground=ACCENT_DARK, selectcolor=CARD_COLOR, font=(FONT_FAMILY, 9), anchor="w")
        check.grid(row=index // 4, column=index % 4, sticky="w", padx=(0, 25), pady=4)

    # Button
    button_frame = tk.Frame(filter_card, bg=CARD_COLOR)
    button_frame.pack(fill="x", padx=25, pady=(0, 25))
    recommend_button = tk.Button(button_frame, text="✨ Recommend Hotels", font=(FONT_FAMILY, 12, "bold"), bg=ACCENT_COLOR, fg="white", activebackground=ACCENT_DARK, activeforeground="white", relief="flat", cursor="hand2", padx=30, pady=12)
    recommend_button.pack(fill="x")
    add_hover(recommend_button, ACCENT_COLOR, ACCENT_DARK)

    # Results Section
    tk.Label(main_frame, text="Top 5 Recommended Hotels", font=(FONT_FAMILY, 20, "bold"), bg=BG_COLOR, fg=HEADER_BG).pack(anchor="w", padx=35, pady=(5, 15))
    results_frame = tk.Frame(main_frame, bg=BG_COLOR)
    results_frame.pack(fill="x", padx=35, pady=(0, 40))

    tk.Label(results_frame, text="Choose a country, city, rating and at least one facility, then tap \"Recommend Hotels\".", font=(FONT_FAMILY, 10), bg=BG_COLOR, fg=SECONDARY_TEXT).pack(anchor="w", pady=10)

    def get_unique_sorted_values(series):
        values, seen = [], set()
        for value in series:
            cleaned = clean_text(value)
            if not cleaned: continue
            normalized = normalize_text(cleaned)
            if normalized not in seen:
                seen.add(normalized)
                values.append(cleaned)
        return sorted(values, key=lambda x: normalize_text(x))

    country_combo["values"] = get_unique_sorted_values(hotel_df["countryName"])

    def update_cities(event=None):
        selected_country = country_var.get()
        city_combo.set(""); rating_combo.set("")
        city_combo["values"] = []; rating_combo["values"] = []
        rating_label_to_value.clear()
        if not selected_country: return
        country_data = hotel_df.loc[hotel_df["countryName"].map(normalize_text) == normalize_text(selected_country)]
        city_combo["values"] = get_unique_sorted_values(country_data["cityName"])

    country_combo.bind("<<ComboboxSelected>>", update_cities)

    def update_ratings(event=None):
        selected_country, selected_city = country_var.get(), city_var.get()
        rating_combo.set(""); rating_combo["values"] = []; rating_label_to_value.clear()
        if not selected_country or not selected_city: return
        mask = (hotel_df["countryName"].map(normalize_text) == normalize_text(selected_country)) & (hotel_df["cityName"].map(normalize_text) == normalize_text(selected_city))
        city_data = hotel_df.loc[mask]
        ratings = sorted(city_data["RatingNumericClean"].dropna().unique().tolist())
        labels = []
        for r in ratings:
            n = int(round(float(r)))
            star_word = "Star" if n == 1 else "Stars"
            label = f"{n} {star_word}  " + ("★" * min(n, 5) + "☆" * (5 - min(n, 5)))
            rating_label_to_value[label] = r
            labels.append(label)
        rating_combo["values"] = labels

    city_combo.bind("<<ComboboxSelected>>", update_ratings)

    def create_hotel_card(parent, row, rank, selected_facilities):
        card = tk.Frame(parent, bg=CARD_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card.pack(fill="x", pady=8)
        tk.Frame(card, bg=ACCENT_COLOR if rank == 1 else BORDER_COLOR, height=4).pack(fill="x", side="top")

        top_frame = tk.Frame(card, bg=CARD_COLOR)
        top_frame.pack(fill="x", padx=20, pady=(16, 6))

        tk.Label(top_frame, text=f"#{rank}  {clean_text(row.get('HotelName', ''))}", font=(FONT_FAMILY, 15, "bold"), bg=CARD_COLOR, fg=HEADER_BG, anchor="w").pack(side="left", fill="x", expand=True)
        tk.Label(top_frame, text=f"{float(row.get('MatchScore', 0)):.0f}% Match", font=(FONT_FAMILY, 10, "bold"), bg=MATCH_BADGE_BG, fg=MATCH_BADGE_FG, padx=12, pady=6).pack(side="right")

        info_text = f"{row.get('RatingDisplay', 'Unrated')}"
        address = clean_text(row.get("Address", ""))
        if address: info_text += f"     📍 {address}"
        tk.Label(card, text=info_text, font=(FONT_FAMILY, 10), bg=CARD_COLOR, fg=SECONDARY_TEXT, anchor="w", justify="left", wraplength=950).pack(fill="x", padx=20, pady=2)

        desc = clean_text(row.get("Description", ""))
        if desc:
            if len(desc) > 400: desc = desc[:400] + "..."
            tk.Label(card, text=desc, font=(FONT_FAMILY, 10), bg=CARD_COLOR, fg=TEXT_COLOR, anchor="w", justify="left", wraplength=950).pack(fill="x", padx=20, pady=(8, 8))

        matched, missing = [], []
        for facility in selected_facilities:
            try:
                if float(row[facility]) >= 1: matched.append(facility)
                else: missing.append(facility)
            except: missing.append(facility)

        fac_frame = tk.Frame(card, bg=CARD_COLOR)
        fac_frame.pack(fill="x", padx=20, pady=(2, 10))
        if matched: tk.Label(fac_frame, text="✓ " + ", ".join(matched), font=(FONT_FAMILY, 9), bg=CARD_COLOR, fg=SUCCESS_COLOR, anchor="w").pack(fill="x")
        if missing: tk.Label(fac_frame, text="✗ " + ", ".join(missing), font=(FONT_FAMILY, 9), bg=CARD_COLOR, fg=MISSING_COLOR, anchor="w").pack(fill="x", pady=(2, 0))

        btn_frame = tk.Frame(card, bg=CARD_COLOR)
        btn_frame.pack(fill="x", padx=20, pady=(5, 18))

        m_btn = tk.Button(btn_frame, text="📍 Google Maps", font=(FONT_FAMILY, 9, "bold"), bg=NEUTRAL_BUTTON_BG, fg=NEUTRAL_BUTTON_FG, relief="flat", cursor="hand2", padx=15, pady=7, command=lambda u=create_google_maps_url(row): open_link(u))
        m_btn.pack(side="left", padx=(0, 8))
        add_hover(m_btn, NEUTRAL_BUTTON_BG, BORDER_COLOR)

        b_btn = tk.Button(btn_frame, text="🏨 Booking.com", font=(FONT_FAMILY, 9, "bold"), bg=HEADER_BG, fg="white", relief="flat", cursor="hand2", padx=15, pady=7, command=lambda u=create_booking_url(row): open_link(u))
        b_btn.pack(side="left")
        add_hover(b_btn, HEADER_BG, HEADER_BG_DARK)

    def recommend_hotels():
        sc, s_city, s_rating_lbl = country_var.get(), city_var.get(), rating_var.get()
        if not sc or not s_city or not s_rating_lbl:
            messagebox.showwarning("Missing Information", "Please select country, city, and rating.")
            return

        selected_facilities = [f for f, var in facility_vars.items() if var.get()]
        if not selected_facilities:
            messagebox.showwarning("Missing Facilities", "Please select at least one facility.")
            return

        selected_rating_numeric = rating_label_to_value.get(s_rating_lbl)
        recommended, used_fallback = compute_recommendations(hotel_df, sc, s_city, selected_rating_numeric, selected_facilities, normalize_text)

        for widget in results_frame.winfo_children():
            widget.destroy()

        if recommended.empty:
            tk.Label(results_frame, text="No hotels were found for the selected options.", font=(FONT_FAMILY, 10), bg=BG_COLOR, fg=SECONDARY_TEXT).pack(anchor="w", pady=10)
            return

        if used_fallback:
            tk.Label(results_frame, text=f"No exact match for the selected rating in {s_city}. Showing best matches from all ratings.", font=(FONT_FAMILY, 9, "italic"), bg=BG_COLOR, fg=SECONDARY_TEXT).pack(anchor="w", pady=(0, 8))

        for rank, (_, row) in enumerate(recommended.iterrows(), start=1):
            create_hotel_card(results_frame, row, rank, selected_facilities)

        root.update_idletasks()
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        main_canvas.yview_moveto(0.35)

    recommend_button.configure(command=recommend_hotels)
    root.mainloop()

if __name__ == "__main__":
    run_app()