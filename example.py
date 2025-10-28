import hashlib
import datetime
from zeep import Client

# === CONFIGURAÇÕES DO SISTEMA ===
CNPJ = "PGM-Sete Lagoas"
SENHA = 'C^yr3#F12"zs' 
DATA_FORMATO = "%d-%m-%Y"
URL_WSDL = "https://eproc1g-ws.tjmg.jus.br/eproc/wsdl.php?srv=intercomunicacao2.2"
#URL_WSDL = "https://eproc1g-hml.tjmg.jus.br/eproc/wsdl.php?srv=intercomunicacao2.2"
# === GERA O HASH DIÁRIO ===
def gerar_hash_diario(senha, data=None):
    if data is None:
        data = datetime.datetime.now().strftime(DATA_FORMATO)
    string_inicial = f"{data}{senha}"
    print(string_inicial)
    retorno = hashlib.sha256(string_inicial.encode("utf-8")).hexdigest()
    print(retorno)
    return retorno

hash_diario = gerar_hash_diario(SENHA)

# === CLIENTE SOAP ===
client = Client(URL_WSDL)

# === DADOS DA CONSULTA ===
numero_processo = "10001325320258130672"

params = {
    "idConsultante": CNPJ,
    "senhaConsultante": hash_diario,
    "numeroProcesso": numero_processo,
    "incluirCabecalho": True,
    "movimentos": True,
    "incluirDocumentos": False
}

# === CHAMADA AO SERVIÇO ===
try:
    resposta = client.service.consultarProcesso(**params)
    print("✅ Sucesso:", resposta.sucesso)
    print("📄 Mensagem:", resposta.mensagem)

    if resposta.sucesso:
        processo = resposta.processo
        print("\n📘 Número:", processo.dadosBasicos.numero)
        print("⚖️ Classe:", processo.dadosBasicos.classeProcessual)
        print("🏛️ Órgão Julgador:", processo.dadosBasicos.orgaoJulgador.nomeOrgao)
        print("👥 Partes:")
        for polo in processo.dadosBasicos.polo:
            print(" -", polo.polo, [p.pessoa.nome for p in polo.parte])
        print("\n📜 Movimentos:")
        for m in processo.movimento:
            print(f" - {m.dataHora}: {m.movimentoLocal.descricao}")
    else:
        print("❌ Erro:", resposta.mensagem)

except Exception as e:
    print("Erro ao consultar processo:", e)
