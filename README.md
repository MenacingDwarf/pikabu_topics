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

You can also download all required data without runnig scripts in [google drive](https://drive.google.com/drive/folders/1eiZEIFzuk1t4u8MPgD6eQXkTWzVrEwew?usp=sharing).
