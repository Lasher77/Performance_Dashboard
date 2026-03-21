import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuthStore } from "../store/auth";

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user);
  const setUser = useAuthStore((s) => s.setUser);
  const logout = useAuthStore((s) => s.logout);
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      api.auth.me().then(setUser).catch(() => {
        logout();
        navigate("/login");
      });
    }
  }, [user, setUser, logout, navigate]);

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", padding: 20 }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 32 }}>
        <h1>SteuerPilot</h1>
        <button onClick={handleLogout} style={{ padding: "8px 16px" }}>
          Abmelden
        </button>
      </header>
      <main>
        {user ? (
          <div>
            <h2>Willkommen, {user.first_name} {user.last_name}!</h2>
            <p>Rolle: {user.role}</p>
            <p style={{ marginTop: 24, color: "#666" }}>
              Das Dashboard wird in den nächsten Schritten ausgebaut.
            </p>
          </div>
        ) : (
          <p>Laden...</p>
        )}
      </main>
    </div>
  );
}
