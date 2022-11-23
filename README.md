# RealEstatePricePrediction

<!-- ABOUT THE PROJECT -->
## About The Project

The aim of this project was to create a chatbot that estimates real estate prices based on the Automated Valuation Model. The scope of it includes a web scraping method, thanks to which the data was be downloaded from the website containing advertisements about the sale of apartments and houses, preprocessing of the obtained dataset, training machine learning models, and creating a chatbot. To achieve the best results, different models were trained (linear regression, decision trees, and neural networks) and compared, and then the best one was applied to the final version of the application.

The chatbot asks a user about features of the property such as localization, area, number of rooms, floor, or parking availability. Based on the address, the program gathers further information on the city's population, travel time to the city center, the nearest store, and the nearest bus or tram stop from open source APIs. Then the enriched data is submitted to the trained model to obtain an estimated price of the real estate, which the chatbot returns to the user.

The project consists of four main folders. The `web-scraping` directory contains the implementation of the web scraping service, which collects data from the [otodom][otodom-url] webpage using the `BeautifulSoup` and `Selenium` libraries. In the `preprocessing` folder, there are two Jupyter notebooks (one for the apartment advertisement dataset and one for the houses advertisement dataset), which aim is to preprocess the scrapped data by handling missing values, removing outliers, normalizing and categorical encoding. The `models` directory includes implementation and evaluation of machine learning models: linear regression, XGBoost and neural networks. Finally, the `chatbot` catalogue considers creating a chatbot with the help of the Rasa framework.

### Built With

[![Python][Python]][Python-url]
[![Jupyter][Jupyter]][Jupyter-url]
[![Numpy][Numpy]][Numpy-url]
[![Pandas][Pandas]][Pandas-url]
[![Tensorflow][Tensorflow]][Tensorflow-url]
[![Scikit-learn][Scikit-learn]][Scikit-learn-url]
[![Rasa][Rasa]][Rasa-url]

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Jupyter]: https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white
[Jupyter-url]: https://jupyter.org/
[Numpy]: https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white
[Numpy-url]: https://numpy.org/
[Pandas]: https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
[Tensorflow]: https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white
[Tensorflow-url]: https://www.tensorflow.org/
[Scikit-learn]: https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white
[Scikit-learn-url]: https://scikit-learn.org/
[Rasa]: https://img.shields.io/badge/rasa-7D4698?style=for-the-badge&logo=rasa&logoColor=white
[Rasa-url]: https://rasa.com/
[otodom-url]: https://otodom.pl/

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is a list of software that should be installed before running the project.
* Rasa: 2.8.2
* Rasa SDK: 2.8.1
* Rasa X: 0.39.3
* Python: 3.8.15

### Set up

To run the project, execute the following commands:

1. Clone the repo
   ```sh
   git clone https://github.com/KlaudiaK1/RealEstatePricePrediction.git
   ```
2. Run the Rasa actions
   ```sh
   rasa run actions
   ```
4. Train the Rasa models
   ```sh
   rasa train
   ```
3. Run the instance of the chatbot in the browser
   ```sh
   rasa x
   ```
