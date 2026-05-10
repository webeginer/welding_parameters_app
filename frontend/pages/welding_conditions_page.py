# frontend/pages/welding_conditions_page.py
import streamlit as st
import requests
import os


# ---------- НАСТРОЙКА АДРЕСА БЭКЕНДА ----------
# Единый адрес для всех запросов к бэкенду
if os.getenv("RENDER"):
    # На Render — используем публичный адрес и явный путь /calculate
    BASE_API_URL = os.getenv("API_URL", "https://welding-backend-ap4o.onrender.com")
else:
    # Локально — localhost:8000
    BASE_API_URL = "http://localhost:8000"

# Полный адрес для эндпоинта расчёта
API_URL = f"{BASE_API_URL}/calculate"

# Отладочный вывод (временно)
st.sidebar.caption(f"🌐 Отправляю запрос на: {API_URL}")

st.markdown("""
<style>
    /* Скрываем стандартный сайдбар и верхнюю панель */
    section[data-testid="stSidebar"] { display: none; }
    .stApp header { display: none; }
    .stAppDeployButton { display: none; }
    .stActionButtons { display: none; }
    
    /* Основные настройки */
    .main > div { padding-left: 0rem; padding-right: 0rem; }
    .block-container { 
        padding-top: 2.2rem; 
        padding-bottom: 0rem; 
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 1300px; 
        margin: 0 auto; 
    }
    
    /* Уменьшаем высоту контейнеров элементов */
    .stElementContainer {
        min-height: 0px !important;
        margin-bottom: -0.2rem !important;
    }
    
    /* Компактные поля */
    .stNumberInput, .stSelectbox {
        margin-bottom: 0rem;
    }
    
    /* Подписи полей */
    .field-label {
        font-size: 0.7rem;
        color: #555;
        margin-bottom: 0rem;
        line-height: 1.2;
    }
    
    /* Кнопка расчёта */
    .stButton button { 
        background-color: #ff6b35; 
        color: white; 
        font-weight: bold; 
        width: 100%; 
        margin-top: 0rem;
        padding: 0.3rem 0rem;
    }
    .stButton button:hover { background-color: #e55a2b; }
    
    /* Метрики */
    div[data-testid="stMetricValue"] { 
        font-size: 1.8rem !important; 
        font-weight: normal !important; 
    }
    div[data-testid="stMetricLabel"] { 
        font-size: 0.7rem !important; 
        color: #666 !important; 
    }
    
    /* Подзаголовки */
    .section-header {
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.2rem 0 0.3rem 0;
        color: #1e3a5f;
    }
    
    /* Компактный чекбокс */
    .stCheckbox {
        margin-top: 0rem;
        margin-bottom: 0rem;
    }
    
    /* Уменьшаем отступы в строках */
    .row-widget {
        margin-bottom: -0.3rem;
    }
    
    /* Скрываем лишние div-контейнеры */
    .st-emotion-cache-17lr0tt {
        min-height: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
    }
    
    /* Уменьшаем высоту selectbox контейнеров */
    div[data-testid="stSelectbox"] > div {
        min-height: 0px;
    }
    
    /* Убираем разделители */
    hr {
        display: none;
    }
</style>
""", unsafe_allow_html=True)


def format_number(value):
    if isinstance(value, (int, float)):
        return str(value).replace('.', ',')
    return value


# Скрываем верхнюю панель через JS
st.markdown("""
<script>
    window.onload = function() {
        const header = document.querySelector('header');
        if (header) header.style.display = 'none';
        const deploy = document.querySelector('.stAppDeployButton');
        if (deploy) deploy.style.display = 'none';
        
        const containers = document.querySelectorAll('.stElementContainer');
        containers.forEach(el => {
            el.style.minHeight = '0px';
            el.style.margin = '0px';
        });
    }
</script>
""", unsafe_allow_html=True)

# Инициализация session state для катета
if "leg_value" not in st.session_state:
    st.session_state.leg_value = 6.0

# -- ЛЕВАЯ КОЛОНКА (ВСЕ ПАРАМЕТРЫ) --
col_left, col_right = st.columns([0.45, 0.55], gap="small")

