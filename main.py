from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate
from reportlab.pdfgen import canvas

import mysql.connector
import sqlalchemy as db
import sys

from datetime import datetime

# DEFININDO AS VARIÁVEIS PARA REQUISIÇÃO DE CONEXÃO
def ConectaBD():
    con = mysql.connector.connect(host='localhost', 
                                port='3306', 
                                database='Imuniza', 
                                user='root', 
                                password='')

    # CASO A CONEXÃO COM O BANCO TENHA SIDO FEITA COM SUCESSO, UMA JANELA DE CONFIRMAÇÃO É EXIBIDA
    if(con.is_connected()):
        db_info = con.get_server_info()
        msg = QtWidgets.QMessageBox(); msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Banco de dados conectado!"); msg.setWindowTitle("Banco de Dados")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok); msg.exec_()
    return con

# FUNÇÃO QUE PERMITE O CADASTRO DE UMA PESSOA NO BANCO DE DADOS
def CadastroPessoa():
    banco = ConectaBD(); cursor = banco.cursor() # CRIA A INSTÂNCIA DE CONEXÃO COM O BANCO
    # ATRIBUI AS VARIÁVEIS OS VALORES PRESENTES NAS CAIXAS DE TEXTO DA TELA DE CADASTRO
    nome = formCadastroPessoa.campoNome.text(); mae = formCadastroPessoa.campoMae.text(); sus = formCadastroPessoa.campoSUS.text()
    sexo = formCadastroPessoa.campoSexo.text(); cpf = formCadastroPessoa.campoCPF.text(); alergias = formCadastroPessoa.campoAlergia.text()
    rua = formCadastroPessoa.campoRua.text(); numero = formCadastroPessoa.campoNumero.text(); municipio = formCadastroPessoa.campoMunicipio.text()
    estado = formCadastroPessoa.campoEstado.text(); cep = formCadastroPessoa.campoCEP.text(); nascimento = QDate.getDate(formCadastroPessoa.campoNascimento.selectedDate()); 
    data = datetime(nascimento[0]  , nascimento[1], nascimento[2])

    idEstadoCivil = cursor.execute("SELECT idEstadoCivil FROM Estado_Civil"); idEstadoCivilLido = cursor.fetchall(); idEstadoCivil = int(idEstadoCivilLido[0][0])
    idReligiao = cursor.execute("SELECT idReligiao FROM Religiao"); idReligiaoLido = cursor.fetchall(); idReligiao = int(idReligiaoLido[0][0])
    idEscolaridade = cursor.execute("SELECT idEscolaridade FROM Escolaridade"); idEscolaLido = cursor.fetchall(); idEscolaridade = int(idEscolaLido[0][0])
    idPlano = cursor.execute("SELECT idPlano FROM Plano_Saude"); idPlanoLido = cursor.fetchall(); idPlano = int(idPlanoLido[0][0])
    idSensiveis = cursor.execute("SELECT idSensiveis FROM Sensiveis"); idSensiveisLido = cursor.fetchall(); idSensiveis = int(idSensiveisLido[0][0])

    # CRIANDO O COMANDO PARA A INSERÇÃO DOS DADOS COLETADOS NO BANCO
    insere_banco = "INSERT INTO Pessoa(nome, nascimento, nome_mae, cadastro_sus, sexo_genetico, cpf, alergias, idEstadoCivil, idEscolaridade, idPlanoSaude, idReligiao, idSensiveis, rua, numeroRua, municipio, estado, cep) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    dados = (nome, data, mae, sus, sexo, cpf, alergias, idEstadoCivil, idEscolaridade, idPlano, idReligiao, idSensiveis, rua, numero, municipio, estado, cep)
    cursor.execute(insere_banco, dados) # EXECUTANDO O COMANDO 
    banco.commit() # SALVANDO AS ALTERAÇÕES

    # LIMPANDO OS DADOS DA TELA
    formCadastroPessoa.campoNome.setText(''); formCadastroPessoa.campoMae.setText(''); formCadastroPessoa.campoSUS.setText(''); formCadastroPessoa.campoSexo.setText(''); formCadastroPessoa.campoCPF.setText(''); formCadastroPessoa.campoAlergia.setText('')
    formCadastroPessoa.campoRua.setText(''); formCadastroPessoa.campoNumero.setText(''); formCadastroPessoa.campoMunicipio.setText(''); formCadastroPessoa.campoEstado.setText(''); formCadastroPessoa.campoCEP.setText('')

