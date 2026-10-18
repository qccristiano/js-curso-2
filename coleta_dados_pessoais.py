"""Coleta de dados pessoais via terminal, com validação básica dos campos."""

import json
import re
from datetime import date, datetime

REGEX_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
REDES_SUGERIDAS = ["Instagram", "LinkedIn", "Facebook", "X/Twitter", "GitHub", "TikTok"]


def _perguntar(mensagem, obrigatorio=True, validar=None, erro="Valor inválido."):
    """Lê um valor do usuário, repetindo a pergunta até ser válido."""
    while True:
        valor = input(mensagem).strip()
        if not valor:
            if obrigatorio:
                print("  Este campo é obrigatório.")
                continue
            return None
        if validar and not validar(valor):
            print(f"  {erro}")
            continue
        return valor


def _data_valida(texto):
    try:
        nascimento = datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        return False
    return nascimento <= date.today()


def _telefone_valido(texto):
    digitos = re.sub(r"\D", "", texto)
    return 10 <= len(digitos) <= 13


def _calcular_idade(nascimento):
    hoje = date.today()
    return hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))


def coletar_dados_pessoais():
    """Pergunta os dados pessoais ao usuário e devolve um dicionário com eles."""
    print("=== Cadastro de dados pessoais ===")

    nome = _perguntar("Nome completo: ", validar=lambda v: len(v.split()) >= 2,
                      erro="Informe nome e sobrenome.")
    nascimento_txt = _perguntar("Data de nascimento (dd/mm/aaaa): ", validar=_data_valida,
                                erro="Data inválida. Use o formato dd/mm/aaaa.")
    nascimento = datetime.strptime(nascimento_txt, "%d/%m/%Y").date()
    profissao = _perguntar("Profissão: ")
    email = _perguntar("E-mail: ", validar=lambda v: REGEX_EMAIL.match(v) is not None,
                       erro="E-mail inválido.")
    telefone = _perguntar("Telefone (opcional): ", obrigatorio=False, validar=_telefone_valido,
                          erro="Telefone inválido. Inclua o DDD.")
    cidade = _perguntar("Cidade/Estado (opcional): ", obrigatorio=False)

    print("\nRedes sociais (deixe em branco para pular):")
    redes = {}
    for rede in REDES_SUGERIDAS:
        perfil = _perguntar(f"  {rede}: ", obrigatorio=False)
        if perfil:
            redes[rede] = perfil
    while True:
        outra = _perguntar("  Outra rede (nome) ou Enter para terminar: ", obrigatorio=False)
        if not outra:
            break
        perfil = _perguntar(f"  Perfil no {outra}: ")
        redes[outra] = perfil

    return {
        "nome": nome.title(),
        "data_nascimento": nascimento.isoformat(),
        "idade": _calcular_idade(nascimento),
        "profissao": profissao,
        "email": email.lower(),
        "telefone": telefone,
        "cidade": cidade,
        "redes_sociais": redes,
    }


def salvar_dados(dados, arquivo="dados_pessoais.json"):
    """Salva os dados em um arquivo JSON."""
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    dados = coletar_dados_pessoais()
    print("\n=== Dados coletados ===")
    print(json.dumps(dados, ensure_ascii=False, indent=2))
    if input("\nSalvar em dados_pessoais.json? (s/n): ").strip().lower() == "s":
        salvar_dados(dados)
        print("Dados salvos.")
