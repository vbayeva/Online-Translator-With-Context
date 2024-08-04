import string
import sys
import requests
from bs4 import BeautifulSoup

base_url = "https://context.reverso.net/translation/"

language_list = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish",
                 "Portuguese", "Romanian", "Russian", "Turkish"]


def get_request_content(language_source, language_target, word):
    language_url_part = f"{language_source.lower()}-{language_target.lower()}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = base_url + language_url_part + "/" + word
    try:
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            return request.content
        elif str(request.status_code).startswith("4"):
            print(f"Sorry, unable to find {word}")
            return None
        else:
            print(f"Something wrong with your internet connection")
            return None
    except requests.exceptions.ConnectionError:
        print(f"Something wrong with your internet connection")
        return None


def get_soup(content):
    return BeautifulSoup(content, "html.parser")


def get_translations(soup: BeautifulSoup):
    translations_tag = soup.findAll("span", {"class": "display-term"})
    translations = []
    for translation_tag in translations_tag:
        translations.append(translation_tag.text)
    return translations


def get_examples(soup: BeautifulSoup, language_source, language_target):
    if language_source.capitalize() == "Arabic":
        examples_tag_source = soup.find_all("div", {"class": "src rtl arabic"})
    elif language_source.capitalize() == "Hebrew":
        examples_tag_source = soup.find_all("div", {"class": "src rtl"})
    else:
        examples_tag_source = soup.find_all("div", {"class": "src ltr"})
    if language_target.capitalize() == "Arabic":
        examples_tag_target = soup.find_all("div", {"class": "trg rtl arabic"})
    elif language_target.capitalize() == "Hebrew":
        examples_tag_target = soup.find_all("div", {"class": "trg rtl"})
    else:
        examples_tag_target = soup.find_all("div", {"class": "trg ltr"})
    translations = []
    length = min(len(examples_tag_source), len(examples_tag_target))
    for i in range(length):
        translations.append(examples_tag_source[i].text)
        translations.append(examples_tag_target[i].text)
    return translations


def translate_word(language_source, language_target, word):
    content = get_request_content(language_source, language_target, word)
    if content is None:
        return None

    soup = get_soup(content)

    translations = get_translations(soup)

    examples = get_examples(soup, language_source, language_target)
    example_clean = []
    for example in examples:
        for whitespace in ['\r', '\n']:
            example = example.replace(whitespace, "")
        example = example.lstrip(' ')
        example_clean.append(example)

    return translations, example_clean


def verity_languages(language_source, language_target):
    if language_source.capitalize() not in language_list:
        print(f"Sorry, the program doesn't support {language_source}")
        return False
    if language_target != "all" and language_target not in language_list:
        print(f"Sorry, the program doesn't support {language_target}")
        return False
    return True


def get_translation(language_source, language_target, word):
    is_ok = verity_languages(language_source, language_target)

    if not is_ok:
        return None

    return translate_word(language_source, language_target, word)


if __name__ == '__main__':
    get_translation()