with col_left:
    st.markdown('<div class="section-header">Исходные параметры</div>',
                unsafe_allow_html=True)

    # Строка 1: метод сварки и металл
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown('<div class="field-label">метод сварки</div>',
                    unsafe_allow_html=True)
        method = st.selectbox(
            "Метод сварки",
            options=["Ручная (MMA)", "Аргонодуговая (TIG)",
                     "Полуавтоматическая (MIG/MAG)"],
            index=0,
            label_visibility="hidden"
        )
    with col_m2:
        st.markdown('<div class="field-label">металл</div>',
                    unsafe_allow_html=True)
        material = st.selectbox(
            "Тип металла",
            options=["Углеродистая сталь",
                     "Алюминий и его сплавы", "Нержавеющая сталь"],
            index=0,
            label_visibility="hidden"
        )

    method_code = {"Ручная (MMA)": "MMA", "Аргонодуговая (TIG)": "TIG",
                   "Полуавтоматическая (MIG/MAG)": "MIG-MAG"}[method]
    material_code = {"Углеродистая сталь": "Сталь углеродистая",
                     "Алюминий и его сплавы": "Алюминий", "Нержавеющая сталь": "Нержавеющая"}[material]

    # Строка 2: ГОСТ, соединение, тип, катет
    col_g1, col_g2, col_g3, col_g4 = st.columns([1, 1, 1, 0.8])
    with col_g1:
        if method_code == "TIG" and material_code == "Алюминий":
            gost_options = ["gost_14806_80"]
            gost_labels = ["ГОСТ 14806-80"]
            gost_disabled = True
        elif method_code == "MMA":
            gost_options = ["gost_5264_80"]
            gost_labels = ["ГОСТ 5264-80"]
            gost_disabled = True
        else:
            gost_options = ["gost_14771_76", "gost_23518_79"]
            gost_labels = ["ГОСТ 14771-76", "ГОСТ 23518-79"]
            gost_disabled = False

        st.markdown('<div class="field-label">Сварка по</div>',
                    unsafe_allow_html=True)
        st.selectbox(
            "ГОСТ", 
            options=gost_options, 
            format_func=lambda x: gost_labels[gost_options.index(x)], 
            disabled=gost_disabled, 
            key="gost_main", 
            label_visibility="hidden"
        )

    JOINT_GROUPS = {
        "Стыковое": ["C1", "C2", "C3", "C4", "C5"],
        "Угловое": ["У1", "У2", "У3", "У4", "У5", "У6", "У7", "У8", "У9", "У10"],
        "Тавровое": ["Т1", "Т2", "Т3", "Т4", "Т5", "Т6", "Т7", "Т8", "Т9"],
        "Нахлесточное": ["Н1", "Н2"]
    }
    with col_g2:
        st.markdown('<div class="field-label">Соединение</div>',
                    unsafe_allow_html=True)
        joint_group = st.selectbox(
            "Тип соединения", 
            options=list(JOINT_GROUPS.keys()), 
            index=0, 
            label_visibility="hidden"
        )
    with col_g3:
        st.markdown('<div class="field-label">Тип</div>',
                    unsafe_allow_html=True)
        joint_type = st.selectbox(
            "Тип соединения детали", 
            options=JOINT_GROUPS[joint_group], 
            index=0, 
            label_visibility="hidden"
        )
    with col_g4:
        # Катет только для угловых и тавровых
        if joint_group in ["Угловое", "Тавровое"]:
            st.markdown('<div class="field-label">📐</div>',
                        unsafe_allow_html=True)
            leg = st.number_input(
                "Катет шва (мм)",
                min_value=1.0,
                max_value=100.0,
                value=st.session_state.leg_value,
                step=0.5,
                format="%.1f",
                key="leg",
                label_visibility="hidden"
            )
            st.session_state.leg_value = leg
        else:
            leg = None

    group_code = {"Стыковое": "C", "Угловое": "У",
                  "Тавровое": "Т", "Нахлесточное": "Н"}[joint_group]

    st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)

    # Геометрия детали
    st.markdown('<div class="section-header">Геометрия детали</div>',
                unsafe_allow_html=True)
    col_t, col_l = st.columns(2)
    with col_t:
        st.markdown('<div class="field-label">Толщина, мм</div>',
                    unsafe_allow_html=True)
        thickness = st.number_input(
            "Толщина металла (мм)", 
            min_value=0.5, 
            max_value=100.0, 
            value=6.0,
            step=0.5, 
            format="%.1f", 
            key="thickness", 
            label_visibility="hidden"
        )
        # Синхронизация катета с толщиной
        if leg is not None:
            if st.session_state.leg_value > thickness:
                st.session_state.leg_value = thickness
                st.rerun()
    with col_l:
        st.markdown('<div class="field-label">Длина, мм</div>',
                    unsafe_allow_html=True)
        length = st.number_input(
            "Длина детали (мм)", 
            min_value=10, 
            max_value=10000,
            value=500, 
            step=50, 
            key="length", 
            label_visibility="hidden"
        )

    st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)

    # Дополнительно
    st.markdown('<div class="section-header">Дополнительно</div>',
                unsafe_allow_html=True)

    # Положение шва
    st.markdown('<div class="field-label">Положение шва</div>',
                unsafe_allow_html=True)
    position = st.selectbox(
        "Положение сварного шва", 
        options=["Нижнее", "Вертикальное", "Потолочное"], 
        index=0, 
        label_visibility="hidden"
    )
    position_code = {"Нижнее": "lower", "Вертикальное": "vertical",
                     "Потолочное": "ceiling"}[position]

    # Газовая смесь
    use_gas = False
    gas_mixture = None
    if method_code in ["TIG", "MIG-MAG"]:
        use_gas = st.checkbox("Газовая смесь")
        if use_gas:
            if method_code == "TIG":
                gas_mixture = st.selectbox(
                    "Газовая смесь TIG", 
                    options=["75% Ar + 25% He", "90% Ar + 10% H₂"], 
                    index=0,
                    label_visibility="hidden"
                )
            else:
                gas_mixture = st.selectbox(
                    "Газовая смесь MIG/MAG", 
                    options=["80% Ar + 20% CO₂", "82% Ar + 18% CO₂", "90% Ar + 10% CO₂"], 
                    index=0,
                    label_visibility="hidden"
                )

    # Кнопка расчёта
    calculate = st.button("Рассчитать", type="primary",
                          use_container_width=True)

