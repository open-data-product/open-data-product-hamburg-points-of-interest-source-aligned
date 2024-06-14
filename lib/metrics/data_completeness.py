import os
import unittest

file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)

data_path = os.path.join(script_path, "..", "..", "data")

key_figure_group = "hamburg-points-of-interest"

statistics_names = [
    # Residential Areas
    # "housing_complexes",
    # "apartment_buildings",

    # Workplaces
    "offices",
    "coworking_spaces",

    # Commercial Services
    "supermarkets",
    "grocery_stores",
    "convenience_stores",
    # "markets",

    # Education
    "schools",
    "kindergartens",
    "childcare",
    "libraries",
    "universities",

    # Healthcare
    "doctors",
    "pharmacies",
    "clinics",
    "hospitals",

    # Recreation and Leisure
    "sport_centers",
    "fitness_centers",

    # Cultural Spaces
    "art_galleries",
    "theaters",
    "museums",
    "cinemas",

    # Food and Dining
    "cafes",
    "restaurants",
    "marketplaces",
    "bars",
    "pubs",
    "beer_gardens",
    "fast_food_restaurants",
    "food_courts",
    "ice_cream_parlours",
    "nightclubs",

    # Public Services
    "post_offices",
    "police_stations",
    "fire_stations",

    # Transportation
    "bus_stops",
    "ubahn_stops",
    "sbahn_stops",
    "tram_stops",
    "bicycle_rentals",
    "car_sharing_stations",

    # Community Spaces
    "community_centers",
    "places_of_worship",

    # Green Spaces
    # "parks", # TODO Find a way to count parks
    # "recreation_ground",
    # "urban_gardens",
    # "greenfield",
    # "grass",
]


class FilesTestCase(unittest.TestCase):
    pass


for year in [2024]:
    for month in ["06"]:
        for statistics_name in statistics_names:
            file = os.path.join(data_path, f"{key_figure_group}-{year}-{month}",
                                f"{key_figure_group}-{statistics_name.replace('_', '-')}-{year}-{month}-details.csv")
            setattr(
                FilesTestCase,
                f"test_{key_figure_group}-{statistics_name}-{year}-{month}-details".replace('-', '_'),
                lambda self, file=file: self.assertTrue(os.path.exists(file))
            )

if __name__ == '__main__':
    unittest.main()