# FUNÇÃO QUE PERMITE O CADASTRO DE UMA VACINA NO BANCO DE DADOS
def CadastrarVacina():
    banco = ConectaBD(); cursor = banco.cursor() # CRIA A INSTÂNCIA DE CONEXÃO COM O BANCO
    # ATRIBUI AS VARIÁVEIS OS VALORES PRESENTES NAS CAIXAS DE TEXTO DA TELA DE CADASTRO
    codigo = formCadastroVacina.campoCodigo.text(); lote = formCadastroVacina.campoLote.text(); doses = formCadastroVacina.campoDoses.text(); efeitos = formCadastroVacina.campoEfeitos.text(); armazenar = formCadastroVacina.campoArmazenar.text();
    doenca = formCadastroVacina.campoDoenca.text(); via = formCadastroVacina.campoVia.text(); data = QDate.getDate(formCadastroVacina.campoData.selectedDate()); vencimento = datetime(data[0]  , data[1], data[2]);
    # doenca = str(doenca);
    idDoenca = cursor.execute("SELECT * FROM Doenca WHERE codigoDoenca = " + doenca); idDoencaLido = cursor.fetchall(); #idDoenca = str(idDoencaLido)
    print(idDoencaLido)
    insere_banco_vacina = "INSERT INTO Vacina(codVacina, lote, doses, dataFabricacao, efeitosColaterais, infoArmazenagem, viaAdministracao, idDoenca) VALUES (%s, %s, %s, %s, %s, %s,%s, %s)"
    dados_vacina = (codigo, lote, doses, vencimento, efeitos, armazenar, via, idDoenca)
    cursor.execute(insere_banco_vacina, dados_vacina) # EXECUTANDO O COMANDO 
    banco.commit() # SALVANDO AS ALTERAÇÕES

    # LIMPANDO OS DADOS DA TELA
    formCadastroVacina.campoCodigo.setText(''); formCadastroVacina.campoLote.setText(''); formCadastroVacina.campoDoses.setText(''); formCadastroVacina.campoEfeitos.setText(''); 
    formCadastroVacina.campoArmazenar.setText(''); formCadastroVacina.campoVia.setText(''); formCadastroVacina.campoDoenca.setText('');

def Vacinacao():
    banco = ConectaBD(); cursor = banco.cursor() # CRIA A INSTÂNCIA DE CONEXÃO COM O BANCO
    # ATRIBUI AS VARIÁVEIS OS VALORES PRESENTES NAS CAIXAS DE TEXTO DA TELA DE CADASTRO
    sus = formPessoaVacina.campoCadSUS.text(); sus = str(sus) # CAMPO DE ENTRADA PARA A CHAVE A SER PESQUISADA NO BANCO
    idPessoa = cursor.execute("SELECT idPessoa FROM Pessoa WHERE cadastro_sus = " + sus); idPessoa = cursor.fetchall(); idPessoa = str(idPessoa[0][0]) # EXECUTANDO O COMANDO E RETORNANDO O VALOR
    
    cod = formPessoaVacina.campoCodVacina.text(); cod = str(cod);
    idVacina = cursor.execute("SELECT idVacina FROM Vacina WHERE codVacina = " + cod); idVacina = cursor.fetchall(); idVacina = str(idVacina[0][0]) # EXECUTANDO O COMANDO E RETORNANDO O VALOR
 
    cadSUS = formPessoaVacina.campoCadSUS.text(); dose = formPessoaVacina.campoDose.text(); dataDose = QDate.getDate(formPessoaVacina.campoDataDose.selectedDate()); data_dose = datetime(dataDose[0], dataDose[1], dataDose[2]);

    insere_pessoa_vacina = "INSERT INTO Pessoa_Vacina(idVacina, idPessoa, dose, dataDose) VALUES (%s, %s, %s, %s)"
    dados_pessoa_vacina = (int(idVacina), int(idPessoa), dose, data_dose)
    cursor.execute(insere_pessoa_vacina, dados_pessoa_vacina) # EXECUTANDO O COMANDO 
    banco.commit() # SALVANDO AS ALTERAÇÕES
    
    # LIMPANDO OS DADOS DA TELA
    formPessoaVacina.campoCodVacina.setText(''); formPessoaVacina.campoDose.setText(''); formPessoaVacina.campoCadSUS.setText(''); 

