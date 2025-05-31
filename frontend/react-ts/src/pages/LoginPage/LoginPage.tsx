import React, { useState } from "react";
import "../../App.css";

export const LoginPage: React.FC = () => {
    const [isRegister, setIsRegister] = useState(false);
    const [form, setForm] = useState({ email: "", password: "", confirm: "" });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (isRegister) {
            if (form.password !== form.confirm) {
                alert("As senhas não coincidem!");
                return;
            }
            // Lógica de cadastro aqui
            alert("Cadastro realizado!");
        } else {
            // Lógica de login aqui
            alert("Login realizado!");
        }
    };

    return (
        <main className="main-content">
            <div className="login-card">
                <form onSubmit={handleSubmit} className="login-container">
                    <span className="login-title">{isRegister ? "Cadastro" : "Login"}</span>
                    <input
                        type="email"
                        name="email"
                        placeholder="E-mail"
                        value={form.email}
                        onChange={handleChange}
                        required
                        className="input"
                    />
                    <input
                        type="password"
                        name="password"
                        placeholder="Senha"
                        value={form.password}
                        onChange={handleChange}
                        required
                        className="input"
                    />
                    {isRegister && (
                        <input
                            type="password"
                            name="confirm"
                            placeholder="Confirme a senha"
                            value={form.confirm}
                            onChange={handleChange}
                            required
                            className="input"
                        />
                    )}
                    <div>
                        <button type="submit" className="login-btn">
                            {isRegister ? "Cadastrar" : "Entrar"}
                        </button>
                    </div>
                </form>
                <div>
                    <p>
                        <div>
                            {isRegister ? "Já tem uma conta?" : "Não tem uma conta?"}{" "}
                        </div>
                        <button
                            className="login-btn"
                            onClick={() => setIsRegister(!isRegister)}
                            type="button"
                        >
                            {isRegister ? "Entrar" : "Cadastrar"}
                        </button>
                    </p>
                </div>
            </div>
        </main>
    );
};

export default LoginPage;