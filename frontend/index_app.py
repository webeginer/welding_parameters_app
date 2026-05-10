# frontend/index_app.py
import streamlit as st
import os
import requests  # добавлено для работы с API

# ---------- НАСТРОЙКА АДРЕСА БЭКЕНДА ----------
# Определяем, где запущено приложение
if os.getenv("STREAMLIT_SHARING") == "true" or os.getenv("STREAMLIT_CLOUD") == "true":
    # Режим Streamlit Cloud
    API_URL = os.getenv("API_URL", "https://welding-backend-ap4o.onrender.com")
else:
    # Локальный режим
    API_URL = "http://localhost:8000"

# Для отладки (можно потом удалить)
st.sidebar.caption(f"🌐 API: {API_URL}")

st.set_page_config(
    page_title="Калькулятор сварщика",
    page_icon="🧑‍🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Стилизация
st.markdown("""
<style>
    /* Скрываем сайдбар */
    section[data-testid="stSidebar"] {
        display: none;
    }
    .main > div {
        padding-left: 0rem;
        padding-right: 0rem;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .welcome-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .welcome-title {
        font-size: 2.8rem;
        font-weight: bold;
        color: #1e3a5f;
        margin-bottom: 0.5rem;
    }
    .welcome-subtitle {
        font-size: 1.1rem;
        color: #666;
    }
    .card-container {
        display: flex;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    .card {
        flex: 1;
        background-color: #f8f9fa;
        border-radius: 16px;
        padding: 1.8rem;
        border-left: 4px solid #ff6b35;
        transition: transform 0.2s;
        height: 100%;
        display: flex;
        flex-direction: column;
        min-height: 420px;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .card-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .card-description {
        color: #444;
        line-height: 1.5;
        margin-bottom: 0.8rem;
        font-size: 0.95rem;
    }
    .card-footer {
        margin-top: auto;
        padding-top: 1rem;
    }
    hr {
        margin: 0.5rem 0;
    }
    /* Стиль для кнопок Streamlit внутри карточек */
    .stButton button {
        background-color: #ff6b35;
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        font-size: 1rem;
    }
    .stButton button:hover {
        background-color: #e55a2b;
    }
    .stButton button:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }
</style>
""", unsafe_allow_html=True)

# Заголовок
st.markdown("""
<div class="welcome-header">
    <div class="welcome-title">🧑‍🏭 Калькулятор сварщика</div>
    <div class="welcome-subtitle">Расчёт параметров дуговой сварки и прогнозирования усадки соединений</div>
</div>
""", unsafe_allow_html=True)

# Карточки
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">
            📋 Параметры сварки плавлением
        </div>
        <div class="card-description">
            Режимы сварки плавлением зависят от толщины свариваемых деталей, марки и состава металла, типа соединения.
        </div>
        <div class="card-description">
            Выбор режимов определяет физические, химические и металлургические процессы, формирующие сварное соединение и его характеристики.
        </div>
        <div class="card-description">
            Правильный режим обеспечивает монолитное соединение с требуемой прочностью. Ошибки ведут к дефектам: непроварам, порам, трещинам.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Калькулятор режимов", key="btn_params", use_container_width=True):
        st.switch_page("pages/welding_conditions_page.py")

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">
            📐 Усадка сварного соединения
        </div>
        <div class="card-description">
            Усадка зависит от объёма наплавленного металла, типа соединения (стыковое, тавровое) и режима сварки.
        </div>
        <div class="card-description">
            Продольная усадка вызывает изгиб конструкции, поперечная — уменьшение ширины или зазоров между деталями.
        </div>
        <div class="card-description">
            Расчёт усадки необходим для компенсации деформаций. После остывания конструкция будет соответствовать проектным размерам.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.button("Калькулятор усадки", key="btn_shrink",
              disabled=True, use_container_width=True)