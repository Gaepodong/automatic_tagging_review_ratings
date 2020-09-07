from bs4 import BeautifulSoup
import requests
import csv
import os

from datetime import datetime
from true_review import db
from true_review.models import Movies, Reviews


def get_title(code):
    url = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=' + str(code)
    response = requests.get(url.format(1))
    if response.status_code == 500:
        print("Movie code error")
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h3', class_='h_movie').find('a').text
    return title


def get_image_url(code):
    # make Url
    # https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=
    url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + \
        str(code)
    response = requests.get(url.format(1))
    if response.status_code == 500:
        print("Movie code error")
    soup = BeautifulSoup(response.text, 'html.parser')
    imageUrl = soup.find('img')
    return imageUrl['src']


def get_movie_code_list():
    movie_code_list = db.session.query(Movies.code).distinct()
    return movie_code_list


# Movies <--- 4개 있음. 3개는 review가 비어있음. 근데 udpate_reviews 실행하면, 비어있던 review 3개가 채워짐.

# update movie and reviews
#   update_movies 무비들을 업데이트하는 함수
#   update_reviews 생긴 무비들과 연결된 review들을 reviews에 등록하는 함수


def update_movies():
    path_dir = 'ranked_reviews/'
    file_list = os.listdir(path_dir)
    movie_code_list = [int(i.split('.')[0]) for i in file_list]

    # get_movi
    old_movie_code_list = [i[0] for i in list(get_movie_code_list())]

    for movie in old_movie_code_list:
        try:
            movie_code_list.remove(movie)
        except:
            pass

    print("존재하는 파일 리스트: ", movie_code_list)
    for movie_code in movie_code_list:
        title = get_title(movie_code)
        imageUrl = get_image_url(movie_code)
        movie = Movies(title, movie_code, datetime.now(), imageUrl)
        db.session.add(movie)
    try:
        db.session.commit()
    except:
        print("중복 생략...")
        return []

    exist_movie_code_list = list(set(movie_code_list + old_movie_code_list))
    update_target_movies = []
    for movie_code in exist_movie_code_list:
        movie = db.session.query(Movies).filter_by(code=movie_code).first()
        if movie.review_set:
            continue
        else:
            update_target_movies.append(movie_code)

    print("리뷰가 업데이트 되는 리스트: ", update_target_movies)
    return update_target_movies


def update_reviews(movie_code):
    movie = db.session.query(Movies).filter_by(code=movie_code).first()
    path = 'ranked_reviews/' + str(movie_code) + '.csv'
    try:
        review_file = open(path, 'r', encoding='cp949')
        # review_file = open(path, 'r', encoding='euc-kr')
    except FileNotFoundError as e:
        print("Error: ", e)
        return 0
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
    except:
        print("Error movie code: {}".format(movie_code))
    try:
        db.session.commit()
    except:
        pass
    review_file.close()
