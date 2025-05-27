import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="포켓몬 도감 검색기", layout="centered")

st.title("🔍 포켓몬 도감 검색기")
pokemon_name = st.text_input("포켓몬 이름을 입력하세요 (예: 메타몽)")

if pokemon_name:
    search_url = f"https://pokemonkorea.co.kr/pokedex?word={pokemon_name}"

    try:
        response = requests.get(search_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        poke_link_tag = soup.select_one('ul.pokemon_list li a')

        if poke_link_tag:
            poke_url = "https://pokemonkorea.co.kr" + poke_link_tag['href']
            poke_response = requests.get(poke_url)
            poke_soup = BeautifulSoup(poke_response.text, 'html.parser')

            # 포켓몬 이름
            name = poke_soup.select_one('.pokemon_info h3').text.strip()

            # 번호
            number = poke_soup.select_one('.pokemon_info .number').text.strip()

            # 타입
            type_tags = poke_soup.select('.pokemon_info .type img')
            types = [img['alt'] for img in type_tags]

            # 이미지
            image_tag = poke_soup.select_one('.img img')
            image_url = image_tag['src'] if image_tag else ""

            st.subheader(f"📘 {name} (#{number})")
            if image_url:
                st.image(image_url, width=200)

            st.markdown(f"**타입**: {' / '.join(types)}")
        else:
            st.warning("해당 이름의 포켓몬을 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
