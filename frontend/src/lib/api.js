// src/lib/api.js

export async function getProfile() {
    const res = await fetch("http://localhost:5000/auth/profile", {
        credentials: "include"
    });
    if (res.ok) return await res.json();
    return null;
}

export function login() {
    window.location.href = "http://localhost:5000/auth/login";
}

export async function logout() {
    const res = await fetch("http://localhost:5000/auth/logout", {
        credentials: "include"
    });
    return res.ok;
}


export async function readTokenFromCookie() {
    const res = await fetch("http://localhost:5000/auth/token", {
        credentials: "include"
    });
    if (res.ok) {
        const data = await res.json();
        // localStorage.setItem("access_token", data.access_token);
        return data.access_token;
    }
}
