import pandas as pd
import numpy as np


def get_recommendations(index, data, recommendations):
    recommendations.clear()
    for i in data.loc[:, 'book_id']:
        i = i - 1
        if data.loc[i, 'for_ages'] == data.loc[index, 'for_ages']:
            distance = np.abs(data.loc[i, 'bestsellers-rank'] - data.loc[index, 'bestsellers-rank']) + np.abs(
                data.loc[i, 'category_id'] - data.loc[index, 'category_id']) + np.abs(
                data.loc[i, 'rating_avg'] - data.loc[index, 'rating_avg'])
            recommendations.append([i, distance])


def recommender(index):
    data = pd.read_csv("recommender_data.csv")
    recommendations = []
    get_recommendations(index, data, recommendations)
    for book in sorted(recommendations, key=lambda x: x[1])[1:6]:
        print(data.index[book[0]])


if __name__ == '__main__':
    index = input("Enter book index:")
    recommender(int(index))
