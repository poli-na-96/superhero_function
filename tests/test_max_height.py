import pytest

from max_height_code.max_height import get_max_height_hero

"""
Создается словарь с данными для тестирования, c парами
(для обеспечения возможности сравнения) сочетания всех комбинаций:
мужчина/женщина/без гендера с работой/без.
"""
superhero_data = {
    1: {"name": "Peter",
        "appearance": {
            "gender": "Male",
            "height": [
                "6'8",
                "203 cm"
            ],
        },
        "work": {
            "occupation": "Musician, adventurer, author",
        },
        },
    2: {"name": "Garry",
        "appearance": {
            "gender": "Male",
            "height": [
                "5'8",
                "103 cm"
            ],
        },
        "work": {
            "occupation": "Musician, author",
        },
        },
    3: {"name": "Ilon",
        "appearance": {
            "gender": "Male",
            "height": [
                "6'8",
                "203 cm"
            ]
        },
        "work": {
            "occupation": "-",
        },
        },
    4: {"name": "Bob",
        "appearance": {
            "gender": "Male",
            "height": [
                "5'8",
                "103 cm"
            ],
        },
        "work": {
            "occupation": "-",
        },
        },
    5: {"name": "Ilona",
        "appearance": {
            "gender": "Female",
            "height": [
                "6'8",
                "203 cm"
            ]
        },
        "work": {
            "occupation": "Writer",
        },
        },
    6: {"name": "Kira",
        "appearance": {
            "gender": "Female",
            "height": [
                "5'8",
                "103 cm"
            ],
        },
        "work": {
            "occupation": "Singer",
        },
        },
    7: {"name": "Mary",
        "appearance": {
            "gender": "Female",
            "height": [
                "6'8",
                "203 cm"
            ]
        },
        "work": {
            "occupation": "-",
        },
        },
    8: {"name": "Polly",
        "appearance": {
            "gender": "Female",
            "height": [
                "5'8",
                "103 cm"
            ],
        },
        "work": {
            "occupation": "-",
        },
        },
    9: {"name": "Neo",
        "appearance": {
            "gender": "-",
            "height": [
                "6'8",
                "203 cm"
            ]
        },
        "work": {
            "occupation": "Writer",
        },
        },
    10: {"name": "Judy",
         "appearance": {
            "gender": "-",
            "height": [
                "5'8",
                "103 cm"
            ],
            },
         "work": {
             "occupation": "Singer",
            },
         },
    11: {"name": "Nemo",
         "appearance": {
             "gender": "-",
             "height": [
                "6'8",
                "203 cm"
             ]
            },
         "work": {
            "occupation": "-",
            },
         },
    12: {"name": "Jody",
         "appearance": {
             "gender": "-",
             "height": [
                "5'8",
                "103 cm"
                ],
            },
         "work": {
            "occupation": "-",
            },
         },
}


@pytest.mark.parametrize(
    "gender, has_work, expected_name",
    [
        ("Male", True, "Peter"),  # Проверяет мужчину с работой
        ("Male", False, "Ilon"),  # Проверяет мужчину без работы
        ("Female", True, "Ilona"),  # Проверяет женщину с работой
        ("Female", False, "Mary"),  # Проверяет женщину без работы
        ("-", True, "Neo"),  # Проверяет героя без гендера с работой
        ("-", False, "Nemo"),  # Проверяет героя без гендера без работы
    ]
)
def test_get_max_height_hero_with_different_parameters(
    mock_api_data, gender, has_work, expected_name
):
    """
    В тесте проверяются все комбинации,
    указанные в параметрах.
    """
    mock_api_data(superhero_data)
    result = get_max_height_hero(gender=gender, has_work=has_work)
    assert result["name"] == expected_name, (
        f"Имя героя должно быть '{expected_name}', "
        f"получен результат: '{result['name']}'"
    )


@pytest.mark.parametrize(
    "gender, has_work",
    [
        ("Kvadrober", False),  # Неизвестный гендер вызовет исключение
        ("Male", "Work"),  # Неправильный формат работы вызовет исключение
    ]
)
def test_get_max_height_hero_exceptions(gender, has_work):
    """
    В тесте проверяется, обрабатывает ли код исключения при вводе
    входных параметров в неправильном формате/с неправильным значением.
    """
    with pytest.raises(ValueError):
        get_max_height_hero(gender, has_work)


def test_get_max_height_hero_same_height(mock_api_data):
    """
    В тесте проверяется, что в случае, если у героев одинаковый рост,
    вернется первый герой с таким ростом.
    """
    api_data = {
        1: {
            "name": "Peter",
            "appearance": {
                "gender": "Male",
                "height": [
                    "6'8",
                    "203 cm"
                ],
            },
            "work": {
                "occupation": "Musician, adventurer, author",
            },
            },
        2: {
            "name": "Garry",
            "appearance": {
                "gender": "Male",
                "height": [
                    "6'8",
                    "203 cm"
                ],
            },
            "work": {
                "occupation": "Musician, author",
            },
            },
    }
    mock_api_data(api_data)
    result = get_max_height_hero("Male", True)
    assert result['name'] == "Peter", (
        "Ожидается, что при одинаковом росте героев функция "
        "вернет первого встретившегося героя с таким ростом."
    )


def test_get_max_height_hero_invalid_height(mock_api_data):
    """
    В тесте проверяется, что в случае, если у героя с указанными параметрами,
    отсутствует рост, функция вернет None.
    """
    api_data = {
        1: {
            "name": "Peter",
            "appearance": {
                "gender": "Male",
                "height": [
                    "6'8",
                    "-"
                ],
            },
            "work": {
                "occupation": "Musician, adventurer, author",
            },
            },
    }
    mock_api_data(api_data)
    result = get_max_height_hero("Male", True)
    assert result is None, (
        "Ожидается, что при неверном формате роста героя "
        "функция вернет None."
    )
