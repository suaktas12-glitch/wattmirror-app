import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="WattMirror - Canlı Enerji Ekosistemi",
    page_icon="🌿",
    layout="wide",
)

if "devices" not in st.session_state:
    st.session_state.devices = [
        {"id": "tv", "name": "Salon TV + Uydu", "watt": 140, "essential": False, "is_on": True},
        {"id": "console", "name": "Oyun Konsolu", "watt": 45, "essential": False, "is_on": True},
        {"id": "monitor", "name": "Çalışma Masası Monitör & Lamba", "watt": 85, "essential": False, "is_on": True},
        {"id": "heater", "name": "Elektrikli Oda Isıtıcısı", "watt": 1800, "essential": False, "is_on": True},
        {"id": "fridge", "name": "Buzdolabı", "watt": 120, "essential": True, "is_on": True},
        {"id": "modem", "name": "Wi-Fi Modem", "watt": 15, "essential": True, "is_on": True},
    ]

MAX_BUDGET_WATT = 2200


def calculate_metrics(devices):
    total_watt = sum(d["watt"] for d in devices if d["is_on"])
    score = max(0, min(100, int(100 - (total_watt / MAX_BUDGET_WATT) * 100)))
    monthly_cost = (total_watt * 8 * 30 / 1000) * 2.6
    return total_watt, score, monthly_cost


def turn_off_non_essential():
    for d in st.session_state.devices:
        if not d["essential"]:
            d["is_on"] = False


def reset_demo():
    for d in st.session_state.devices:
        d["is_on"] = True


total_watt, eco_score, monthly_cost = calculate_metrics(st.session_state.devices)

st.title("🌿 WattMirror — Canlı Enerji Ekosistemi")
st.caption("Evdeki elektrik tüketimini yaşayan bir dijital ekosistemle görselleştir ve gereksiz yükleri tek tuşla kapat.")

col_eco, col_ctrl = st.columns([1.3, 1], gap="large")

