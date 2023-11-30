![logo](https://github.com/data-silence/newsrucom-dataset-eda/blob/master/logo.png?raw=True)
# Table of contents

* [About](#about-project)
* [Project structure](#project-structure)
* [About datasource](#about-datasource)
* [License](#license)


## About project

This repository is an attempt to create an aggregator of the Past based on a Telegram bot - [@time_mashine_bot](https://t.me/time_mashine_bot)
At the moment, the first stage of the project has been realized - [aggregator of news of the past](https://t.me/time_mashine_bot) has been created on the basis of materials of the agency [newsru.com](https://www.newsru.com/)

This work is a demonstration of my skills as a data-science professional to address a full range of tasks:
- data collection and processing;
- data analysis;
- data utilization ideation; 
- realization of data storage infra-structure;
- training of necessary machine learning models for solving tasks within the project;
- writing telegram bot code based on aiogram library
- Deployment and support of the finished bot using docker


## Project structure

Materials related to collecting and analyzing the dataset can be found in the researh_notebooks directory.

The other directories are parts of the telegram bot:
- imports: contains files with imports of the necessary libraries;
- models: contains ready-made models of embeddings and classifier, which are used by the bot;
- scripts: stores scripts that provide functionality of separate parts of the bot:
    * time_machine.py is the main script for obtaining and converting data into the required output format;
    * handlers.py and common_handlers.py - dispatcher and handlers of main and basic user reactions;
    * keyboard.py - keyboards;
    * utils - auxiliary functions and variables
- graphs: stores auxiliary graphical files

The app.py file is the entry point for the bot.



## About datasource


This is Exploratory Data Analysis (EDA) and its developing and of newsru.com dataset

[Newsru.com](https://www.newsru.com/) is a Russian online media agency that existed from August 28, 2000 to May 31, 2021 as a news agency, and since June 1, 2021 has existed in the format of a news archive for the entire time of its operation.

This is the dataset of Russian-language news obtained from a single agency:
- russian news for 21 years
- more then 600.000 news articles
- contains short summary of all news, which can be used to train sammarization models in ML 



## License
This project is licensed under the MIT license. For more information, see the LICENSE file.
All text materials on NEWSru.com are available under the Creative Commons Attribution 4.0 International license.