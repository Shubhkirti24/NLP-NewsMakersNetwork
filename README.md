# Fall-2023--NLP-Group-3


# Project Title: News Makers Network

## Team: Glen Colletti, Peter Stewart, Shubhkirti Prasad

---
### Web app link : http://peeves.pythonanywhere.com/network
---
## Project Description:

This project aims to develop a tool that allows users to quickly analyze a named person in the news, see what other people or entities they are connected with, and the general sentiment of news about them. We will accomplish this by:
- Identifying named entities
- Sorting entities into people, places, and things
- Assessing article sentiment
- Graphing a network of articles and people with sentiment links
- Providing tools for users to investigate relationships and articles

## Usefulness:

This tool will be useful for people who want to quickly understand the news coverage of a particular person or entity. It can be used to research politicians, celebrities, or other people in the public eye. The tool can also be used to identify trends in the news and to understand the different perspectives on a particular issue.

## Data:

We will use the following datasets for this project:

- CNN News Articles: 
This dataset contains over 9,000 articles from CNN's website. The dataset includes the article text, author, date, category, sub-category, URL, headline, description, keywords, and alternative headline.
This dataset is downloadable from Kaggle here: https://www.kaggle.com/datasets/hadasu92/cnn-articles

## Functionalities:

Our tool will perform the following tasks:

1. Preprocess data: We will preprocess the raw text of each article by removing stop words and either rooting or lemmatizing each word before vectorizing the text.
2. Named Entity Recognition (NER) and classification into people, places, and things: We will use a pre-trained NER model to identify named entities in the preprocessed text. We will then classify the named entities into people, places, and things.
3. Article clustering: We will cluster articles based on co-mentions of named entities. We may also investigate document similarity as a criteria for clustering.
4. Article sentiment analysis: We will use a pre-trained sentiment analysis model to predict the sentiment of each article.
5. Graph generation: We will generate a graph of named entities in the news article corpus centered on a user-selected entity. The graph will show the relationships between the named entities and the sentiment of the articles that mention them.
6. User interaction: We will allow users to select which NER model is used to generate the entity list and to filter the graph by entity type and sentiment.


## Next Steps:

We are currently in the early stages of development for this project. We are planning to implement the following features in the next few weeks:

1. NER and classification into people, places, and things
2. Article clustering
3. Article sentiment analysis
4. Graph generation
5. Data Visualisation

---

## Final Implementation:

![Network X Graph representing nodes ,co-mentions and sentiments](https://github.iu.edu/shubpras/Fall-2023--NLP-Group-3/blob/main/Screenshot%202023-12-10%20201446.png)

---

![Intial implementation]([https://github.iu.edu/shubpras/Fall-2023--NLP-Group-3/blob/main/Screenshot%202023-12-10%20192951.png](https://github.com/Shubhkirti24/NLP-NewsMakersNetwork/blob/main/Screenshot%202023-12-10%20192951.png)https://github.com/Shubhkirti24/NLP-NewsMakersNetwork/blob/main/Screenshot%202023-12-10%20192951.png)

