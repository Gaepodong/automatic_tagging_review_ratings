from bs4 import BeautifulSoup
import requests
import csv
import os
from datetime import datetime
from true_review import db
from true_review.models import Movies, Reviews


def get_title(code):
    """
    get movie title from naver movie page with movie_code
    :param code: int movie_code
    :return title: string movie_title
    """
    url = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=' + str(code)
    response = requests.get(url.format(1))
    if response.status_code == 500:
        print("Movie code error")
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h3', class_='h_movie').find('a').text
    return title


def get_image_url(code):
    """
    get movie_image url from naver movie page with movie_code
    :param code: int movie_code
    :return imageUrl['src']: string movie_image url
    """
    url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + \
        str(code)
    response = requests.get(url.format(1))
    if response.status_code == 500:
        print("Movie code error")
    soup = BeautifulSoup(response.text, 'html.parser')
    imageUrl = soup.find('img')
    return imageUrl['src']


def get_already_registered_movie_codes():
    """
    get movie code list from DB
    :return movie_code_list: List already_existed_movie_codes
    """
    movie_code_list = db.session.query(Movies.code).distinct()
    return movie_code_list


def update_reviews(movie):
    """
    update  movie reviews.
    :param  movie: Movies data object
    :return Boolean: if there is no file, return false
    """
    path = 'ranked_reviews/' + str(movie.code) + '.csv'
    try:
        review_file = open(path, 'r', encoding='cp949')
    except FileNotFoundError as e:
        print("Error: ", e)
        return False

    rdr = csv.reader(review_file)
    try:
        for i, line in enumerate(rdr):
            if i == 0:
                continue
            text_rank = float(line[1])
            content = line[2]
            pos_or_neg = int(line[3])
            reviews = Reviews(movie.id, text_rank, content, pos_or_neg)
            movie.review_set.append(reviews)
            db.session.add(movie)
    except:
        print("Error movie code: {}".format(movie.code))
    review_file.close()
    return True


def update_movies_and_reviews():
    """
    update movies and reviews without duplication
    """
    path_dir = 'ranked_reviews/'
    file_list = os.listdir(path_dir)
    movie_code_list = [int(i.split('.')[0]) for i in file_list]
    get_already_registered_movie_codes = [
        i[0] for i in list(get_already_registered_movie_codes())]

    for movie_code in get_already_registered_movie_codes:
        try:
            movie_code_list.remove(movie_code)
        except:
            pass

    for movie_code in movie_code_list:
        title = get_title(movie_code)
        imageUrl = get_image_url(movie_code)
        movie = Movies(title, movie_code, datetime.now(), imageUrl)
        if update_reviews(movie) is False:
            return
    try:
        db.session.commit()
    except:
        return
