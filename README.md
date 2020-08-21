# automatic_tagging_review_ratings

[대회관련 팀노션](https://www.notion.so/00d4ec17dfbf49358cac0f20d149369a)

## 개요

**감정분석 기법을 이용한 영화 리뷰평점 자동 태깅 시스템**
  
  진행 순서
  
    영화 리뷰 댓글 데이터 수집
  
    -> 감정분석
    
    -> 감정에 따른 자동 평점 부여 (한 댓글당 평점부여, 전체 평점은 작업이 완료된 이후 산술평균)
    
    -> 감정별 text rank 산정
    
    -> 유사데이터 제외, 감정수치가 높거나 극성이 가장 잘 드러나는 댓글들을 추림. (혹은 감정별 대부분의 의견을 반영한 댓글 텍스트 요약)

## 참고자료
- [네이버 영화평 데이터셋](https://github.com/e9t/nsmc)
- [국어정보처리 경진대회 특강 관련 자료](https://cafe.naver.com/nlpk/319)
- [TextRank를 이용한 키워드 추출과 핵심문장 추출](https://lovit.github.io/nlp/2019/04/30/textrank/)
- [\[DBR\] 트럼프 당선 예측했던 그 분석, 인간의 언어에서 감정을 읽어내](https://dbr.donga.com/article/view/1101/article_no/8892/ac/a_view)
- [인공감성지능 기술 동향 및 산업 분야별 적용 사례](http://www.itfind.or.kr/publication/regular/weeklytrend/weekly/view.do?boardParam1=7893&boardParam2=7893)

## 데이터셋 수집
- 네이버 영화 평점(댓글)
- 왓챠피디아 코멘트

*스포츠 댓글 및 TV프로그램 평가 댓글에서도 적용가능하게 모델의 Input을 통일시킬 필요가 있음*

## 감정분석


## 요약? 압축? 모델
- Input: Word Sequence
- Output: 

- TextRank 알고리즘 변형
- 감성수치에 기반한 Text Rank

## 모델설계
