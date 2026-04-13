import json
import requests

HH_URL = "https://api.hh.ru/vacancies"


def one_page_hh_vacansies(url: str, query: dict):
    responce = requests.get(url, query)
    if responce.status_code != 200:
        print("Запрос пришел с ошибкой", responce.text)
        return
    print(f"Получены вакансии со страницы {query["page"]}")
    result = responce.json()
    return result


def all_page_hh_vacancies(url: str, text: str, max_vacancies: int):
    per_page = 100
    page = 0
    vacancies_data = []
    query = {
        "text": text,
        "per_page": per_page,
        "page": page,
    }
    while len(vacancies_data) < max_vacancies:
        query["page"] = page
        vacancies = one_page_hh_vacansies(HH_URL, query)
        if vacancies is None or len(vacancies["items"]) == 0:
            break

        remaining = max_vacancies - len(vacancies_data)
        vacancies_to_add = vacancies["items"][:remaining]
        vacancies_data.extend(vacancies_to_add)

        page += 1

    with open("vacancies.json", "w", encoding="utf-8") as file_out:
        json.dump(vacancies_data, file_out, indent=3, ensure_ascii=False)
    print(f"Сохранено {len(vacancies_data)} вакансий в файл vacancies.json")
    return {"ok": True}


def main():
    print(
        "Данная программа создаст json файл содержащий вакансии с заданными вами аргументами"
    )
    print("Вводите аргументы по очереди, как закончите напишите stop")
    texts = []
    while True:
        text = input()
        if text.lower() == "stop":
            break
        texts.append(text)
    max_vacancies = input("Сколько вы хотите максимально вакансий?")
    result = all_page_hh_vacancies(HH_URL, " OR ".join(texts), int(max_vacancies))


if __name__ == "__main__":
    main()
