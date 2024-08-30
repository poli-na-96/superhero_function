import concurrent.futures
import os
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

FIRST_HERO_NUMBER = 1
LAST_HERO_NUMBER = 731


def fetch_hero_data(superhero_id: int, token: str) -> Optional[dict]:
    """
    Функция для получения данных о супергерое по его id.
    """
    url = f'https://www.superheroapi.com/api.php/{token}/{superhero_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def get_max_height_hero(gender: str, has_work: bool) -> Optional[dict]:
    """
    Функция, которая возвращает самого высокого супергероя из множества героев
    одного пола и множества имеющих/не имеющих работу.
    """
    types_gender = ["Male", "Female", "-"]
    if gender not in types_gender:
        raise ValueError("Неизвестный тип гендера")
    if not isinstance(has_work, bool):
        raise ValueError("Наличие работы должно быть True или False")
    token = os.getenv("SUPERHERO_API_TOKEN")
    if not token:
        raise EnvironmentError("API token отсутствует.")

    max_height = 0
    max_height_hero = None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_hero_data, superhero_id, token)
            for superhero_id in range(FIRST_HERO_NUMBER, LAST_HERO_NUMBER + 1)
        ]
        for future in concurrent.futures.as_completed(futures):
            hero = future.result()
            if hero is None:
                continue
            hero_gender = hero.get("appearance", {}).get("gender")
            hero_occupation = hero.get("work", {}).get("occupation")
            hero_work = True
            if hero_occupation == "-":
                hero_work = False
            if hero_gender == gender and hero_work == has_work:
                try:
                    height = float(
                        hero.get("appearance", {}).get("height", [])[1]
                        .split()[0]
                    )
                except (ValueError, IndexError):
                    height = 0
                if height > max_height:
                    max_height = height
                    max_height_hero = hero

    return max_height_hero
