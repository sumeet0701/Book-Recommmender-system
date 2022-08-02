from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

popular_df = pickle.load(open('popular.plk', 'rb'))
book_df = pickle.load(open('book.plk', 'rb'))
pt_df = pickle.load(open('pt.plk', 'rb'))
similar_df = pickle.load(open('similar.plk', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           Author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-S'].values),
                           no_of_vote=list(popular_df['Num_rating'].values),
                           ratings=list(popular_df['avg_rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommender.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index_op = np.where(pt_df.index == user_input)[0][0]
    distance = sorted(list(enumerate(similar_df[index_op])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in distance:
        item = []
        temp_df = book_df[book_df['Book-Title'] == (pt_df.index[i[0]])]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)

    return render_template('recommender.html', data=data)


if __name__ == "__main__":
     app.run(debug=True ,port=8080,use_reloader=False)
