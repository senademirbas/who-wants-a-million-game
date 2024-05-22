import requests
import random

url = " https://turkiyeapi.dev/api/v1/provinces"

def get_turkey_cities():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        turkey_data = data[0]
        cities = turkey_data.get("subregion", [])
        return cities
    else:
        print("API'ye erişim sağlanamadi.")
        return []

def collect_word() -> str:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cities = data.get("data", [])  # API'nin döndürdüğü veriyi doğru şekilde işlemek için gerekli değişiklik
        city_names = [city['name'] for city in cities]
        return random.choice(city_names)
    else:
        return "Unknown"
    
def createSecret(word:str ,hash_count:int)->str:
    word_len = len(word)
    latter_list = list(word)
    for i in range(hash_count):
        random_index = random.randint(0, word_len - 1)
        latter_list[random_index] = "*"
    secret = "".join(latter_list)
    return secret

    