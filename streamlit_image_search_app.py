#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import streamlit as st
from PIL import Image

from image_prompt_search import search

st.set_page_config(page_title="Prompt Image Search", layout="wide")
st.title("Prompt Image Search")
st.caption("Search your local indexed images with natural language prompts.")

index_dir = st.text_input("Index directory", value="./.image_search_index")
query = st.text_input("Search prompt", value="blue and white shoes")
top_k = st.slider("Results", min_value=5, max_value=100, value=30, step=5)

if st.button("Search"):
    idx = Path(index_dir).expanduser().resolve()
    if not idx.exists():
        st.error("Index directory not found. Build an index first with image_prompt_search.py.")
    elif not query.strip():
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Searching..."):
            try:
                results = search(idx, query=query.strip(), top_k=top_k)
            except Exception as exc:
                st.exception(exc)
                st.stop()

        st.success(f"Found {len(results)} results")
        cols = st.columns(3)
        for i, item in enumerate(results):
            col = cols[i % 3]
            with col:
                path = Path(item["path"])
                st.write(f"**Score:** {item['score']:.3f}")
                st.caption(str(path))
                if path.exists():
                    try:
                        img = Image.open(path)
                        st.image(img, use_container_width=True)
                    except Exception:
                        st.warning("Preview unavailable")
                else:
                    st.warning("File not found")
