## 네이버 쇼핑에서 키워드 검색한 상품 리스트를 크롤링 합니다.
판매처, 상품이름, 가격, 링크를 수집합니다.


## 로컬 환경 설정
1. .env.example 을 복사하여 .env 파일을 생성합니다.
2. .env db 정보는 docker-compose.yml 파일을 참조합니다
3. docker-compose up 으로 로컬 환경을 구축합니다.
4. docker container 에 접속하여 python3 main.py 파일을 실행합니다.


## Table
```sql
CREATE TABLE `naver_shopping` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `product_name` varchar(255) NOT NULL DEFAULT '' COMMENT '상품이름',
  `product_price` int(10) NOT NULL DEFAULT '0' COMMENT '상품가격',
  `mall_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '판매처 고유키',
  `mall_link` text NOT NULL COMMENT '판매처 판매 링크',
  `crawling_date` datetime DEFAULT NULL COMMENT '크롤링된 시간',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8 COMMENT='네이버 쇼핑에 노출되는 상품 리스트'
```
