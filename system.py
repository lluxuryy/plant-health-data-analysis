from pathlib import Path
project_folder = Path(__file__).resolve().parent

from datetime import datetime

import csv
import statistics

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from plant import Plant


class PlantIRS:
    def __init__(self):
        self._plant_list = []

    # loads every row from the csv file into a plant object
    def load_data(self):
        self._plant_list = []

        with open("plant_health_data.csv", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)

            for unique_id, row in enumerate(reader, start=1):
                plant = Plant(
                    timestamp=row[0],
                    plant_id=int(row[1]),
                    soil_moisture=float(row[2]),
                    ambient_temperature=float(row[3]),
                    soil_temperature=float(row[4]),
                    humidity=float(row[5]),
                    light_intensity=float(row[6]),
                    soil_ph=float(row[7]),
                    nitrogen_level=float(row[8]),
                    phosphorus_level=float(row[9]),
                    potassium_level=float(row[10]),
                    chlorophyll_content=float(row[11]),
                    electrochemical_signal=float(row[12]),
                    plant_health_status=row[13],
                    unique_id=unique_id,
                )
                self._plant_list.append(plant)

    # adds one plant object to the current plant list
    def add_plant(self, plant):
        self._plant_list.append(plant)

    # finds the main statistics for one selected attribute
    def summarize_attribute(self, attribute):
        values = [getattr(plant, attribute) for plant in self._plant_list]

        count = len(values)
        mean = statistics.mean(values)
        median = statistics.median(values)
        stdev = statistics.pstdev(values)
        minimum = min(values)
        maximum = max(values)

        return count, mean, median, stdev, minimum, maximum

    # groups an attribute by health status and finds the average for each group
    def average_by_health_status(self, attribute):
        groups = {}

        for plant in self._plant_list:
            status = plant.plant_health_status
            value = getattr(plant, attribute)

            if status not in groups:
                groups[status] = []

            groups[status].append(value)

        results = {}
        for status, values in groups.items():
            results[status] = sum(values) / len(values)

        return results

    # prints every plant reading that was loaded from the csv file
    def print_plants(self):
        for plant in self._plant_list:
            print(plant)

    # graphs one plant attribute across all of its timestamps
    def attribute_over_time(self, attribute, plant_id):
        attribute_list = []
        timestamp_list = []

        for plant in self._plant_list:
            if plant.plant_id == plant_id:
                attribute_list.append(getattr(plant, attribute))

                # converts the timestamp into an actual date instead of plain text
                timestamp_list.append(datetime.fromisoformat(plant.timestamp))

        if not attribute_list:
            print(f"No data found for Plant ID {plant_id}")
            return

        # keeps the values in timestamp order before graphing them
        sorted_data = sorted(zip(timestamp_list, attribute_list))
        timestamp_list, attribute_list = zip(*sorted_data)

        display_name = attribute.replace("_", " ").title()

        plt.figure(figsize=(10, 6))
        plt.plot(timestamp_list, attribute_list, marker="o")
        plt.title(f"{display_name} Over Time - Plant {plant_id}")
        plt.xlabel("Timestamp")
        plt.ylabel(display_name)

        # automatically spaces out the date labels so they do not overlap
        date_locator = mdates.AutoDateLocator()
        date_formatter = mdates.ConciseDateFormatter(date_locator)

        plt.gca().xaxis.set_major_locator(date_locator)
        plt.gca().xaxis.set_major_formatter(date_formatter)

        plt.grid(alpha=0.25)
        plt.tight_layout()

        plot_path = project_folder / "plot.png"
        plt.savefig(plot_path, dpi=150, bbox_inches="tight")
        print(f"saved plot to {plot_path}")
        plt.close()

    # converts the health labels into numbers so they can be graphed and compared
    @staticmethod
    def _convert_health(value):
        health_map = {
            "Healthy": 0,
            "Moderate Stress": 1,
            "High Stress": 2,
        }
        return health_map.get(value, value)

    # calculates the correlation and makes a scatter plot with a best fit line
    def correlation_graph(self, attr1, attr2):
        x_values = []
        y_values = []

        for plant in self._plant_list:
            x = self._convert_health(getattr(plant, attr1))
            y = self._convert_health(getattr(plant, attr2))
            x_values.append(x)
            y_values.append(y)

        mean_x = statistics.mean(x_values)
        mean_y = statistics.mean(y_values)

        numerator = 0
        denominator_x = 0
        denominator_y = 0

        # calculates pearson correlation and the values needed for the best fit line
        for x, y in zip(x_values, y_values):
            dx = x - mean_x
            dy = y - mean_y
            numerator += dx * dy
            denominator_x += dx * dx
            denominator_y += dy * dy

        if denominator_x == 0 or denominator_y == 0:
            r = 0
            slope = 0
            intercept = mean_y
        else:
            r = numerator / ((denominator_x * denominator_y) ** 0.5)
            slope = numerator / denominator_x
            intercept = mean_y - slope * mean_x

        x_min = min(x_values)
        x_max = max(x_values)
        x_line = [x_min, x_max]
        y_line = [slope * x_min + intercept, slope * x_max + intercept]

        x_label = attr1.replace("_", " ").title()
        y_label = attr2.replace("_", " ").title()

        plt.figure(figsize=(10, 6))
        plt.scatter(x_values, y_values, alpha=0.65)
        plt.plot(x_line, y_line, color="red", linewidth=2)
        plt.title(f"{y_label} vs {x_label} (r = {r:.3f})")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(alpha=0.2)

        # replaces 0, 1, and 2 with the actual health status names
        health_ticks = ["Healthy", "Moderate Stress", "High Stress"]
        if attr1 == "plant_health_status":
            plt.xticks([0, 1, 2], health_ticks)
        if attr2 == "plant_health_status":
            plt.yticks([0, 1, 2], health_ticks)

        plt.tight_layout()

        plot_path = project_folder / "plot.png"
        plt.savefig(plot_path, dpi=150, bbox_inches="tight")
        print(f"saved plot to {plot_path}")
        plt.close()

        print(f"Correlation between {x_label} and {y_label}: {r:.3f}")