# RealEstatePricePrediction

<!-- ABOUT THE PROJECT -->
## About The Project

The aim of this project was to create a chatbot that estimates real estate prices based on the Automated Valuation Model. The scope of it includes a web scraping method, thanks to which the data was be downloaded from the website containing advertisements about the sale of apartments and houses, preprocessing of the obtained dataset, training machine learning models, and creating a chatbot. To achieve the best results, different models were trained (linear regression, decision trees, and neural networks) and compared, and then the best one was applied to the final version of the application.

The chatbot asks a user about features of the property such as localization, area, number of rooms, floor, or parking availability. Based on the address, the program gathers further information on the city's population, travel time to the city center, the nearest store, and the nearest bus or tram stop from open source APIs. Then the enriched data is submitted to the trained model to obtain an estimated price of the real estate, which the chatbot returns to the user.

### Built With

[![Python][Python]][Python-url]
[![Jupyter][Jupyter]][Jupyter-url]
[![Numpy][Numpy]][Numpy-url]
[![Pandas][Pandas]][Pandas-url]
[![Tensorflow][Tensorflow]][Tensorflow-url]
[![Scikit-learn][Scikit-learn]][Scikit-learn-url]



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
