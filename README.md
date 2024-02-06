![logo](https://github.com/data-silence/timemachine/blob/master/graphs/tm.jpg?raw=true)

![Pandas](https://img.shields.io/badge/Pandas-black?style=flat-square&logo=Pandas) ![Numpy](https://img.shields.io/badge/Numpy-black?style=flat-square&logo=Numpy) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-black?style=flat-square&logo=PostgreSQL) ![Docker](https://img.shields.io/badge/Docker-black?style=flat-square&logo=Docker) ![aiogram](https://img.shields.io/badge/aiogram-black?style=flat-square&logo=aiogram) ![sklearn](https://img.shields.io/badge/sklearn-black?style=flat-square&logo=sklearn)

# Table of contents

* [About](#about-project)
* [Project structure](#project-structure)
* [About datasource](#about-datasource)
* [License](#license)

## About project

Timemachine - the NLP project based on newsru.com dataset.

This is an attempt to create an aggregator of the Past based on a Telegram bot - [@time_mashine_bot](https://t.me/time_mashine_bot)

At the moment, the first stage of the project has been realized: aggregator of news of the past has been created on the basis of materials of the agency [newsru.com](https://www.newsru.com/)

This work is a demonstration of my skills as a data-science professional to address a full range of tasks:
- data collection and processing;
- data analysis;
- data utilization ideation; 
- realization of data storage infra-structure;
- training of necessary machine learning models for solving tasks within the project;
- writing telegram bot code based on aiogram library
- Deployment and support of the finished bot using docker


## Project structure

Materials related to collecting and analyzing the dataset (parser, EDA, etc.) can be found in the researh_notebooks directory.

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


[Newsru.com](https://www.newsru.com/) is a Russian online media agency that existed from August 28, 2000 to May 31, 2021 as a news agency, and since June 1, 2021 has existed in the format of a news archive for the entire time of its operation.

This is the dataset of Russian-language news obtained from a single agency:
- russian news for 21 years
- more then 600.000 news articles
- contains short summary of all news, which can be used to train sammarization models in ML 



## License
This project is licensed under the MIT license. For more information, see the LICENSE file.
All text materials on NEWSru.com are available under the Creative Commons Attribution 4.0 International license.
