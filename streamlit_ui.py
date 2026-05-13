import os
import streamlit as st
from pathlib import Path

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="File Manager",
    page_icon="🗂️",
    layout="wide",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Syne', sans-serif;
    }

    .stApp {
        background: #0d0d0d;
        color: #e8e8e0;
    }

    h1, h2, h3 {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        color: #f5f0e8;
        letter-spacing: -0.05em;
        margin-bottom: 0;
    }

    .subtitle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #888;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-top: 0;
    }

    .stButton > button {
        background: #1a1a1a;
        color: #e8e8e0;
        border: 1px solid #333;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        padding: 0.6rem 1.2rem;
        transition: all 0.15s ease;
        width: 100%;
    }

    .stButton > button:hover {
        background: #c8f564;
        color: #0d0d0d;
        border-color: #c8f564;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #1a1a1a;
        color: #e8e8e0;
        border: 1px solid #333;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #c8f564;
        box-shadow: 0 0 0 1px #c8f564;
    }

    .stSelectbox > div > div {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 6px;
        color: #e8e8e0;
    }

    .file-card {
        background: #141414;
        border: 1px solid #222;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.2rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #aaa;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .file-card:hover {
        border-color: #444;
        color: #e8e8e0;
    }

    .badge {
        background: #c8f564;
        color: #0d0d0d;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 0.15rem 0.5rem;
        border-radius: 3px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .badge-folder {
        background: #6496f5;
        color: #fff;
    }

    .section-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #555;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        border-bottom: 1px solid #222;
        padding-bottom: 0.4rem;
        margin-bottom: 0.8rem;
    }

    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
    }

    div[data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid #1e1e1e;
    }

    .stRadio > div {
        gap: 0.5rem;
    }

    .stRadio > div > label {
        background: #141414;
        border: 1px solid #222;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        transition: all 0.15s;
        cursor: pointer;
        color: #aaa;
    }

    .stRadio > div > label:hover {
        border-color: #c8f564;
        color: #e8e8e0;
    }

    .content-preview {
        background: #111;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #c8f564;
        white-space: pre-wrap;
        max-height: 300px;
        overflow-y: auto;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)


# ─── Helper Functions ────────────────────────────────────────────────────────
def get_all_items():
    p = Path('')
    return list(p.rglob('*'))

