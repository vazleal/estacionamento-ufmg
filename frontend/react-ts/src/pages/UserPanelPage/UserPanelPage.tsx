import React from "react";
import "../../App.css";
import "./UserPanelPage.css";

export const UserPanelPage: React.FC = () => {
    const handleLogout = () => {
        localStorage.removeItem("token");
        window.location.href = "/login";
    };

    return (
        <main className="main-content">
            <div className="login-card">
                <h2>Painel do Usuário</h2>
                <p>Bem-vindo ao seu painel!</p>
                <button className="login-btn" onClick={handleLogout}>
                    Logout
                </button>
            </div>
        </main>
    );
};

export default UserPanelPage;
