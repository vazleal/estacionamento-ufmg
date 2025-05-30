import React, { useState } from "react";
import "../App.css";

const LoginPage: React.FC = () => {
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
            <div className="card">
                <div className="login-container">
                    <h2>{isRegister ? "Cadastro" : "Login"}</h2>
                    <form onSubmit={handleSubmit} className="login-form">
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
                        <button type="submit" className="button">
                            {isRegister ? "Cadastrar" : "Entrar"}
                        </button>
                    </form>
                    <p>
                        {isRegister ? "Já tem uma conta?" : "Não tem uma conta?"}{" "}
                        <button
                            className="link-button"
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