def get_icon(item: Path):
    return "📁" if item.is_dir() else "📄"


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="main-title">🗂️</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-title">File<br>Manager</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">v1.0 · Streamlit UI</p>', unsafe_allow_html=True)

    st.markdown("---")

    operation = st.radio(
        "Operation",
        options=[
            "📋  List Files",
            "✏️  Create File",
            "👁️  Read File",
            "🔄  Update File",
            "🗑️  Delete File",
            "✏️  Rename File",
            "📁  Create Folder",
            "🗑️  Delete Folder",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<p class="section-header">Working Directory</p>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.75rem;color:#666;">{Path.cwd()}</div>',
        unsafe_allow_html=True
    )


# ─── Main Panel ──────────────────────────────────────────────────────────────
col_main, col_tree = st.columns([3, 2], gap="large")

with col_main:
    op_name = operation.split("  ", 1)[1] if "  " in operation else operation
    st.markdown(f'<p class="section-header">/ {op_name}</p>', unsafe_allow_html=True)

    # ── LIST ──────────────────────────────────────────────────────────────────
    if "List Files" in operation:
        items = get_all_items()
        if not items:
            st.info("No files or folders found in the current directory.")
        else:
            for item in items:
                icon = get_icon(item)
                badge_cls = "badge-folder" if item.is_dir() else "badge"
                badge_txt = "DIR" if item.is_dir() else "FILE"
                st.markdown(
                    f'<div class="file-card">{icon} {item} '
                    f'<span class="{badge_cls} badge">{badge_txt}</span></div>',
                    unsafe_allow_html=True
                )

    # ── CREATE FILE ───────────────────────────────────────────────────────────
    elif "Create File" in operation:
        file_name = st.text_input("File name", placeholder="example.txt")
        content   = st.text_area("File content", placeholder="Type content here…", height=150)
        if st.button("Create File"):
            if not file_name:
                st.error("Please enter a file name.")
            else:
                p = Path(file_name)
                if p.exists():
                    st.warning("⚠️  File already exists.")
                else:
                    try:
                        p.write_text(content)
                        st.success(f"✅ File **{file_name}** created successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ── READ FILE ─────────────────────────────────────────────────────────────
    elif "Read File" in operation:
        items = [str(i) for i in get_all_items() if Path(i).is_file()]
        file_name = st.selectbox("Select a file to read", ["— select —"] + items)
        if st.button("Read File") or file_name != "— select —":
            if file_name == "— select —":
                st.info("Select a file from the dropdown.")
            else:
                p = Path(file_name)
                if p.exists():
                    try:
                        content = p.read_text()
                        st.markdown('<p class="section-header">File Contents</p>', unsafe_allow_html=True)
                        st.markdown(f'<div class="content-preview">{content}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error reading file: {e}")
                else:
                    st.error("File not found.")

    # ── UPDATE FILE ───────────────────────────────────────────────────────────
    elif "Update File" in operation:
        items = [str(i) for i in get_all_items() if Path(i).is_file()]
        file_name  = st.selectbox("Select a file to update", ["— select —"] + items)
        update_mode = st.radio("Mode", ["Overwrite", "Append"], horizontal=True)
        new_content = st.text_area("New content", height=150)

        if file_name != "— select —":
            try:
                existing = Path(file_name).read_text()
                st.markdown('<p class="section-header">Current Content</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="content-preview">{existing}</div>', unsafe_allow_html=True)
            except Exception:
                pass

        if st.button("Update File"):
            if file_name == "— select —":
                st.error("Please select a file.")
            else:
                p = Path(file_name)
                if p.exists():
                    try:
                        mode = 'w' if update_mode == "Overwrite" else 'a'
                        with open(file_name, mode) as f:
                            f.write(new_content)
                        st.success(f"✅ File **{file_name}** updated ({update_mode.lower()})!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("File not found.")

    # ── DELETE FILE ───────────────────────────────────────────────────────────
    elif "Delete File" in operation:
        items = [str(i) for i in get_all_items() if Path(i).is_file()]
        file_name = st.selectbox("Select a file to delete", ["— select —"] + items)
        st.warning("⚠️  This action is permanent and cannot be undone.")
        if st.button("🗑️  Delete File", type="primary"):
            if file_name == "— select —":
                st.error("Please select a file.")
            else:
                p = Path(file_name)
                if p.exists():
                    try:
                        os.remove(p)
                        st.success(f"✅ File **{file_name}** deleted.")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("File not found.")

    # ── RENAME FILE ───────────────────────────────────────────────────────────
    elif "Rename File" in operation:
        items = [str(i) for i in get_all_items() if Path(i).is_file()]
        file_name = st.selectbox("Select a file to rename", ["— select —"] + items)
        new_name  = st.text_input("New file name", placeholder="new_name.txt")
        if st.button("Rename File"):
            if file_name == "— select —" or not new_name:
                st.error("Please select a file and enter a new name.")
            else:
                p = Path(file_name)
                if p.exists():
                    try:
                        p.rename(new_name)
                        st.success(f"✅ Renamed **{file_name}** → **{new_name}**")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("File not found.")

    # ── CREATE FOLDER ─────────────────────────────────────────────────────────
    elif "Create Folder" in operation:
        folder_name = st.text_input("Folder name", placeholder="my_folder")
        if st.button("Create Folder"):
            if not folder_name:
                st.error("Please enter a folder name.")
            else:
                p = Path(folder_name)
                if p.exists():
                    st.warning("⚠️  Folder already exists.")
                else:
                    try:
                        p.mkdir(parents=True)
                        st.success(f"✅ Folder **{folder_name}** created!")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ── DELETE FOLDER ─────────────────────────────────────────────────────────
    elif "Delete Folder" in operation:
        items = [str(i) for i in get_all_items() if Path(i).is_dir()]
        folder_name = st.selectbox("Select a folder to delete", ["— select —"] + items)
        st.warning("⚠️  Folder must be empty to delete.")
        if st.button("🗑️  Delete Folder", type="primary"):
            if folder_name == "— select —":
                st.error("Please select a folder.")
            else:
                p = Path(folder_name)
                if p.exists():
                    try:
                        p.rmdir()
                        st.success(f"✅ Folder **{folder_name}** deleted.")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("Folder not found.")


# ─── File Tree Panel ──────────────────────────────────────────────────────────
with col_tree:
    st.markdown('<p class="section-header">/ File Tree</p>', unsafe_allow_html=True)
    if st.button("🔁  Refresh"):
        st.rerun()

    items = get_all_items()
    if not items:
        st.markdown('<div class="file-card">No items found</div>', unsafe_allow_html=True)
    else:
        for item in items:
            icon = get_icon(item)
            st.markdown(
                f'<div class="file-card" style="font-size:0.72rem">{icon} {item}</div>',
                unsafe_allow_html=True
            )