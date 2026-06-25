"""Reusable UI components."""
from __future__ import annotations

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

from core.theme import render_kpi_card


def election_selector(key: str = "election_select") -> int | None:
    from services.realtime import get_elections

    elections = get_elections()
    if elections.empty:
        st.warning("No elections found. Import election data or run seed script.")
        return None

    options = {
        f"{row['name']} ({row['status']})": row["id"]
        for _, row in elections.iterrows()
    }
    selected = st.selectbox("Select Election", list(options.keys()), key=key)
    election_id = options[selected]
    st.session_state.selected_election_id = election_id
    return election_id


def kpi_row(kpis: dict) -> None:
    cols = st.columns(4)
    items = [
        ("Total Votes Counted", f"{kpis['total_votes']:,}", "🗳️"),
        ("Constituencies Declared", f"{kpis['declared']}/{kpis['total_constituencies']}", "✅"),
        ("Leading Party", str(kpis["leading_party"]), "🏛️"),
        ("Voter Turnout", f"{kpis['turnout_pct']}%", "📊"),
    ]
    for col, (label, value, icon) in zip(cols, items):
        with col:
            render_kpi_card(label, value, icon=icon)

    cols2 = st.columns(4)
    items2 = [
        ("Pending Constituencies", str(kpis["pending"]), "⏳"),
        ("Winning Party", str(kpis["winning_party"]), "🏆"),
        ("Total Candidates", str(kpis["total_candidates"]), "👥"),
        ("Counting Progress", f"{kpis['counting_progress']}%", "📈"),
    ]
    for col, (label, value, icon) in zip(cols2, items2):
        with col:
            render_kpi_card(label, value, icon=icon)


def live_results_grid(df, height: int = 450):
    if df.empty:
        st.info("No results data available.")
        return

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
    gb.configure_default_column(filterable=True, sortable=True, resizable=True)
    gb.configure_selection("single")
    grid = AgGrid(
        df,
        gridOptions=gb.build(),
        update_mode=GridUpdateMode.NO_UPDATE,
        height=height,
        theme="streamlit",
        allow_unsafe_jscode=True,
    )
    return grid


def insight_cards(insights: list[dict]) -> None:
    st.markdown('<div class="section-title">🤖 AI Insights</div>', unsafe_allow_html=True)
    for ins in insights:
        st.markdown(
            f'<div class="insight-card">{ins["icon"]} {ins["text"]}</div>',
            unsafe_allow_html=True,
        )


def search_filter_bar(df, search_cols: list[str]):
    search = st.text_input("🔍 Search", placeholder="Search by candidate, party, constituency...")
    status_filter = st.multiselect("Status", ["declared", "pending", "counting"], default=[])

    filtered = df.copy()
    if search:
        mask = False
        for col in search_cols:
            if col in filtered.columns:
                mask = mask | filtered[col].astype(str).str.contains(search, case=False, na=False)
        filtered = filtered[mask]
    if status_filter:
        filtered = filtered[filtered["status"].isin(status_filter)]
    return filtered
