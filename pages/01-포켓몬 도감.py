import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_pokemon_info(pokemon_name):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        search_url = f"https://pokemonkorea.co.kr/pokedex?word={pokemon_name}"
        driver.get(search_url)
        time.sleep(2)

        # 검색 결과 중 첫 번째 항목 클릭
        try:
            first_pokemon_link = driver.find_element(By.CSS_SELECTOR, "ul.pokemon_list li a")
            first_pokemon_link.click()
            time.sleep(2)
        except NoSuchElementException:
            return None, "검색 결과가 없습니다."

        # 상세 페이지에서 정보 추출
        try:
            name = driver.find_element(By.CSS_SELECTOR, ".pokemon_info h3").text.strip()
            number = driver.find_element(By.CSS_SELECTOR, ".pokemon_info .number").text.strip()
            types = [img.get_attribute("alt") for img in driver.find_elements(By.CSS_SELECTOR, ".pokemon_info .type img")]
            img_tag = driver.find_element(By.CSS_SELECTOR, ".img img")
            image_url = img_tag.get_attribute("src") if img_tag else ""
            return {
                "name": name,
                "number": number,
                "types": types,
                "image_url": image_url
            }, None
        except Exception as e:
            return None, f"정보를 불러오는 중 오류 발생: {e}"

    except Exception as e:
        return None, f"Selenium 오류: {e}"
    finally:
        driver.quit()

# --- Streamlit UI 구성 ---

st.set_page_config(page_title="포켓몬 도감 검색기", layout="centered")
st.title("🔍 포켓몬 도감 검색기")

pokemon_name = st.text_input("포켓몬 이름을 입력하세요 (예: 피카츄, 메타몽)")

if pokemon_name:
    with st.spinner("검색 중..."):
        data, error = get_pokemon_info(pokemon_name)

        if error:
            st.error(error)
        elif data:
            st.subheader(f"{data['name']} (#{data['number']})")
            if data['image_url']:
                st.image(data['image_url'], width=200)
            st.markdown(f"**타입**: {' / '.join(data['types'])}")
        else:
            st.warning("결과를 찾을 수 없습니다.")