# -- ПРАВАЯ КОЛОНКА (РЕЗУЛЬТАТЫ) --
with col_right:
    if calculate:
        gost_value = gost_options[0] if gost_options else "gost_5264_80"

        # Марка электрода для рекомендаций
        electrode_brand = "УОНИ 13/45"

        payload = {
            "method": method_code,
            "material": material_code,
            "thickness": thickness,
            "joint_group": group_code,
            "joint_type": joint_type,
            "length": length,
            "position": position_code,
            "with_filler": True,
            "gas_mixture": gas_mixture,
            "electrode_brand": None,
            "gost_standard": gost_value,
            "leg": leg
        }

        with st.spinner("..."):
            try:
                response = requests.post(
                    f"{API_URL}/calculate", json=payload, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    params = result.get("parameters", {})

                    st.markdown(
                        '<div class="section-header">Основные параметры</div>', unsafe_allow_html=True)

                    cols = st.columns(4)
                    metrics = [
                        ("Iсв, А", params.get("current", "—")),
                        ("Uсв, В", params.get("voltage", "—")),
                        ("Dэ, мм", params.get("electrode_diameter",
                         params.get("wire_diameter", "—"))),
                        ("Vсв, м/ч", params.get("welding_speed", "—"))
                    ]
                    for i, (label, value) in enumerate(metrics):
                        with cols[i]:
                            st.metric(label, format_number(value))

                    gas = format_number(params.get("gas_flow_rate", "—")) if params.get(
                        "gas_flow_rate") else "—"

                    polarity = params.get("polarity", "—")
                    if "переменный" in polarity.lower():
                        current_symbol = "~"
                        electrode_symbol = "~"
                    elif "прямая" in polarity.lower():
                        current_symbol = "-"
                        electrode_symbol = "-"
                    elif "обратная" in polarity.lower():
                        current_symbol = "-"
                        electrode_symbol = "+"
                    else:
                        current_symbol = "—"
                        electrode_symbol = "—"

                    col_g1, col_g2, col_g3 = st.columns(3)
                    with col_g1:
                        st.metric("Qг, л/мин", gas)
                    with col_g2:
                        st.metric("Род тока", current_symbol)
                    with col_g3:
                        st.metric("На электроде", electrode_symbol)

                    # Рекомендации
                    with st.expander("▶ Рекомендации"):
                        recommendations = ["• Короткая дуга (1,5–3 мм)"]
                        if method_code == "MMA":
                            recommendations.append(
                                f"• Марка электрода: {electrode_brand}")
                        if leg is not None:
                            recommendations.append(
                                f"• Катет шва не более: {format_number(leg)} мм")
                        for rec in recommendations:
                            st.markdown(rec)

                    # Дополнительные параметры
                    with st.expander("▶ Дополнительные параметры"):
                        Gn = thickness * length * 7.85 / 1000
                        alpha_n = params.get("deposition_coefficient", 8)
                        I = params.get("current", 150)
                        t0 = Gn / (alpha_n * I) if alpha_n and I else 0
                        t0_min = t0 * 60
                        T = t0 / 0.55
                        T_min = T * 60
                        G_el = Gn * 1.65
                        A = (params.get("voltage", 25) * I /
                             0.75 / 1000) * t0 if I else 0

                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(
                                "Время горения дуги, мин", f"{format_number(round(t0_min, 1))}" if t0_min else "—")
                            st.metric(
                                "Расход электродов, г", f"{format_number(round(G_el))}" if G_el else "—")
                        with col2:
                            st.metric(
                                "Полное время сварки, мин", f"{format_number(round(T_min, 1))}" if T_min else "—")
                            st.metric("Расход э/энергии, кВт·ч",
                                      f"{format_number(round(A, 2))}" if A else "—")

                else:
                    st.error(f"Ошибка: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(f"❌ Бэкенд не отвечает по адресу: {API_URL}")
            except Exception as e:
                st.error(f"⚠️ {str(e)}")
    else:
        st.markdown(
            '<div class="section-header">Основные параметры</div>', unsafe_allow_html=True)
        st.caption("Введите исходные параметры и нажмите «Рассчитать»")