with col_eco:
    if eco_score >= 75:
        status_title = "🌟 Ekosistem Dengede ve Canlı"
        status_desc = "Harika! Gereksiz enerji tüketimi düşük, dijital ekosistem sağlıklı görünüyor."
        sky_top, sky_bottom = "#a8edea", "#fed6e3"
        tree_scale = 1.0
        leaf_color = "#2ecc71"
        fog_opacity = 0.0
        sun_opacity = 1.0
    elif eco_score >= 40:
        status_title = "⛅ Dikkat: Tüketim Artıyor"
        status_desc = "Bazı cihazlar enerji çekiyor. Birkaçını kapatarak ekosistemi canlandırabilirsin."
        sky_top, sky_bottom = "#cfd9df", "#e2ebf0"
        tree_scale = 0.85
        leaf_color = "#a3cb38"
        fog_opacity = 0.25
        sun_opacity = 0.5
    else:
        status_title = "🌫️ Uyarı: Yüksek Enerji Tüketimi"
        status_desc = "Yüksek güç çeken veya açık unutulan cihazlar ekosistemi olumsuz etkiliyor."
        sky_top, sky_bottom = "#4b6cb7", "#182848"
        tree_scale = 0.7
        leaf_color = "#7f8c8d"
        fog_opacity = 0.55
        sun_opacity = 0.1

    ecosystem_html = f"""
    <div style="
        background: linear-gradient(180deg, {sky_top} 0%, {sky_bottom} 100%);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        position: relative;
        overflow: hidden;
        height: 430px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        font-family: sans-serif;
    ">
        <div style="display:flex; justify-content:space-between; align-items:center; z-index:2;">
            <span style="background:rgba(255,255,255,0.88); padding:8px 14px; border-radius:12px; font-weight:bold; color:#1e272e;">
                Eko-Skor: {eco_score} / 100
            </span>
            <span style="background:rgba(255,255,255,0.88); padding:8px 14px; border-radius:12px; font-weight:bold; color:#1e272e;">
                Anlık Yük: {total_watt} W
            </span>
        </div>

        <svg viewBox="0 0 500 280" style="width:100%; height:290px; z-index:1;">
            <circle cx="410" cy="60" r="32" fill="#f9ca24" opacity="{sun_opacity}" />
            <path d="M0,230 Q140,170 280,230 T500,220 L500,280 L0,280 Z" fill="#27ae60" opacity="0.7"/>
            <path d="M0,245 Q200,195 380,245 T500,240 L500,280 L0,280 Z" fill="#1e8449"/>
            <g transform="translate(250, 235) scale({tree_scale})">
                <rect x="-10" y="-85" width="20" height="85" rx="6" fill="#6d4c41"/>
                <circle cx="0" cy="-105" r="48" fill="{leaf_color}"/>
                <circle cx="-35" cy="-85" r="34" fill="{leaf_color}"/>
                <circle cx="35" cy="-85" r="34" fill="{leaf_color}"/>
                <circle cx="0" cy="-135" r="32" fill="{leaf_color}"/>
            </g>
            <rect x="0" y="0" width="500" height="280" fill="#2c3e50" opacity="{fog_opacity}"/>
        </svg>

        <div style="background:rgba(255,255,255,0.92); padding:12px 16px; border-radius:14px; z-index:2; color:#1e272e;">
            <div style="font-weight:bold; font-size:16px;">{status_title}</div>
            <div style="font-size:13px; color:#485460; margin-top:4px;">{status_desc}</div>
        </div>
    </div>
    """
    components.html(ecosystem_html, height=450)

    m1, m2 = st.columns(2)
    diff_text = f"Hedef Altı: {600 - total_watt} W" if total_watt <= 600 else f"+{total_watt - 600} W Fazla"
    m1.metric("Anlık Ev Tüketimi", f"{total_watt} W", delta=diff_text, delta_color="inverse")
    m2.metric("Tahmini Aylık Yük Maliyeti", f"{monthly_cost:.0f} TL / ay")

with col_ctrl:
    st.subheader("🔌 Evdeki Cihazlar & Tasarruf Kontrolü")
    st.write("Cihazları tek tek kapatabilir veya gereksiz yükleri tek tuşla durdurabilirsin:")

    b1, b2 = st.columns(2)
    with b1:
        st.button(
            "🌙 Tasarruf Modu",
            on_click=turn_off_non_essential,
            use_container_width=True,
            type="primary",
        )
    with b2:
        st.button(
            "🔄 Tümünü Aç",
            on_click=reset_demo,
            use_container_width=True,
        )

    st.divider()

    for idx, device in enumerate(st.session_state.devices):
        c_name, c_watt, c_toggle = st.columns([3, 1.2, 1])
        with c_name:
            badge = " 🔒 *(Temel)*" if device["essential"] else ""
            st.markdown(f"**{device['name']}**{badge}")
        with c_watt:
            st.write(f"`{device['watt']} W`")
        with c_toggle:
            new_state = st.toggle(
                "Durum",
                value=device["is_on"],
                key=f"toggle_{device['id']}",
                label_visibility="collapsed",
            )
            if new_state != device["is_on"]:
                st.session_state.devices[idx]["is_on"] = new_state
                st.rerun()

    st.divider()

    active_high_loads = [d for d in st.session_state.devices if d["is_on"] and not d["essential"]]
    if active_high_loads:
        top_device = max(active_high_loads, key=lambda x: x["watt"])
        saved_tl = (top_device["watt"] * 8 * 30 / 1000) * 2.6
        st.warning(
            f"💡 **Öneri:** En yüksek gereksiz yük **{top_device['name']}** ({top_device['watt']} W). "
            f"Kapattığında ayda yaklaşık **{saved_tl:.0f} TL** tasarruf sağlayabilirsin."
        )
    else:
        st.success("✅ Evde yalnızca temel cihazlar çalışıyor.")