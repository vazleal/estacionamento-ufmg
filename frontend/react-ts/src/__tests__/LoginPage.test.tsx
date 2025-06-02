import { render, screen, fireEvent } from "@testing-library/react";
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import LoginPage from "../pages/LoginPage/LoginPage";
import { MemoryRouter } from "react-router-dom";

describe("LoginPage", () => {
  it("renders login form by default", () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Login/i)).toBeInTheDocument();
  });

  it("switches to cadastro form", () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );

    const switchButton = screen.getByText(/Cadastrar/i);
    fireEvent.click(switchButton);

    expect(screen.getByText(/Cadastro/i)).toBeInTheDocument();
  });


  it("alerts when passwords do not match", async () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );

    const spy = vi.spyOn(window, 'alert').mockImplementation(() => {});

    const switchButton = screen.getByText(/Cadastrar/i);
    fireEvent.click(switchButton);

    const nameInput = screen.getByPlaceholderText('Nome Completo');
    const emailInput = screen.getByPlaceholderText('E-mail');
    const passwordInput = screen.getByPlaceholderText('Senha');
    const confirmPasswordInput = screen.getByPlaceholderText('Confirme a senha');
    const matriculaInput = screen.getByPlaceholderText('Matrícula');
    const submitButton = screen.getByRole("button", { name: /Cadastrar/i });

    fireEvent.change(nameInput, { target: { value: 'abc' } });
    fireEvent.change(emailInput, { target: { value: 'abc@gmail.com' } });
    fireEvent.change(passwordInput, { target: { value: '123456' } });
    fireEvent.change(confirmPasswordInput, { target: { value: '654321' } });
    fireEvent.change(matriculaInput, { target: { value: '123' } });
    fireEvent.click(submitButton);

    expect(spy).toHaveBeenCalledWith("As senhas não coincidem!");
  });
});

