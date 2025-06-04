import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../../App.css";
import "./LoginPage.css";

export const LoginPage: React.FC = () => {
    const [isRegister, setIsRegister] = useState(false);
    const [form, setForm] = useState({
        nome: "",
        email: "",
        senha: "",
        confirma: "",
        matricula: "",
        tipo: "aluno"
    });

    const navigate = useNavigate();

    React.useEffect(() => {
        const id = localStorage.getItem("usuario_id");
        const tipo = localStorage.getItem("usuario_tipo");
        if (id) {
            if (tipo === "admin") {
                navigate("/", { replace: true });
            } else {
                navigate("/painel", { replace: true });
            }
        }
    }, [navigate]);

    if (localStorage.getItem("usuario_id")) {
        return null; 
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (isRegister) {
            if (form.senha !== form.confirma) {
                alert("As senhas não coincidem!");
                return;
            }
            
            try {
                const res = await axios.post("http://localhost:8000/register", {
                    nome: form.nome,
                    email: form.email,
                    senha: form.senha,
                    matricula: form.matricula,
                    tipo: form.tipo
                });
                if(res.status == 200) {
                    alert("Cadastro realizado com sucesso!");
                    setIsRegister(false);
                    navigate("/login");  // Redireciona para Login
                } else {
                    alert(res.data.detail || "Erro no cadastro.");
                }
            } catch (error: any) {
                alert(error.response?.data?.detail || "Erro no cadastro.");
            }
        } else {
            try {
                const res = await axios.post("http://localhost:8000/login", {
                    email: form.email,
                    senha: form.senha
                });
                alert("Login realizado com sucesso!");
                localStorage.setItem("usuario_id", res.data.id);
                localStorage.setItem("usuario_nome", res.data.nome);
                localStorage.setItem("usuario_tipo", res.data.tipo);
                if (res.data.tipo === "admin") {
                    navigate("/");
                } else {
                    navigate("/painel");
                }
            } catch (error: any) {
                alert(error.response?.data?.detail || "Erro no login.");
            }
        }
    };

    return (
        <main className="main-content">
            <div className="login-card">
                <form onSubmit={handleSubmit} className="login-container">
                    <span className="login-title">
                        {isRegister ? "Cadastro" : "Login"}
                    </span>
                    {isRegister && (
                        <input
                            type="text"
                            name="nome"
                            placeholder="Nome Completo"
                            value={form.nome}
                            onChange={handleChange}
                            required
                            className="input"
                        />
                    )}
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
                        name="senha"
                        placeholder="Senha"
                        value={form.senha}
                        onChange={handleChange}
                        required
                        className="input"
                    />

                    {isRegister && (
                        <>
                            <input
                                type="password"
                                name="confirma"
                                placeholder="Confirme a senha"
                                value={form.confirma}
                                onChange={handleChange}
                                required
                                className="input"
                            />

                            <input
                                type="text"
                                name="matricula"
                                placeholder="Matrícula"
                                value={form.matricula}
                                onChange={handleChange}
                                required
                                className="input"
                            />
                            <select
                                name="tipo"
                                value={form.tipo}
                                onChange={handleChange}
                                className="input"
                            >
                                <option value="aluno">Aluno</option>
                                <option value="professor">Professor</option>
                            </select>
                        </>
                    )}

                    <div>
                        <button type="submit" className="login-btn">
                            {isRegister ? "Cadastrar" : "Entrar"}
                        </button>
                    </div>
                </form>

                <div>
                    <p>
                        {isRegister ? "Já tem uma conta?" : "Não tem uma conta?"}
                    </p>
                    <button
                        className="login-btn"
                        onClick={() => setIsRegister(!isRegister)}
                        type="button"
                    >
                        {isRegister ? "Entrar" : "Cadastrar"}
                    </button>
                </div>
            </div>
        </main>
    );
};

export default LoginPage;
