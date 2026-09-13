from system import PlantIRS


class Interface:
    # starts the program and handles all of the user menu options
    @staticmethod
    def start():
        system = PlantIRS()
        system.load_data()

        attribute_map = {
            "1": ("soil_moisture", "Soil Moisture"),
            "2": ("ambient_temperature", "Ambient Temperature"),
            "3": ("soil_temperature", "Soil Temperature"),
            "4": ("humidity", "Humidity"),
            "5": ("light_intensity", "Light Intensity"),
            "6": ("soil_ph", "Soil pH"),
            "7": ("nitrogen_level", "Nitrogen Level"),
            "8": ("phosphorus_level", "Phosphorus Level"),
            "9": ("potassium_level", "Potassium Level"),
            "10": ("chlorophyll_content", "Chlorophyll Content"),
            "11": ("electrochemical_signal", "Electrochemical Signal"),
        }

        print("***********************************************************")
        print("*Welcome to the Plant Data Retrieval System*")
        print("***********************************************************")

        option = "-1"
        while option != "0":
            option = input(
                "What would you like to do?\n"
                "[1] Print all Plants\n"
                "[2] Find all the main statistics of an Attribute\n"
                "[3] Make a Graph\n"
                "[4] Average an Attribute by Health Status\n"
                "[0] Exit Program\n"
            )

            if option == "1":
                system.print_plants()

            elif option == "2":
                Interface._statistics_menu(system, attribute_map)

            elif option == "3":
                Interface._graph_menu(system, attribute_map)

            elif option == "4":
                Interface._average_menu(system, attribute_map)

            elif option == "0":
                print("Goodbye!")

            else:
                print("Invalid option. Please try again.")

    # shows the menu used for choosing a plant attribute
    @staticmethod
    def _attribute_prompt(include_health=False):
        prompt = (
            "[1] - Soil Moisture\n"
            "[2] - Ambient Temperature\n"
            "[3] - Soil Temperature\n"
            "[4] - Humidity\n"
            "[5] - Light Intensity\n"
            "[6] - Soil pH\n"
            "[7] - Nitrogen Level\n"
            "[8] - Phosphorus Level\n"
            "[9] - Potassium Level\n"
            "[10] - Chlorophyll Content\n"
            "[11] - Electrochemical Signal\n"
        )

        if include_health:
            prompt += "[12] - Plant Health Status\n"

        return prompt + "[0] - Go Back\n"

    # handles the statistics option from the main menu
    @staticmethod
    def _statistics_menu(system, attribute_map):
        option = input(
            "Choose an attribute to find statistics for:\n"
            + Interface._attribute_prompt()
        )

        if option == "0":
            return

        if option not in attribute_map:
            print("Invalid option. Please try again.")
            return

        attribute_name, display_name = attribute_map[option]
        count, mean, median, stdev, minimum, maximum = system.summarize_attribute(
            attribute_name
        )

        print(f"\n{display_name} statistics:")
        print(f"Count: {count}")
        print(f"Mean: {mean}")
        print(f"Median: {median}")
        print(f"Standard Deviation: {stdev}")
        print(f"Minimum: {minimum}")
        print(f"Maximum: {maximum}\n")

    # handles both graphing options from the main menu
    @staticmethod
    def _graph_menu(system, attribute_map):
        option = input(
            "[1] Graph an Attribute over Time\n"
            "[2] Correlation Graph Between Two Attributes\n"
            "[0] Go Back\n"
        )

        if option == "1":
            Interface._time_graph_menu(system, attribute_map)
        elif option == "2":
            Interface._correlation_menu(system, attribute_map)
        elif option != "0":
            print("Invalid option. Please try again.")

    # graphs one selected plant attribute over time
    @staticmethod
    def _time_graph_menu(system, attribute_map):
        plant_option = input(
            "What Plant would you like to graph?\n"
            "[1] - Plant 1\n"
            "[2] - Plant 2\n"
            "[3] - Plant 3\n"
            "[4] - Plant 4\n"
            "[5] - Plant 5\n"
            "[6] - Plant 6\n"
            "[7] - Plant 7\n"
            "[8] - Plant 8\n"
            "[9] - Plant 9\n"
            "[10] - Plant 10\n"
            "[0] - Go Back\n"
        )

        if plant_option == "0":
            return

        if not plant_option.isdigit() or not 1 <= int(plant_option) <= 10:
            print("Invalid option. Please try again.")
            return

        attribute_option = input(
            "What attribute would you like to graph?\n"
            + Interface._attribute_prompt()
        )

        if attribute_option == "0":
            return

        if attribute_option not in attribute_map:
            print("Invalid option. Please try again.")
            return

        attribute_name = attribute_map[attribute_option][0]
        system.attribute_over_time(attribute_name, int(plant_option))

    # makes a correlation graph between any two selected attributes
    @staticmethod
    def _correlation_menu(system, attribute_map):
        correlation_map = {
            key: value[0] for key, value in attribute_map.items()
        }
        correlation_map["12"] = "plant_health_status"

        first = input(
            "Choose the first attribute (x-axis):\n"
            + Interface._attribute_prompt(include_health=True)
        )

        if first == "0":
            return

        if first not in correlation_map:
            print("Invalid option. Please try again.")
            return

        second = input(
            "Choose the second attribute (y-axis):\n"
            + Interface._attribute_prompt(include_health=True)
        )

        if second == "0":
            return

        if second not in correlation_map:
            print("Invalid option. Please try again.")
            return

        system.correlation_graph(correlation_map[first], correlation_map[second])

    # averages one selected attribute for each plant health status
    @staticmethod
    def _average_menu(system, attribute_map):
        option = input(
            "Choose an attribute to average by health status:\n"
            + Interface._attribute_prompt()
        )

        if option == "0":
            return

        if option not in attribute_map:
            print("Invalid option. Please try again.")
            return

        attribute_name, display_name = attribute_map[option]
        results = system.average_by_health_status(attribute_name)

        print(f"\nAverage {display_name} by health status:")
        for status, average in results.items():
            print(f"{status}: {average}")
        print()
