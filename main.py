import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

hh_url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

zp = []
list = []
mix_sort = []
vscan_t = []
sort_list = []
jobs_all = []
adr = []


def get_handres():
    return Headers(browser="firefox", os="win").generate()


def link_on_page():
    link_vac = []
    print(
        "начата сортировка по линку с переходом на страницу вакансии с главной", end=""
    )
    main_padge = requests.get(hh_url, headers=get_handres()).text
    bs = BeautifulSoup(main_padge, features="lxml")
    vacan_s = bs.find_all("a", class_="serp-item__title")
    for vacan in vacan_s:
        link_vac.append(vacan["href"])
        response_link_temp = requests.get(vacan["href"], headers=get_handres()).text
        response_link = BeautifulSoup(response_link_temp, features="lxml")
        desc_vak = response_link.find("div", {"data-qa": "vacancy-description"})
        if (("Django" or "django") or ("Flask" or "flask")) in desc_vak.text:
            vscan_t.append("+")
        else:
            vscan_t.append("-")
    for a, b in zip(vscan_t, link_vac):
        if a == "+":
            sort_list.append(b)
    print("- ВЫПОЛНЕНО")
    return sort_list


def zp_vac():
    print("Сбор данных по зарплатам", end=" ")
    for link in sort_list:  # перебираем станицы по ссылке на вакансии
        zp_links = requests.get(link, headers=get_handres()).text
        zp_link = BeautifulSoup(zp_links, features="lxml")
        zp_link_on = zp_link.find(
            "span", class_="bloko-header-section-2 bloko-header-section-2_lite"
        )
        zp.append(zp_link_on.text.replace("\xa0", " "))  # добавлям и декодируем
    print("- ВЫПОЛНЕНО")
    return


def adres():
    print("получение адеса по ссылке на вакансию", end=" ")
    for link in sort_list:
        locals = requests.get(link, headers=get_handres()).text
        localss = BeautifulSoup(locals, features="lxml")
        local = localss.find("span", {"data-qa": "vacancy-view-raw-address"})
        local1 = localss.find("p", {"data-qa": "vacancy-view-location"})
        if local != None:
            adr.append(local.text)
        if local1 != None:
            adr.append(local1.text)
    print("- ВЫПОЛНЕНО")
    return adr


def jobs():
    print("Сбор информации о работодателе", end=" ")
    for link in sort_list:
        job_link = requests.get(link, headers=get_handres()).text
        jobs_links = BeautifulSoup(job_link, features="lxml")
        jobs_link = jobs_links.find("span", {"data-qa": "bloko-header-2"}).text
        jobs_all.append(jobs_link.replace("\xa0", " "))
    print("- ВЫПОЛНЕНО")
    return jobs_all


def mix_grup(sort_list_all, zp, adress, jobs):
    print("создание словаря", end=" ")
    mix_sort = {"link-on": sort_list_all, "zap": zp, "adres": adress, "jobs": jobs}
    for a in range(len(mix_sort["adres"])):
        if (
            "Москва" in mix_sort["adres"][a]
            or "Санкт-Петербург" in mix_sort["adres"][a]
        ):
            list.append(
                {
                    "адрес": (mix_sort["adres"][a]),
                    "работодатель": (mix_sort["jobs"][a]),
                    "ссылка на вакансию": (mix_sort["link-on"][a]),
                    "зарплата": (mix_sort["zap"][a]),
                }
            )
    print("- ВЫПОЛНЕНО")
    return


def rec(load):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(load, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    link_on_page()
    zp_vac()
    adres()
    jobs()
    mix_grup(sort_list, zp, adr, jobs_all)
    rec(list)
    pprint(list)
