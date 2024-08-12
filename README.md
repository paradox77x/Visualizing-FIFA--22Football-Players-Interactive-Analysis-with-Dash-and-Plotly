# Visualizing FIFA 22 Football Players: Interactive Analysis with Dash and Plotly

## Project Description
This project aims to visualize FIFA 22 player data using Dash and Plotly. With this application, users can interactively analyze player data, such as age, rating, and player distribution by country.

## Table of Contents
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Contact](#contact)

## Key Features
- **Interactive Visualization**: 
  - Scatter plot of overall rating vs age for players with a specific preferred foot.
  - Choropleth map showing player distribution by country.
  - Detailed player information when a data point on the scatter plot is clicked.
  - Bar chart displaying the top 10 players based on rating from the selected country.
- **Dynamic Filters**: Options to filter data by age, preferred foot, and region.

## Installation
To run this project locally, follow these steps:

1. Clone this repository:
    ```bash
    git clone https://github.com/paradox77x/Visualizing-FIFA--22Football-Players-Interactive-Analysis-with-Dash-and-Plotly.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Visualizing-FIFA--22Football-Players-Interactive-Analysis-with-Dash-and-Plotly
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the application:
    ```bash
    python Uas.py
    ```

## Usage
Once the application is running, you can access it via your browser at `http://localhost:8050`. Use the interactive interface to explore FIFA 22 player data.


## Project Structure
Here is the main folder structure of this project:
- `Main.py`: The main file to run the Dash application.
- `assets/`: Folder for storing CSS or JavaScript files.
- `data/`: Folder for storing the datasets used.
- `README.md`: Documentation for this project.

## Dataset
The datasets used are sourced from Kaggle:
- [FIFA 22 Complete Player Dataset](https://www.kaggle.com/stefanoleone992/fifa-22-complete-player-dataset)
- [Continents Dataset](https://www.kaggle.com/datasets/andradaolteanu/country-mapping-iso-continent-region)

## Contact
If you have any questions or suggestions, feel free to reach out to me via [Email](mailto:devin7swijaya@gmail.com) or through my [GitHub profile](https://github.com/paradox77x).
