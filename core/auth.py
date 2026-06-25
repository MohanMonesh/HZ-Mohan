"""Authentication and role-based access control."""
from __future__ import annotations

import bcrypt
import streamlit as st

from core.database import execute, get_connection, init_db, query_df

DEFAULT_USERS = [
    ("admin", "Admin@2024", "System Administrator", "super_admin"),
    ("officer", "Officer@2024", "Election Officer", "election_officer"),
    ("analyst", "Analyst@2024", "Data Analyst", "analyst"),
    ("public", "Public@2024", "Public Viewer", "public"),
]


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes | str) -> bool:
    if isinstance(hashed, str):
        hashed = hashed.encode()
    return bcrypt.checkpw(password.encode(), hashed)


def seed_users() -> None:
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count > 0:
            return
        for username, password, full_name, role in DEFAULT_USERS:
            conn.execute(
                "INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                (username, hash_password(password).decode(), full_name, role),
            )


def authenticate(username: str, password: str) -> dict | None:
    df = query_df(
        "SELECT id, username, password_hash, full_name, role FROM users WHERE username = ? AND is_active = 1",
        (username,),
    )
    if df.empty:
        return None
    row = df.iloc[0]
    if verify_password(password, row["password_hash"]):
        return {
            "id": row["id"],
            "username": row["username"],
            "full_name": row["full_name"],
            "role": row["role"],
        }
    return None


def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    if "selected_election_id" not in st.session_state:
        st.session_state.selected_election_id = None
    if "alerts" not in st.session_state:
        st.session_state.alerts = []


def login(user: dict) -> None:
    st.session_state.authenticated = True
    st.session_state.user = user


def logout() -> None:
    st.session_state.authenticated = False
    st.session_state.user = None


def require_roles(*roles: str) -> bool:
    if not st.session_state.get("authenticated"):
        return False
    return st.session_state.user["role"] in roles or st.session_state.user["role"] == "super_admin"


ROLE_PERMISSIONS = {
    "super_admin": {"manage_elections", "publish", "manage_users", "upload", "verify", "analytics", "public_view"},
    "election_officer": {"upload", "verify", "publish", "analytics", "public_view"},
    "analyst": {"analytics", "public_view"},
    "public": {"public_view"},
}


def has_permission(permission: str) -> bool:
    if not st.session_state.get("authenticated"):
        return permission == "public_view"
    role = st.session_state.user["role"]
    return permission in ROLE_PERMISSIONS.get(role, set())


def setup_auth() -> None:
    init_db()
    seed_users()
    init_session()
