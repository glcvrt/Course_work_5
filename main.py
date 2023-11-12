from utils import create_database, filler_company, filler_vacancies
from DBManager import DBManager


def main():
    create_database()
    filler_company()
    filler_vacancies()

    manag = DBManager()

    print(f"Выберите действие для работы с базой данных:\n"
                       f"1 - получить список всех компаний и количество вакансий у каждой компании\n"
                       f"2 - получить список всех вакансий с указанием названия компании, названия вакансии "
                       f"и зарплаты и ссылки навакансию\n"
                       f"3 - получить среднюю зарплату по вакансиям\n"
                       f"4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
                       f"5 - получить список всех вакансий, в названии которых содержится переданные в метод слово, например python\n"
                       f"exit - выход\n")

    while True:

        answer = input()

        if answer == "1":
            print(manag.get_companies_and_vacancies_count())
        elif answer == "2":
            print(manag.get_all_vacancies())
        elif answer == "3":
            print(manag.get_avg_salary())
        elif answer == "4":
            print(manag.get_vacancies_with_higher_salary())
        elif answer == "5":
            answ = input("Введите слово: ")
            print(manag.get_vacancies_with_keyword(answ))
        elif answer == "exit":
            break
        else:
            print("Нет такой команды.")


main()
