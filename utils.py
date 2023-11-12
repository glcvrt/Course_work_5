import json

import psycopg2
import requests


def create_database():
    """Создание базы данных и таблиц для сохранения данных о каналах и видео."""

    conn = psycopg2.connect(host="localhost", database="HeadHunter", user="postgres", password="i1485563")
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE company (
                company_number SERIAL PRIMARY KEY,
                company_name VARCHAR(50) NOT NULL,
                company_id INTEGER
            );
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancies_id INT PRIMARY KEY,
                company_id INTEGER NOT NULL,
                vacancies_name VARCHAR NOT NULL,
                address VARCHAR,
                requirements VARCHAR,
                url_vacancies VARCHAR,
                salary INTEGER

            );
        """)

    conn.commit()
    conn.close()


def filler_company():
    with open("../Course_work_5/company_id.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
        count = 0
        for k, v in data.items():
            count += 1
            conn = psycopg2.connect(host="localhost", database="HeadHunter", user="postgres", password="i1485563")
            conn.autocommit = True

            with conn.cursor() as cur:
                cur.execute(f"INSERT INTO company VALUES (%s, %s, %s);", (count, k, v))

            conn.commit()
            conn.close()


def filler_vacancies():
    with open("../Course_work_5/company_id.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
        for k, v in data.items():
            url = f"https://api.hh.ru/vacancies?employer_id={int(v)}"
            data_vacancies = requests.get(url, params={'per_page': 10}).json()["items"]
            for item in data_vacancies:
                vacancies_id = item["id"]
                company_id = v
                vacancies_name = item["name"]
                if item["address"] is None:
                    address = None
                elif item["address"]["raw"] == "null":
                    address = None
                else:
                    address = item["address"]["raw"]
                if item["snippet"] is None or item["snippet"]["requirement"] is None or item["snippet"][
                    "responsibility"] is None:
                    requirements = "null"
                else:
                    requirements = f'{item["snippet"]["requirement"]}\n{item["snippet"]["responsibility"]}'
                url_vacancies = item["alternate_url"]
                if item["salary"] == "null" or item["salary"] is None:
                    salary = None
                elif item["salary"]["to"] != "null" and item["salary"]["to"] is not None:
                    salary = int(item["salary"]["to"])
                elif item["salary"]["from"] != "null" and item["salary"]["from"] is not None:
                    salary = int(item["salary"]["from"])

                conn = psycopg2.connect(host="localhost", database="HeadHunter", user="postgres", password="i1485563")
                conn.autocommit = True

                with conn.cursor() as cur:
                    cur.execute(f"INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s);",
                                (vacancies_id, company_id, vacancies_name, address, requirements, url_vacancies, salary)
                                )
                    conn.commit()
                    conn.close()


# def printj(dict_to_print: dict) -> None:
#     """Выводит словарь в json-подобном удобном формате с отступами"""
#     print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
#
#
# url = "https://api.hh.ru/vacancies?employer_id=882"
# data_vacancies = requests.get(url, params={'per_page': 2}).json()["items"]
# printj(data_vacancies)
#
# params = {
#     'per_page': 10,
#     'open_vacancies': True
# }
# url = f"https://api.hh.ru/employers/882"
# data_vacancies = requests.get(url, params=params).json()
# printj(data_vacancies)
