# Valorant Game Analysis & Heatmap Visualization

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)  
A comprehensive analytical toolkit for **Valorant** players, coaches, and strategists, providing deep insights into the game's current meta and strategic trends. This project leverages data analysis, image detection, and heatmap visualization to enhance team strategy and map control.  

## Table of Contents
1. [Introduction](#introduction)
2. [Project Objectives](#project-objectives)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Data Sources](#data-sources)
7. [Contributions](#contributions)

---

## Introduction

Valorant is a highly competitive, tactical first-person shooter game where strategic positioning and map control can significantly impact a team’s success. This project provides tools for analyzing gameplay data and visualizing movement patterns using heatmaps. With insights derived from movement data, players and coaches can understand the game's meta more effectively, optimize strategies, and make informed decisions.

## Project Objectives

- **Meta Analysis**: Understand and evaluate the current in-game meta by analyzing agent usage, economy effectiveness, map control, and win conditions.
- **Movement Heatmaps**: Automatically generate heatmaps representing player movement patterns on maps, utilizing image recognition for accurate positional data.
- **Strategic Insights**: Provide useful, data-driven insights that support team strategy, helping players and coaches to adapt to the evolving game dynamics.
  
## Features

- **Agent and Economy Analysis**: Identify trends in agent popularity, effectiveness of abilities, and economy management across various maps.
- **Win Condition Metrics**: Analyze conditions contributing to win probability, such as economic management, positioning, and round timings.
- **Heatmap Visualization**: Use image recognition to track movement and activity, generating heatmaps to highlight high-traffic areas, common engagement zones, and bottlenecks on maps.
- **Automatic Data Processing**: Automate the ingestion and processing of gameplay footage and data, streamlining the process from data collection to insight generation.
  
## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/mariusBRM/M8_Valorant.git
    cd M8_Valorant
    ```
2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Set up configuration**:
   Modify the `config.yaml` file to add API keys or configure file paths, if required for specific features.

## Usage

To generate insights and visualizations:

1. **Run data analysis**:
    ```bash
    streamlit run streamlit_app.py
    ```
2. **Generate Heatmaps**:
    ```bash
    python heatMap.py -url "https://example.com/video" -nameF "myFolder" -n 5
    ```

## Data Sources

- **Gameplay**: Game recordings in `.mp4` format are used to extract movement data from Youtube.
- **API Integrations**: Optional APIs for advanced stats and metadata. Integrations are specified in `config.yaml`.
- **Third-Party Datasets**: Optional usage of datasets from trusted sources such as community-driven websites or official APIs.

## Contributions

Contributions are welcome to improve the analytical depth and functionality of this project. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

```



