import psycopg2


class DBManager:
    def __init__(self):
        self.host = "localhost"
        self.database = "HeadHunter"
        self.user = "postgres"
        self.password = "i1485563"

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""

        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)

        with conn.cursor() as cur:
            cur.execute("SELECT company_name, COUNT(vacancies_name) AS count_vacancies "
                        "FROM company "
                        "JOIN vacancies USING (company_id) "
                        "GROUP BY company.company_name")
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию"""

        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)

        with conn.cursor() as cur:
            cur.execute("SELECT company.company_name, vacancies.vacancies_name, vacancies.salary, url_vacancies "
                        "FROM company "
                        "JOIN vacancies USING (company_id)"
                        )
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""

        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)

        with conn.cursor() as cur:
            cur.execute("SELECT AVG(salary) AS average_salary FROM vacancies")
            result = cur.fetchall()

        conn.commit()
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""

        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vacancies "
                        "WHERE salary >= (SELECT AVG(salary) FROM vacancies)")
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, word):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""

        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vacancies "
                        f"WHERE LOWER(vacancies_name) LIKE '%{word}%' OR LOWER(vacancies_name) LIKE '%{word}' "
                        f"OR LOWER(vacancies_name) LIKE '{word}%' "
                        f"OR LOWER(requirements) LIKE '%{word}%' OR LOWER(requirements) LIKE '%{word}' "
                        f"OR LOWER(requirements) LIKE '{word}%'")
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

