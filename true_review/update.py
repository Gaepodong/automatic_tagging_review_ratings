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
    # 1. ranked_reviews 폴더에 존재하는 code.csv 파일 목록 list로 저장  V
    # 2. 이미 db에 올라와 있는 파일들을 list에서 제거
    # 3. 크롤링으로 title, image_path 가져오기 (image_path 가죠오는건 이미 존재)
    # 4. 데이터 추가하기
    # 5.
    path_dir = 'ranked_reviews/'
    file_list = os.listdir(path_dir)
    movie_code_list = [int(i.split('.')[0]) for i in file_list]

    old_movie_code_list = [i[0] for i in list(get_movie_code_list())]

# list.remove(찾을아이템)
# 찾을 아이템이 없으면 ValueError 발생
    for movie in old_movie_code_list:
        try:
            movie_code_list.remove(movie)
        except:
            pass

    print(movie_code_list)
    for movie_code in movie_code_list:
        title = get_title(movie_code)
        imageUrl = get_image_url(movie_code)
        movie = Movies(title, movie_code, datetime.now(), imageUrl)
        db.session.add(movie)
    db.session.commit()

    new_movie_code_list = list(set(movie_code_list + old_movie_code_list))
    print(new_movie_code_list)
    return new_movie_code_list

def update_reviews(movie_code):
    movie = db.session.query(Movies).filter_by(code=movie_code).first()
    path = 'ranked_reviews/' + str(movie_code) + '.csv'
    try:
        review_file = open(path, 'r', encoding='cp949')
    except FileNotFoundError as e:
        print("Error: ", e)
        return 0
    rdr = csv.reader(review_file)
    # 인코딩에러는 rdr 객체를 반복문에 돌릴 때 발생한다.
    # 이 부분을 함수화 해서 UnicodeDecodeError가 발생하면
    # euc-kr, utf-8 등으로 다시 인코딩 해야할듯
    for i, line in enumerate(rdr):
        if i == 0:
            continue
        text_rank = float(line[1])
        content = line[2]
        emotion = int(line[3])
        reviews = Reviews(movie.id, text_rank, content, -1, emotion)
        movie.review_set.append(reviews)
    db.session.commit()
    review_file.close()
