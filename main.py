from bs4 import BeautifulSoup as bs
import requests
import regex as re


def cloudflare_decode(e):
    de = ""
    k = int(
        e[:2], 16)
    for i in range(2, len(e)-1, 2):
        de += chr(int(
            e[i:i+2], 16) ^ k)
    return de


def get_firms():
    firms = []
    url = "https://ornekteknokent.com.tr/firmalar/yazilim-firmalari" # Burayi degistirmen lazim
    html_content = requests.get(
        url).text
    soup = bs(
        html_content, "html.parser")
    for firm in soup.find_all("div", attrs={"class": "vc_btn3-container"}):
        firms.append(firm.find_all("a", attrs={
                     "class": "vc_general"})[0]["href"].split("/")[-2])
    return firms


firms = get_firms()


def get_email(firm):
    url = f"https://ornekteknokent.com.tr/firmalar/yazilim-firmalari{firm}" # Burayi da
    html_content = requests.get(
        url).text
    soup = bs(
        html_content, "html.parser")
    try:
        email_without_parsing = soup.find_all("div", attrs={
            "class": "main-content"})[1].find_all("div", attrs={"class": "text"})[0]
        soup = bs(str(email_without_parsing), "html.parser").find_all(
            "span", attrs={"class": "__cf_email__"})[0]
        return cloudflare_decode(soup["data-cfemail"])
    except:
        return "Firm not found."


file = open(
    "email.txt", "a")

for firm in firms:
    # print(get_email(firm))
    if (re.match(r"[^@]+@[^@]+\.[^@]+", get_email(firm))):
        file.write(
            get_email(firm) + "\n")
