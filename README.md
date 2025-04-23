🅿️ Sistema de Gerenciamento de Vagas – Versão Porteiro
🎯 Objetivo
Permitir que a portaria registre entradas de veículos de professores e alunos com base na carteirinha apresentada. O sistema controla ocupação e emite alertas de escassez de vagas reservadas para professores, podendo bloquear a entrada de alunos automaticamente.

🧩 Funcionalidades Principais
✅ 1. Registro de Entrada de Veículo
Interface simples com dois botões:
+ Professor | + Aluno

Ao clicar, o sistema registra a entrada com:

Timestamp

Tipo de motorista (professor ou aluno)

Dia da semana

✅ 2. Registro de Saída (opcional)
Interface com botão – Professor | – Aluno

Pode ser usado para simular a saída de veículos e liberar vaga

✅ 3. Painel de Vagas em Tempo Real
Exibe:

Vagas totais do estacionamento

Vagas ocupadas (total e por tipo)

Vagas reservadas para professores (ex: 40)

Quantas dessas ainda estão disponíveis

Quantas vagas restantes no total

✅ 4. Alerta de Escassez para Professores
Se vagas reservadas para professores < 10% disponíveis:

Sistema exibe ALERTA VISUAL

Opcional: aumenta a reserva automaticamente (ex: +5) se houver vagas disponíveis

Se não houver vagas gerais livres, bloqueia botão + Aluno

✅ 5. Relatório Histórico (por dia da semana)
Tabela simples com:

Quantos professores e alunos entraram por dia

Média por dia da semana

Base para ajustar reservas

💡 Regras de Negócio
Vagas totais = 100 (por exemplo)

Vagas reservadas para professores = 40 (configurável)

Se ocupação de vagas reservadas for ≥ 90%:

Mostrar aviso: "⚠️ Apenas X vagas reservadas restantes para professores"

Se ainda houver vagas gerais, opcionalmente mover algumas para professores

Se total de vagas lotadas:

Bloquear botão + Aluno
