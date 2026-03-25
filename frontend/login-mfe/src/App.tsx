import "regenerator-runtime/runtime";
import React, { useState } from "react";

const LOGIN_URL = "http://localhost:8001/users/login";
const TOKEN_KEY = "ecotech_token";

export default function Root() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const body = new URLSearchParams();
      body.append("username", email);
      body.append("password", password);

      const response = await fetch(LOGIN_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          accept: "application/json",
        },
        body: body.toString(),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Não foi possível fazer login.");
      }

      localStorage.setItem(TOKEN_KEY, data.access_token);
      window.location.href = "http://localhost:9000/orders";
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro inesperado ao fazer login.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#f5f5f5",
        padding: "24px",
        boxSizing: "border-box",
      }}
    >
      <section
        style={{
          width: "100%",
          maxWidth: "420px",
          backgroundColor: "#ffffff",
          borderRadius: "12px",
          padding: "32px",
          boxShadow: "0 8px 24px rgba(0, 0, 0, 0.08)",
          boxSizing: "border-box",
        }}
      >
        <h1 style={{ marginTop: 0, marginBottom: "8px" }}>Login Ecotech</h1>
        <p style={{ marginTop: 0, marginBottom: "24px", color: "#555" }}>
          Entre com seu e-mail e senha para acessar o painel de pedidos.
        </p>

        <form onSubmit={handleSubmit}>
          <div style={{ display: "flex", flexDirection: "column", gap: "8px", marginBottom: "16px" }}>
            <label htmlFor="email">E-mail</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="voce@empresa.com"
              required
              style={{
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid #ccc",
                fontSize: "16px",
              }}
            />
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "8px", marginBottom: "16px" }}>
            <label htmlFor="password">Senha</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Digite sua senha"
              required
              style={{
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid #ccc",
                fontSize: "16px",
              }}
            />
          </div>

          {error ? (
            <p
              style={{
                color: "#b00020",
                backgroundColor: "#fdecea",
                borderRadius: "8px",
                padding: "12px",
                marginBottom: "16px",
              }}
            >
              {error}
            </p>
          ) : null}

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "12px",
              border: "none",
              borderRadius: "8px",
              fontSize: "16px",
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>
      </section>
    </main>
  );
}
