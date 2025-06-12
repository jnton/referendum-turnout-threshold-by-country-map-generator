# Referendum Turnout Threshold by Country Map Generator

This repository contains the Python script and data files used to generate the original ["File:Referendum Turnout Threshold by Country.svg"](https://commons.wikimedia.org/wiki/File:Referendum_Turnout_Threshold_by_Country.svg) image on Wikimedia Commons. After generation, the version uploaded to Wikimedia Commons was post-processed by adding metadata and exporting it as a "Plain SVG" using [Inkscape](https://inkscape.org/).

## Description

This project uses a Python script to color an SVG world map based on referendum turnout requirements for different countries. The map provides a visual representation of these thresholds using the following color scheme:

*   **Dark blue:** Turnout threshold of 50% or more.
*   **Dodger blue:** Turnout threshold between 40% and 49%.
*   **Steel blue:** Turnout threshold between 26% and 39%.
*   **Light blue:** Turnout threshold of 25% or less.
*   **Green:** No turnout threshold required for the referendum to be binding.
*   **Light Green:** Historically no threshold, with few exceptions (e.g., United Kingdom).
*   **Red:** No legal provision for national referendums.
*   **Dark grey:** Allows referendums, but data on a possible turnout threshold is not available.
*   **Light grey:** No data available.

This map visualizes only the turnout threshold and does not account for other potential requirements, such as approval quorums, or the various types, rules, and limitations on referendums that differ between countries.

## Data Sources

*   **Referendum Data:** [Wikipedia: Referendums by country](https://en.wikipedia.org/w/index.php?title=Referendums_by_country&oldid=1295140579) (as of 12 June 2025). The content from Wikipedia is available under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/). Attribution is given to Wikipedia contributors.
*   **Blank World Map:** [Wikimedia Commons: BlankMap-World.svg](https://commons.wikimedia.org/wiki/File:BlankMap-World.svg). This file is in the **Public Domain**.

## How to Use

1.  **Prerequisites**: Make sure you have Python 3 installed on your system.

2.  **Install Dependencies**: The script requires a few Python packages. You can install them using pip:
    ```bash
    pip install beautifulsoup4 pycountry lxml
    ```

3.  **Update Data**: The referendum data is stored in the `Wikipedia data` file. You can update this file by pasting the wikitable content from the source Wikipedia page.

4.  **Generate the Map**: Run the `final_map_generator.py` script from your terminal:
    ```bash
    python3 final_map_generator.py
    ```
    This will create (or update) the `Referendum_map_colored.svg` file in the project directory.

## License

This project is licensed under the **AGPL-3.0 License**. See the [LICENSE](LICENSE) file for details.