"""
Livro Digital de Amor - Versão Python (Streamlit)
Crie livros digitais românticos personalizados.
"""

import streamlit as st
from streamlit_option_menu import option_menu
import base64
from io import BytesIO
from datetime import datetime, date
from PIL import Image
import json
import uuid
import os

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Livro Digital de Amor ❤️",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');
    
    .main {
        background: linear-gradient(135deg, #fff1f2 0%, #fdf8f3 50%, #ffe4e6 100%);
    }
    
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #be123c !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(244, 63, 94, 0.4) !important;
    }
    
    .book-page {
        background: linear-gradient(to right, #faf7f2 0%, #fffefb 100%);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(190, 18, 60, 0.1);
        border: 1px solid #fecdd3;
        min-height: 500px;
        margin-bottom: 1.5rem;
    }
    
    .cover-page {
        background: linear-gradient(135deg, #f43f5e 0%, #be123c 100%);
        color: white;
        text-align: center;
        padding: 3rem 2rem;
        border-radius: 16px;
        min-height: 450px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .page-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: #be123c;
        margin-bottom: 1rem;
    }
    
    .page-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        line-height: 1.7;
        color: #4a1c2e;
        white-space: pre-wrap;
    }
    
    .caption {
        font-style: italic;
        color: #e11d48;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    .special-date-card {
        background: #fff1f2;
        border-left: 4px solid #f43f5e;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
    }
    
    .step-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff1f2 0%, #fdf8f3 100%);
    }
    
    .stProgress > div > div {
        background-color: #f43f5e !important;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# ESTADO INICIAL
# ============================================================
def init_session():
    defaults = {
        "step": "inicio",
        "from_name": "",
        "to_name": "",
        "nickname": "",
        "start_date": None,
        "special_date": None,
        "intro_message": "",
        "photos": [],          # lista de dicts {id, data, caption, filename}
        "cover_photo_idx": 0,
        "pages": get_default_pages(),
        "special_dates": [],
        "current_page_idx": 0,
        "book_id": str(uuid.uuid4()),
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def get_default_pages():
    return [
        {
            "id": "cover",
            "type": "cover",
            "title": "Uma história chamada nós.",
            "text": "",
            "photo_idx": None,
            "caption": "",
        },
        {
            "id": "inicio",
            "type": "content",
            "title": "Nosso Começo",
            "text": "Antes de você, eu não sabia que alguém poderia transformar tantos pequenos momentos em lembranças tão especiais.",
            "photo_idx": None,
            "caption": "",
        },
        {
            "id": "conheci",
            "type": "content",
            "title": "Quando Te Conheci",
            "text": "Conte aqui como vocês se conheceram... o primeiro olhar, a primeira conversa, o momento em que tudo mudou.",
            "photo_idx": None,
            "caption": "",
        },
        {
            "id": "amo",
            "type": "content",
            "title": "O Que Eu Mais Amo Em Você",
            "text": "Liste as qualidades, os detalhes e os momentos que fazem você amar essa pessoa todos os dias.",
            "photo_idx": None,
            "caption": "",
        },
        {
            "id": "momentos",
            "type": "content",
            "title": "Nossos Momentos",
            "text": "Pequenas lembranças que guardamos no coração.",
            "photo_idx": None,
            "caption": "",
        },
        {
            "id": "lugar",
            "type": "content",
            "title": "Meu Lugar Favorito",
            "text": "Estar ao seu lado faz qualquer lugar parecer o melhor do mundo. Você é o meu lar.",
            "photo_idx": None,
            "caption": "",
        },
        {
            "id": "planos",
            "type": "content",
            "title": "Nossos Planos",
            "text": "Sonhos, viagens, objetivos e todas as experiências que queremos viver juntos.",
            "photo_idx": None,
            "caption": "",
        },
        {
            "id": "datas",
            "type": "dates",
            "title": "Datas Especiais",
            "text": "Momentos importantes que queremos celebrar.",
            "photo_idx": None,
            "caption": "",
        },
        {
            "id": "promessa",
            "type": "promise",
            "title": "Uma Promessa",
            "text": "Escreva aqui uma promessa ou declaração especial para a pessoa amada.",
            "photo_idx": None,
            "caption": "",
        },
        {
            "id": "final",
            "type": "final",
            "title": "Se eu pudesse escolher novamente...",
            "text": "ainda escolheria você.",
            "photo_idx": None,
            "caption": "",
        },
    ]


# ============================================================
# UTILITÁRIOS
# ============================================================
def image_to_base64(img: Image.Image) -> str:
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode()


def compress_image(uploaded_file, max_size=1200) -> Image.Image:
    img = Image.open(uploaded_file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    w, h = img.size
    if max(w, h) > max_size:
        ratio = max_size / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)
    return img


def days_together(start_date):
    if not start_date:
        return None
    return (date.today() - start_date).days


def countdown_days(target_date):
    if not target_date:
        return None
    delta = (target_date - date.today()).days
    return delta


# ============================================================
# TELAS
# ============================================================
def tela_inicio():
    st.markdown("""
    <div style="text-align:center; padding: 3rem 1rem;">
        <div style="font-size: 4.5rem; margin-bottom: 1rem;">📖</div>
        <h1 style="font-size: 2.8rem; margin-bottom: 0.5rem;">
            Crie uma história<br>para quem você ama ❤️
        </h1>
        <p style="font-size: 1.2rem; color: #9f1239; max-width: 500px; margin: 1.5rem auto 2.5rem;">
            Transforme suas memórias, fotografias e sentimentos em um livro inesquecível.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Criar meu livro", use_container_width=True):
            st.session_state.step = "personalizar"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("📸 **Suas fotos**\n\nAdicione fotografias especiais e legendas carinhosas")
    with c2:
        st.info("✍️ **Suas palavras**\n\nEscreva declarações, promessas e momentos únicos")
    with c3:
        st.info("🎁 **Presente digital**\n\nVisualize, baixe ou compartilhe seu livro")


def tela_personalizar():
    st.markdown('<div class="step-header"><h2>💌 Personalize seu livro</h2><p>Preencha os detalhes do seu presente especial</p></div>', unsafe_allow_html=True)

    with st.form("form_personalizar"):
        col1, col2 = st.columns(2)
        with col1:
            from_name = st.text_input("Seu nome *", value=st.session_state.from_name, placeholder="Ex: Ana")
        with col2:
            to_name = st.text_input("Nome de quem vai receber *", value=st.session_state.to_name, placeholder="Ex: Pedro")

        nickname = st.text_input("Apelido carinhoso (opcional)", value=st.session_state.nickname, placeholder="Ex: Meu amor, Princesa...")

        col3, col4 = st.columns(2)
        with col3:
            start_date = st.date_input("Quando começaram a namorar", value=st.session_state.start_date or None, format="DD/MM/YYYY")
        with col4:
            special_date = st.date_input("Data especial para comemorar", value=st.session_state.special_date or None, format="DD/MM/YYYY")

        intro = st.text_area("Mensagem de introdução", value=st.session_state.intro_message, height=100,
                             placeholder="Uma mensagem especial para abrir o livro...")

        submitted = st.form_submit_button("Continuar para as fotos →", use_container_width=True)

        if submitted:
            if not from_name.strip() or not to_name.strip():
                st.error("Por favor, preencha pelo menos os nomes.")
            else:
                st.session_state.from_name = from_name.strip()
                st.session_state.to_name = to_name.strip()
                st.session_state.nickname = nickname.strip()
                st.session_state.start_date = start_date
                st.session_state.special_date = special_date
                st.session_state.intro_message = intro.strip()
                st.session_state.step = "fotos"
                st.rerun()

    if st.button("← Voltar"):
        st.session_state.step = "inicio"
        st.rerun()


def tela_fotos():
    st.markdown('<div class="step-header"><h2>📷 Adicione fotografias</h2><p>Escolha as fotos que farão parte do livro</p></div>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Envie uma ou várias fotos",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        key="uploader"
    )

    if uploaded:
        for f in uploaded:
            # Evita duplicatas pelo nome
            if any(p["filename"] == f.name for p in st.session_state.photos):
                continue
            try:
                img = compress_image(f)
                st.session_state.photos.append({
                    "id": str(uuid.uuid4()),
                    "data": image_to_base64(img),
                    "caption": "",
                    "filename": f.name,
                })
            except Exception as e:
                st.warning(f"Não foi possível processar {f.name}: {e}")

    photos = st.session_state.photos

    if photos:
        st.success(f"{len(photos)} foto(s) adicionada(s)")
        st.markdown("#### Gerenciar fotos")

        for i, photo in enumerate(photos):
            col_img, col_info = st.columns([1, 3])
            with col_img:
                st.image(base64.b64decode(photo["data"]), use_container_width=True)
            with col_info:
                caption = st.text_input("Legenda", value=photo["caption"], key=f"cap_{photo['id']}", placeholder="Uma legenda carinhosa...")
                st.session_state.photos[i]["caption"] = caption

                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("⭐ Capa", key=f"cover_{i}"):
                        st.session_state.cover_photo_idx = i
                        st.rerun()
                with c2:
                    if st.button("🗑️ Excluir", key=f"del_{i}"):
                        st.session_state.photos.pop(i)
                        if st.session_state.cover_photo_idx >= len(st.session_state.photos):
                            st.session_state.cover_photo_idx = max(0, len(st.session_state.photos) - 1)
                        st.rerun()
                with c3:
                    if st.session_state.cover_photo_idx == i:
                        st.markdown("**✓ Capa atual**")
            st.divider()

        # Auto-associa fotos às páginas
        for idx, page in enumerate(st.session_state.pages):
            if page["type"] not in ("dates", "promise") and page["photo_idx"] is None and idx - 1 < len(photos):
                # Atribui sequencialmente
                pass
        # Atribuição simples: capa + páginas seguintes
        if st.session_state.pages[0]["photo_idx"] is None and photos:
            st.session_state.pages[0]["photo_idx"] = st.session_state.cover_photo_idx
            for j in range(1, min(len(st.session_state.pages), len(photos) + 1)):
                if st.session_state.pages[j]["type"] not in ("dates", "promise"):
                    photo_i = (j - 1) % len(photos)
                    st.session_state.pages[j]["photo_idx"] = photo_i

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("← Voltar"):
            st.session_state.step = "personalizar"
            st.rerun()
    with col_b:
        label = f"Continuar com {len(photos)} foto(s) →" if photos else "Continuar sem fotos →"
        if st.button(label, use_container_width=True):
            st.session_state.step = "editor"
            st.rerun()


def tela_editor():
    st.markdown('<div class="step-header"><h2>✏️ Editor de Páginas</h2></div>', unsafe_allow_html=True)

    pages = st.session_state.pages
    idx = st.session_state.current_page_idx
    page = pages[idx]

    # Seletor de páginas
    page_labels = [f"{i+1}. {p['title'][:25]}" for i, p in enumerate(pages)]
    selected = st.selectbox("Página atual", options=range(len(pages)), format_func=lambda i: page_labels[i], index=idx)
    if selected != idx:
        st.session_state.current_page_idx = selected
        st.rerun()

    st.markdown("---")

    col_edit, col_preview = st.columns([1, 1])

    with col_edit:
        st.subheader("Editar conteúdo")
        new_title = st.text_input("Título", value=page["title"], key=f"title_{idx}")
        new_text = st.text_area("Texto romântico", value=page["text"], height=180, key=f"text_{idx}")
        new_caption = st.text_input("Legenda da foto", value=page.get("caption", ""), key=f"caption_{idx}")

        # Escolher foto
        if st.session_state.photos and page["type"] not in ("dates",):
            options = ["Nenhuma"] + [f"Foto {i+1}: {p['filename'][:20]}" for i, p in enumerate(st.session_state.photos)]
            current_photo = page["photo_idx"]
            default_idx = (current_photo + 1) if current_photo is not None else 0
            chosen = st.selectbox("Foto desta página", options=options, index=min(default_idx, len(options)-1), key=f"photo_sel_{idx}")
            if chosen == "Nenhuma":
                page["photo_idx"] = None
            else:
                page["photo_idx"] = options.index(chosen) - 1

        # Datas especiais
        if page["type"] == "dates":
            st.markdown("#### Eventos especiais")
            if st.button("➕ Adicionar evento"):
                st.session_state.special_dates.append({
                    "id": str(uuid.uuid4()),
                    "name": "",
                    "date": None,
                    "description": "",
                    "countdown": True,
                })
                st.rerun()

            for i, ev in enumerate(st.session_state.special_dates):
                with st.expander(f"Evento {i+1}: {ev['name'] or 'Sem nome'}", expanded=True):
                    ev["name"] = st.text_input("Nome do evento", value=ev["name"], key=f"ev_name_{i}")
                    ev["date"] = st.date_input("Data", value=ev["date"], key=f"ev_date_{i}", format="DD/MM/YYYY")
                    ev["description"] = st.text_area("Descrição", value=ev["description"], key=f"ev_desc_{i}", height=80)
                    ev["countdown"] = st.checkbox("Mostrar contagem regressiva", value=ev.get("countdown", True), key=f"ev_cd_{i}")
                    if st.button("Remover evento", key=f"ev_del_{i}"):
                        st.session_state.special_dates.pop(i)
                        st.rerun()

        # Salvar alterações da página
        pages[idx]["title"] = new_title
        pages[idx]["text"] = new_text
        pages[idx]["caption"] = new_caption
        st.session_state.pages = pages

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("← Página anterior") and idx > 0:
                st.session_state.current_page_idx = idx - 1
                st.rerun()
        with c2:
            st.markdown(f"<p style='text-align:center;padding-top:0.5rem'>{idx+1} / {len(pages)}</p>", unsafe_allow_html=True)
        with c3:
            if st.button("Próxima página →") and idx < len(pages) - 1:
                st.session_state.current_page_idx = idx + 1
                st.rerun()

    with col_preview:
        st.subheader("Pré-visualização")
        render_page(page, idx)

    st.markdown("---")
    col_back, col_next = st.columns(2)
    with col_back:
        if st.button("← Voltar para fotos"):
            st.session_state.step = "fotos"
            st.rerun()
    with col_next:
        if st.button("📖 Visualizar livro completo →", use_container_width=True):
            st.session_state.step = "visualizar"
            st.session_state.current_page_idx = 0
            st.rerun()


def render_page(page, idx):
    """Renderiza uma página do livro de forma bonita."""
    photos = st.session_state.photos
    photo_b64 = None
    if page.get("photo_idx") is not None and 0 <= page["photo_idx"] < len(photos):
        photo_b64 = photos[page["photo_idx"]]["data"]

    if page["type"] == "cover" or page["type"] == "final":
        # Capa / Final com visual especial
        st.markdown(f"""
        <div class="cover-page">
            <h1 style="color:white; font-size:2.2rem; margin-bottom:1rem;">{page['title']}</h1>
            {"<p style='font-size:1.3rem; margin-bottom:0.5rem;'>" + st.session_state.from_name + " & " + st.session_state.to_name + "</p>" if page["type"] == "cover" else ""}
            {"<p style='font-style:italic; opacity:0.9;'>" + st.session_state.nickname + "</p>" if page["type"] == "cover" and st.session_state.nickname else ""}
            {"<p style='margin-top:1.5rem; font-size:1.1rem; max-width:320px;'>" + st.session_state.intro_message + "</p>" if page["type"] == "cover" and st.session_state.intro_message else ""}
            {"<p style='font-size:1.3rem; font-style:italic; margin-top:1rem;'>" + page['text'] + "</p>" if page["type"] == "final" else ""}
        </div>
        """, unsafe_allow_html=True)
        if photo_b64:
            st.image(base64.b64decode(photo_b64), use_container_width=True)
        days = days_together(st.session_state.start_date)
        if page["type"] == "cover" and days and days > 0:
            st.caption(f"💕 {days} dias de história juntos")
    else:
        with st.container():
            st.markdown(f'<div class="book-page">', unsafe_allow_html=True)
            if photo_b64:
                st.image(base64.b64decode(photo_b64), use_container_width=True)
                if page.get("caption"):
                    st.markdown(f'<p class="caption">{page["caption"]}</p>', unsafe_allow_html=True)

            st.markdown(f'<p class="page-title">{page["title"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="page-text">{page["text"]}</p>', unsafe_allow_html=True)

            # Datas especiais
            if page["type"] == "dates" and st.session_state.special_dates:
                for ev in st.session_state.special_dates:
                    days_left = countdown_days(ev.get("date"))
                    cd_html = ""
                    if ev.get("countdown") and days_left is not None:
                        if days_left > 0:
                            cd_html = f'<span style="background:#f43f5e;color:white;padding:2px 8px;border-radius:20px;font-size:0.75rem;">{days_left} dias</span>'
                        elif days_left == 0:
                            cd_html = '<span style="background:#f43f5e;color:white;padding:2px 8px;border-radius:20px;font-size:0.75rem;">É hoje! 🎉</span>'

                    date_str = ev["date"].strftime("%d/%m/%Y") if ev.get("date") else ""
                    st.markdown(f"""
                    <div class="special-date-card">
                        <strong>{ev.get('name') or 'Evento'}</strong> {cd_html}<br>
                        <small style="color:#e11d48;">{date_str}</small>
                        <p style="margin:0.4rem 0 0; font-size:0.9rem;">{ev.get('description', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown(f'<p style="text-align:center; color:#fda4af; font-size:0.8rem; margin-top:1.5rem;">{idx+1} / {len(st.session_state.pages)}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


def tela_visualizar():
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <h2>📖 Livro de {st.session_state.from_name} & {st.session_state.to_name}</h2>
        <p style="color:#9f1239;">Navegue pelas páginas do seu livro de amor</p>
    </div>
    """, unsafe_allow_html=True)

    pages = st.session_state.pages
    idx = st.session_state.current_page_idx

    # Controles de navegação
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    with col1:
        if st.button("⏮️ Início"):
            st.session_state.current_page_idx = 0
            st.rerun()
    with col2:
        if st.button("← Anterior") and idx > 0:
            st.session_state.current_page_idx = idx - 1
            st.rerun()
    with col3:
        st.markdown(f"<h4 style='text-align:center; color:#be123c;'>{idx+1} / {len(pages)}</h4>", unsafe_allow_html=True)
    with col4:
        if st.button("Próxima →") and idx < len(pages) - 1:
            st.session_state.current_page_idx = idx + 1
            st.rerun()
    with col5:
        if st.button("⏭️ Final"):
            st.session_state.current_page_idx = len(pages) - 1
            st.rerun()

    st.markdown("---")
    render_page(pages[idx], idx)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("✏️ Voltar ao editor"):
            st.session_state.step = "editor"
            st.rerun()
    with c2:
        if st.button("🏠 Início"):
            st.session_state.step = "inicio"
            st.rerun()
    with c3:
        # Exportar dados como JSON (simples)
        book_data = {
            "id": st.session_state.book_id,
            "from_name": st.session_state.from_name,
            "to_name": st.session_state.to_name,
            "nickname": st.session_state.nickname,
            "start_date": str(st.session_state.start_date) if st.session_state.start_date else None,
            "intro_message": st.session_state.intro_message,
            "pages": st.session_state.pages,
            "special_dates": [
                {**d, "date": str(d["date"]) if d.get("date") else None}
                for d in st.session_state.special_dates
            ],
        }
        json_str = json.dumps(book_data, ensure_ascii=False, indent=2)
        st.download_button(
            "💾 Baixar dados (JSON)",
            data=json_str,
            file_name=f"livro_{st.session_state.from_name}_{st.session_state.to_name}.json",
            mime="application/json",
        )


# ============================================================
# MAIN
# ============================================================
def main():
    init_session()

    # Sidebar com progresso
    with st.sidebar:
        st.markdown("## 📖 Livro de Amor")
        steps = {
            "inicio": "1. Início",
            "personalizar": "2. Personalizar",
            "fotos": "3. Fotos",
            "editor": "4. Editor",
            "visualizar": "5. Visualizar",
        }
        current_steps = list(steps.keys())
        current_idx = current_steps.index(st.session_state.step) if st.session_state.step in current_steps else 0

        for i, (key, label) in enumerate(steps.items()):
            if i < current_idx:
                st.markdown(f"✅ ~~{label}~~")
            elif i == current_idx:
                st.markdown(f"**👉 {label}**")
            else:
                st.markdown(f"⬜ {label}")

        st.markdown("---")
        if st.session_state.from_name:
            st.markdown(f"**De:** {st.session_state.from_name}")
            st.markdown(f"**Para:** {st.session_state.to_name}")
            if st.session_state.photos:
                st.markdown(f"**Fotos:** {len(st.session_state.photos)}")

        st.markdown("---")
        st.caption("Feito com ❤️ em Python + Streamlit")

    # Roteamento
    step = st.session_state.step
    if step == "inicio":
        tela_inicio()
    elif step == "personalizar":
        tela_personalizar()
    elif step == "fotos":
        tela_fotos()
    elif step == "editor":
        tela_editor()
    elif step == "visualizar":
        tela_visualizar()


if __name__ == "__main__":
    main()