# FUNÇÃO QUE PERMITE GERAR UM PDF DOS DADOS CONSULTADOS  DE PESSOA
def GeraPDF():
    banco = ConectaBD(); cursor = banco.cursor() # CRIA A INSTÂNCIA DE CONEXÃO COM O BANCO
    result = cursor.execute("SELECT * FROM Pessoa"); result = cursor.fetchall() # REALIZA A CONSULTA NO BANCO

    # MOLDANDO O DOCUMENTO PDF
    pdf = canvas.Canvas("PDF/cadastros_pessoas.pdf")
    pdf.drawString(10, 850, "ID"); pdf.drawString(10, 820, "NOME"); pdf.drawString(10, 790, "NASCIMENTO"); pdf.drawString(10, 760, "MAE"); pdf.drawString(10, 730, "SUS"); pdf.drawString(10, 700, "SEXO"); pdf.drawString(10, 670, "CPF"); pdf.drawString(10, 640, "ALERGIAS"); 
    pdf.drawString(10, 610, "ESTADO CIVIL"); pdf.drawString(10, 580, "ESCOLARIDADE"); pdf.drawString(10, 550, "PLANO DE SAUDE"); pdf.drawString(10, 520, "RELIGIAO"); pdf.drawString(10, 490, "SENSIVEIS"); pdf.drawString(10, 460, "RUA"); pdf.drawString(10, 430, "NUMERO"); 
    pdf.drawString(10, 400, "MUNICIPIO"); pdf.drawString(10, 370, "ESTADO"); pdf.drawString(10, 340, "CEP");

    # ESCREVENDO OS VALORES NO PDF
    for i in range(0, len(result)):
        pdf.drawString(155, 850, str(result[i][0])); pdf.drawString(155, 820, str(result[i][1])); pdf.drawString(155, 790, str(result[i][2])); pdf.drawString(155, 760, str(result[i][3])); pdf.drawString(155, 730, str(result[i][4])); pdf.drawString(155, 700, str(result[i][5])); 
        pdf.drawString(155, 670, str(result[i][6])); pdf.drawString(155, 640, str(result[i][7])); pdf.drawString(155, 610, str(result[i][8])); pdf.drawString(155, 580, str(result[i][9])); pdf.drawString(155, 550, str(result[i][10])); pdf.drawString(155, 520, str(result[i][11])); 
        pdf.drawString(155, 490, str(result[i][12])); pdf.drawString(155, 460, str(result[i][13])); pdf.drawString(155, 430, str(result[i][14]));pdf.drawString(155, 400, str(result[i][15])); pdf.drawString(155, 370, str(result[i][16])); pdf.drawString(155, 340, str(result[i][17]));

    pdf.save() # SALVANDO O PDF

# FUNÇÃO QUE PERMITE CONSULTAR UMA PESSOA EM ESPECÍFICO ATRAVÉS DO CADASTRO DO SUS
def ConsultaPessoa():
    banco = ConectaBD(); cursor = banco.cursor() # CRIA A INSTÂNCIA DE CONEXÃO COM O BANCO 
    sus = listarCadastroPessoa.campoSUS.text(); sus = str(sus) # CAMPO DE ENTRADA PARA A CHAVE A SER PESQUISADA NO BANCO
    result = cursor.execute("SELECT * FROM Pessoa WHERE cadastro_sus = " + sus); result = cursor.fetchall() # EXECUTANDO O COMANDO E RETORNANDO O VALOR
    telaDeListagem.show(); telaDeListagem.tableWidget.setRowCount(len(result)); telaDeListagem.tableWidget.setColumnCount(18) # MOSTRANDO A TELA DE LISTAGEM
    telaDeListagem.botaoSalvar.clicked.connect(GeraPDF) # CHAMANDO A FUNÇÃO QUE FICA RESPONSAVEL POR SALVAR A CONSULTA EM UM ARQUIVO PDF
    telaDeListagem.botaoExcluir.clicked.connect(ExcluirCadastro) # CHAMANDO A FUNÇÃO QUE FICA RESPONSAVEL POR EXCLUIR UM CADASTRO

    # ITERAÇÃO PARA ESCREVER TODOS OS DADOS NA TELA
    for i in range(0, len(result)):
        for j in range(0, 18):
            telaDeListagem.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))

