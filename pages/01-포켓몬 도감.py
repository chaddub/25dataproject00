import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

st.set_page_config(page_title="포켓몬 도감 검색기", layout="centered")
st.title("🔍 포켓몬 도감 검색기")

pokemon_name = st.text_input("포켓몬 이름을 입력하세요 (예: 메타몽)")

if pokemon_name:
    with st.spinner("검색 중..."):
        try:
            # Selenium WebDriver 설정
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # 브라우저 창을 띄우지 않음
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            # 포켓몬코리아 도감 페이지 접속
            search_url = f"https://pokemonkorea.co.kr/pokedex?word={pokemon_name}"
            driver.get(search_url)
            time.sleep(3)  # 페이지 로딩 대기

            # 검색 결과에서 첫 번째 포켓몬 선택
            try:
                first_pokemon = driver.find_element(By.CSS_SELECTOR, "ul.pokemon_list li a")
                first_pokemon.click()
                time.sleep(3)  # 상세 페이지 로딩 대기

                # 포켓몬 정보 추출
                name = driver.find_element(By.CSS_SELECTOR, ".pokemon_info h3").text.strip()
                number = driver.find_element(By.CSS_SELECTOR, ".pokemon_info .number").text.strip()
                type_elements = driver.find_elements(By.CSS_SELECTOR, ".pokemon_info .type img")
                types = [elem.get_attribute("alt") for elem in type_elements]
                image_element = driver.find_element(By.CSS_SELECTOR, ".img img")
                image_url = image_element.get_attribute("src") if image_element else ""

                # 결과 출력
                st.subheader(f"📘 {name} (#{number})")
                if image_url:
                    st.image(image_url, width=200)
                st.markdown(f"**타입**: {' / '.join(types)}")

            except Exception as e:
                st.warning("해당 이름의 포켓몬을 찾을 수 없습니다.")

            driver.quit()

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
