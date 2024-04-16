import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv("recommender_data.csv")
similarities = cosine_similarity(data)


def give_recommendation(index):
    data = pd.read_csv("recommender_data.csv")
    similarities = cosine_similarity(data)
    for book in sorted(list(enumerate(similarities[index])), key=lambda x: x[1], reverse=True)[1:6]:
        print(data.index[book[0]])


if __name__ == '__main__':
    index = input("Enter book index:")
    give_recommendation((int(index)))