# FUNÇÃO QUE PERMITE CONSULTAR TODOS OS CADASTROS DE PESSOA NO BANCO
def ConsultarTodos():
    banco = ConectaBD(); cursor = banco.cursor() # CRIA A INSTÂNCIA DE CONEXÃO COM O BANCO 
    sus = listarCadastroPessoa.campoSUS.text(); sus = str(sus) # CAMPO DE ENTRADA PARA A CHAVE A SER PESQUISADA NO BANCO
    result = cursor.execute("SELECT * FROM Pessoa"); result = cursor.fetchall(); # EXECUTANDO O COMANDO E RETORNANDO O VALOR
    telaDeListagem.show(); telaDeListagem.tableWidget.setRowCount(len(result)); telaDeListagem.tableWidget.setColumnCount(18) # MOSTRANDO A TELA DE LISTAGEM
    telaDeListagem.botaoSalvar.clicked.connect(GeraPDF) # CHAMANDO A FUNÇÃO QUE FICA RESPONSAVEL POR SALVAR A CONSULTA EM UM ARQUIVO PDF
    telaDeListagem.botaoExcluir.clicked.connect(ExcluirCadastro) # CHAMANDO A FUNÇÃO QUE FICA RESPONSAVEL POR EXCLUIR UM CADASTRO

    # ITERAÇÃO PARA ESCREVER TODOS OS DADOS NA TELA
    for i in range(0, len(result)):
        for j in range(0, 18):
            telaDeListagem.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))

def ConsultarPorOrdemDeNome():
    banco = ConectaBD(); cursor = banco.cursor() # CRIA A INSTÂNCIA DE CONEXÃO COM O BANCO 
    sus = listarCadastroPessoa.campoSUS.text(); sus = str(sus) # CAMPO DE ENTRADA PARA A CHAVE A SER PESQUISADA NO BANCO
    result = cursor.execute("SELECT Pessoa.nome, Pessoa_Vacina.dataDose, Doenca.codigoDoenca FROM Pessoa INNER JOIN (Pessoa_Vacina INNER JOIN (Vacina INNER JOIN Doenca ON Vacina.idDoenca = Doenca.idDoenca AND Doenca.codigoDoenca = 'COVID-19') ON Pessoa_Vacina.idVacina = Vacina.idVacina) ON Pessoa.idPessoa = Pessoa_Vacina.idPessoa ORDER BY Pessoa.nome, Pessoa_Vacina.dataDose"); result = cursor.fetchall(); # EXECUTANDO O COMANDO E RETORNANDO O VALOR
    telaDeListagem.show(); telaDeListagem.tableWidget.setRowCount(len(result)); telaDeListagem.tableWidget.setColumnCount(18) # MOSTRANDO A TELA DE LISTAGEM
    telaDeListagem.botaoSalvar.clicked.connect(GeraPDF) # CHAMANDO A FUNÇÃO QUE FICA RESPONSAVEL POR SALVAR A CONSULTA EM UM ARQUIVO PDF
    telaDeListagem.botaoExcluir.clicked.connect(ExcluirCadastro) # CHAMANDO A FUNÇÃO QUE FICA RESPONSAVEL POR EXCLUIR UM CADASTRO

    # ITERAÇÃO PARA ESCREVER TODOS OS DADOS NA TELA
    for i in range(0, len(result)):
        for j in range(0, 18):
            telaDeListagem.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))

def SegundaConsulta():
    banco = ConectaBD(); cursor = banco.cursor() # CRIA A INSTÂNCIA DE CONEXÃO COM O BANCO 
    sus = listarCadastroPessoa.campoSUS.text(); sus = str(sus) # CAMPO DE ENTRADA PARA A CHAVE A SER PESQUISADA NO BANCO
    result = cursor.execute("SELECT Pessoa.nome, Pessoa_Vacina.dataDose FROM Pessoa INNER JOIN Pessoa_Vacina ON Pessoa.idPessoa = Pessoa_Vacina.idPessoa ORDER BY Pessoa.nome, Pessoa_Vacina.dataDose"); result = cursor.fetchall(); # EXECUTANDO O COMANDO E RETORNANDO O VALOR
    telaDeListagem.show(); telaDeListagem.tableWidget.setRowCount(len(result)); telaDeListagem.tableWidget.setColumnCount(2) # MOSTRANDO A TELA DE LISTAGEM
    telaDeListagem.botaoSalvar.clicked.connect(GeraPDF) # CHAMANDO A FUNÇÃO QUE FICA RESPONSAVEL POR SALVAR A CONSULTA EM UM ARQUIVO PDF
    telaDeListagem.botaoExcluir.clicked.connect(ExcluirCadastro) # CHAMANDO A FUNÇÃO QUE FICA RESPONSAVEL POR EXCLUIR UM CADASTRO

    # ITERAÇÃO PARA ESCREVER TODOS OS DADOS NA TELA
    for i in range(0, len(result)):
        for j in range(0, 2):
            telaDeListagem.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))

