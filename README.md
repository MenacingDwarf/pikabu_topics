# Pikabu topics analyzer
Pikabu scrapper and data analyzer

## Part 1. Data collection

On this step dataset with 100000 posts will be collected from pikabu. For this purposes I used selenium. All posts belongs one of ten categories:
1. "politics"
2. "humour"
3. "help"
4. "children"
5. "relationships"
6. "coronavirus"
7. "poetry"
8. "job"
9. "history"
10. "ukraine"

To reproduce data collection please perform the following steps:
1. Run [crawler script](Part1/crawler.py).
2. Run [script for dataframe creation](Part1/main_processing.py).
3. Continue in [jupyter notebook](Part1/preprocessing.ipynb) for data preprocessing.
4. If you don't want use jupyter notebooks you can just run [script for full processing](Part1/full_processing.py) insted of steps 2 and 3.

You can also download all required data without runnig scripts in [google drive](https://drive.google.com/drive/folders/1eiZEIFzuk1t4u8MPgD6eQXkTWzVrEwew?usp=sharing).

## Part 2. Exploratory Data Analysis

On this step some additional preprocessing was done (dates translation to float, fill nans). After that, the data were carefully examined. Frequency analysis and correlation analysis were carried out.

To reproduce data collection please perform the following steps:
1. Run the [EDA notebook](Part2/EDA.ipynb) and follow the steps in it.

## Part 3. Classification, clusterization, topic modeling

To begin with, additional work had to be done with the data prepared in the previous stages. The [fasttext algorithm](https://fasttext.cc/docs/en/crawl-vectors.html) was applied to the text of posts and headings to get the embedded text. Stop words were removed from all posts and lemmatization was applied. As a result, the features necessary for further training were selected.

But the main purpose of this stage was the application of algorithms for classification, clustering, topic modeling. To reproduce the results perform the following steps:
1. Run the [feature selection notebook](Part3/features_selection.ipynb) and follow the steps in it.
2. Run the [topic modeling notebook](Part3/topic_modeling.ipynb) and follow the steps in it.

The following results were obtained:

### Classification:
 - **SVC**: 0.6848
 - **Logestic Regression**: 0.6848
 - **LDA**: 0.676

### Clusterization

The KMeans algorithm was applied for clustering. The results were extremely disastrous. The shown accuracy cannot be used in any way to solve the problem.

### Topic modeling

10 topics were identified using the LDA algorithm. Among those identified, the themes of politics, work, children, and poetry are quite clearly traced. The rest of the themes are traced implicitly, it is difficult to determine what exactly they mean.