def OrdemDeCep():
    banco = ConectaBD(); cursor = banco.cursor() # CRIA A INSTÂNCIA DE CONEXÃO COM O BANCO 
    sus = listarCadastroPessoa.campoSUS.text(); sus = str(sus) # CAMPO DE ENTRADA PARA A CHAVE A SER PESQUISADA NO BANCO
    result = cursor.execute("SELECT * FROM Pessoa ORDER BY cep"); result = cursor.fetchall(); # EXECUTANDO O COMANDO E RETORNANDO O VALOR
    telaDeListagem.show(); telaDeListagem.tableWidget.setRowCount(len(result)); telaDeListagem.tableWidget.setColumnCount(18) # MOSTRANDO A TELA DE LISTAGEM
    telaDeListagem.botaoSalvar.clicked.connect(GeraPDF) # CHAMANDO A FUNÇÃO QUE FICA RESPONSAVEL POR SALVAR A CONSULTA EM UM ARQUIVO PDF
    telaDeListagem.botaoExcluir.clicked.connect(ExcluirCadastro) # CHAMANDO A FUNÇÃO QUE FICA RESPONSAVEL POR EXCLUIR UM CADASTRO

    # ITERAÇÃO PARA ESCREVER TODOS OS DADOS NA TELA
    for i in range(0, len(result)):
        for j in range(0, 18):
            telaDeListagem.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))

def OrdemIdade():
    banco = ConectaBD(); cursor = banco.cursor() # CRIA A INSTÂNCIA DE CONEXÃO COM O BANCO 
    sus = listarCadastroPessoa.campoSUS.text(); sus = str(sus) # CAMPO DE ENTRADA PARA A CHAVE A SER PESQUISADA NO BANCO
    result = cursor.execute("SELECT * FROM Pessoa WHERE nascimento BETWEEN '1900-01-01' AND '2021-12-31' ORDER BY nascimento DESC"); result = cursor.fetchall(); # EXECUTANDO O COMANDO E RETORNANDO O VALOR
    telaDeListagem.show(); telaDeListagem.tableWidget.setRowCount(len(result)); telaDeListagem.tableWidget.setColumnCount(18) # MOSTRANDO A TELA DE LISTAGEM
    telaDeListagem.botaoSalvar.clicked.connect(GeraPDF) # CHAMANDO A FUNÇÃO QUE FICA RESPONSAVEL POR SALVAR A CONSULTA EM UM ARQUIVO PDF
    telaDeListagem.botaoExcluir.clicked.connect(ExcluirCadastro) # CHAMANDO A FUNÇÃO QUE FICA RESPONSAVEL POR EXCLUIR UM CADASTRO

    # ITERAÇÃO PARA ESCREVER TODOS OS DADOS NA TELA
    for i in range(0, len(result)):
        for j in range(0, 18):
            telaDeListagem.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))

def ExcluirCadastro():
    banco = ConectaBD(); cursor = banco.cursor() # CRIA A INSTÂNCIA DE CONEXÃO COM O BANCO
    linha = telaDeListagem.tableWidget.currentRow(); telaDeListagem.tableWidget.removeRow(linha) # IDENTIFICA A LINHA SELECIONADA NA TELA
    cursor.execute("SELECT cadastro_sus FROM Pessoa"); leitura = cursor.fetchall(); sus = leitura[linha][0] # ISOLANDO O REGISTRO PARA PODER EFETUAR UMA EXCLUSAO
    cursor.execute("DELETE FROM Pessoa WHERE cadastro_sus = " + sus) # EXECUTANDO O COMANDO PARA EXCLUIR UM CADASTRO POR UMA CHAVE DETERMINADA
    banco.commit() # SALVANDO AS ALTERAÇÕES NO BANCO

# FUNÇÃO QUE INVOCA A OUTRA FUNÇÃO E TELA DE CADASTRAR UMA PESSOA
def ChamaCadastro():
    formCadastroPessoa.show() # EXIBE A TELA DE FORMULÁRIO PARA CADASTRAR UMA PESSOA
    formCadastroPessoa.botaoSalvar.clicked.connect(CadastroPessoa) # INVOCA A FUNÇÃO PARA CADASTRAR UMA PESSOA E INSERIR OS DADOS NO BANCO ATRAVÉS DO CLIQUE DO BOTÃO

# FUNÇÃO QUE INVOCA A OUTRA FUNÇÃO E TELA DE CADASTRAR UMA VACINA
def ChamaCadastroVacina():
    formCadastroVacina.show() # EXIBE A TELA DE FORMULÁRIO PARA CADASTRAR UMA VACINA
    formCadastroVacina.botaoProximo.clicked.connect(CadastrarVacina) # INVOCA A FUNÇÃO PARA CADASTRAR UMA VACINA E INSERIR OS DADOS NO BANCO ATRAVÉS DO CLIQUE DO BOTÃO

# FUNÇÃO QUE INVOCA A OUTRA FUNÇÃO E TELA DE CADASTRAR UMA PESSOA_VACINA
def ChamaVacinacao():
    formPessoaVacina.show()
    formPessoaVacina.botaoSalvar.clicked.connect(Vacinacao)

# FUNÇÃO QUE INVOCA A OUTRA FUNÇÃO E TELA DE LISTAR CADASTRO
def ChamaListagem():
    listarCadastroPessoa.show() # EXIBE A TELA DE FORMULÁRIO PARA CONSULTAR UM CADASTRO
    listarCadastroPessoa.botaoConsultar.clicked.connect(ConsultaPessoa) # LISTA UMA PESSOA EM ESPECÍFICO ATRAVÉS DO CLIQUE DO BOTÃO
    listarCadastroPessoa.botaoListarTodos.clicked.connect(ConsultarTodos) # LISTA TODOS OS CADASTROS ATRAVÉS DO CLIQUE DO BOTÃO
    listarCadastroPessoa.botaoOrdemAlfabetica.clicked.connect(ConsultarPorOrdemDeNome) # LISTA TODOS OS CADASTROS ATRAVÉS DO CLIQUE DO BOTÃO
    listarCadastroPessoa.botaoConsultaDois.clicked.connect(SegundaConsulta) # LISTA TODOS OS CADASTROS ATRAVÉS DO CLIQUE DO BOTÃO
    listarCadastroPessoa.botaoOrdemCEP.clicked.connect(OrdemDeCep) # LISTA TODOS OS CADASTROS ATRAVÉS DO CLIQUE DO BOTÃO
    listarCadastroPessoa.botaoOrdemIdade.clicked.connect(OrdemIdade) # LISTA TODOS OS CADASTROS ATRAVÉS DO CLIQUE DO BOTÃO

app = QtWidgets.QApplication([]) # DEFININDO A APLICAÇÃO

telaDeInicio = uic.loadUi("Telas/telaDeInicio.ui") # IMPORTANDO A TELA DE INICIO
formCadastroPessoa = uic.loadUi("Telas/formCadastroPessoa.ui") # IMPORTANDO A TELA DE FORMULÁRIO DE CADASTRO DE PESSOA
listarCadastroPessoa = uic.loadUi("Telas/listarCadastroPessoa.ui") # IMPORTANDO A TELA DE CONSULTA DE CADASTRO
telaDeListagem = uic.loadUi("Telas/telaDeListagem.ui") # IMPORTANDO A TELA PARA LISTAR OS DADOS DE CADASTRO DE PESSOA
formCadastroVacina = uic.loadUi("Telas/formCadastroVacina.ui") # IMPORTANDO A TELA DE FORMULÁRIO DE CADASTRO DE VACINA
formPessoaVacina = uic.loadUi("Telas/formPessoaVacina.ui") # IMPORTANDO A TELA DE FORMULÁRIO DE PESSOA_VACINA

telaDeInicio.botaoCadastrar.clicked.connect(ChamaCadastro) # AÇÃO DO BOTÃO CADASTRAR, QUE INVOCA A FUNÇÃO "ChamaCadastro"
telaDeInicio.botaoListar.clicked.connect(ChamaListagem) # AÇÃO DO BOTÃO LISTAR, QUE INVOCA A FUNÇÃO "ChamaListagem"
telaDeInicio.botaoCadastrarVacina.clicked.connect(ChamaCadastroVacina) # AÇÃO DO BOTÃO CADASTRAR, QUE INVOCA A FUNÇÃO "ChamaCadastroVacina"
telaDeInicio.botaoVacinacao.clicked.connect(ChamaVacinacao) # AÇÃO DO BOTÃO VACINACAO, QUE INVOCA A FUNÇÃO "ChamaVacinacao"

telaDeInicio.show() # EXIBE INICIALMENTE A TELA DE INICIO
app.exec() # EXECUTA A APLICAÇÃO