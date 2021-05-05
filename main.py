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

    if(con.is_connected()):
        db_info = con.get_server_info()
        print("Conexao establecida com sucesso", db_info)
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)

    return con

def CadastroPessoa():

    banco = ConectaBD()
    cursor = banco.cursor()

    nome = formCadastroPessoa.campoNome.text()
    mae = formCadastroPessoa.campoMae.text()
    sus = formCadastroPessoa.campoSUS.text()
    sexo = formCadastroPessoa.campoSexo.text()
    cpf = formCadastroPessoa.campoCPF.text()
    alergias = formCadastroPessoa.campoAlergia.text()
    rua = formCadastroPessoa.campoRua.text()
    numero = formCadastroPessoa.campoNumero.text()
    municipio = formCadastroPessoa.campoMunicipio.text()
    estado = formCadastroPessoa.campoEstado.text()
    cep = formCadastroPessoa.campoCEP.text()    
    nascimento = QDate.getDate(formCadastroPessoa.campoNascimento.selectedDate()); data = datetime(nascimento[0]  , nascimento[1], nascimento[2])

    idEstadoCivil = cursor.execute("SELECT idEstadoCivil FROM Estado_Civil"); idEstadoCivilLido = cursor.fetchall(); idEstadoCivil = int(idEstadoCivilLido[0][0])
    idReligiao = cursor.execute("SELECT idReligiao FROM Religiao"); idReligiaoLido = cursor.fetchall(); idReligiao = int(idReligiaoLido[0][0])
    idEscolaridade = cursor.execute("SELECT idEscolaridade FROM Escolaridade"); idEscolaLido = cursor.fetchall(); idEscolaridade = int(idEscolaLido[0][0])
    idPlano = cursor.execute("SELECT idPlano FROM Plano_Saude"); idPlanoLido = cursor.fetchall(); idPlano = int(idPlanoLido[0][0])
    idSensiveis = cursor.execute("SELECT idSensiveis FROM Sensiveis"); idSensiveisLido = cursor.fetchall(); idSensiveis = int(idSensiveisLido[0][0])

    insere_banco = "INSERT INTO Pessoa(nome, nascimento, nome_mae, cadastro_sus, sexo_genetico, cpf, alergias, idEstadoCivil, idEscolaridade, idPlanoSaude, idReligiao, idSensiveis, rua, numeroRua, municipio, estado, cep) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    dados = (nome, data, mae, sus, sexo, cpf, alergias, idEstadoCivil, idEscolaridade, idPlano, idReligiao, idSensiveis, rua, numero, municipio, estado, cep)
    cursor.execute(insere_banco, dados)
    banco.commit()

    # # # LIMPANDO OS DADOS DA TELA
    formCadastroPessoa.campoNome.setText('')
    formCadastroPessoa.campoMae.setText('')
    formCadastroPessoa.campoSUS.setText('')
    formCadastroPessoa.campoSexo.setText('')
    formCadastroPessoa.campoCPF.setText('')
    formCadastroPessoa.campoAlergia.setText('')
    formCadastroPessoa.campoRua.setText('')
    formCadastroPessoa.campoNumero.setText('')
    formCadastroPessoa.campoMunicipio.setText('')
    formCadastroPessoa.campoEstado.setText('')
    formCadastroPessoa.campoCEP.setText('')

def GeraPDF():
    banco = ConectaBD(); cursor = banco.cursor()
    result = cursor.execute("SELECT * FROM Pessoa"); result = cursor.fetchall()
    y = 0;
    pdf = canvas.Canvas("cadastros_pessoas.pdf")
    # pdf.setFont(psfontname="Tahoma", size=22); 
    pdf.drawString(200, 1200, "Produtos cadastrados: "); 
    # pdf.setFont(psfontname="Tahoma", size=12);
    pdf.drawString(10, 950, "ID"); 
    pdf.drawString(10, 900, "NOME"); 
    pdf.drawString(10, 850, "NASCIMENTO"); 
    pdf.drawString(10, 800, "MAE");
    pdf.drawString(10, 750, "SUS"); 
    pdf.drawString(10, 700, "SEXO");
    pdf.drawString(10, 650, "CPF"); 
    pdf.drawString(10, 600, "ALERGIAS"); 
    pdf.drawString(10, 550, "ESTADO CIVIL"); 
    pdf.drawString(10, 500, "ESCOLARIDADE"); 
    pdf.drawString(10, 450, "PLANO DE SAUDE"); 
    pdf.drawString(10, 400, "RELIGIAO");
    pdf.drawString(10, 350, "SENSIVEIS"); 
    pdf.drawString(10, 300, "RUA"); 
    pdf.drawString(10, 250, "NUMERO"); 
    pdf.drawString(10, 200, "MUNICIPIO"); 
    pdf.drawString(10, 150, "ESTADO"); 
    pdf.drawString(10, 100, "CEP");

    for i in range(0, len(result)):
        y += 50
        pdf.drawString(140, 950-y, str(result[i][0])); 
        pdf.drawString(140, 900-y, str(result[i][1])); 
        pdf.drawString(140, 850-y, str(result[i][2])); 
        pdf.drawString(140, 800-y, str(result[i][3])); 
        pdf.drawString(140, 750-y, str(result[i][4]));
        pdf.drawString(140, 700-y, str(result[i][5])); 
        pdf.drawString(140, 650-y, str(result[i][6])); 
        pdf.drawString(140, 600-y, str(result[i][7])); 
        pdf.drawString(140, 550-y, str(result[i][8])); 
        pdf.drawString(140, 500-y, str(result[i][9]));
        pdf.drawString(140, 450-y, str(result[i][10])); 
        pdf.drawString(140, 400-y, str(result[i][11])); 
        pdf.drawString(140, 350-y, str(result[i][12])); 
        pdf.drawString(140, 300-y, str(result[i][13])); 
        pdf.drawString(140, 250-y, str(result[i][14]));
        pdf.drawString(140, 200-y, str(result[i][15])); 
        pdf.drawString(140, 150-y, str(result[i][16])); 
        pdf.drawString(140, 100-y, str(result[i][17]));

    pdf.save()

def ConsultaPessoa():

    banco = ConectaBD(); cursor = banco.cursor()    
    sus = listarCadastroPessoa.campoSUS.text()
    sus = str(sus)
    result = cursor.execute("SELECT * FROM Pessoa WHERE cadastro_sus = " + sus); result = cursor.fetchall()
    telaDeListagem.show()
    telaDeListagem.tableWidget.setRowCount(len(result))
    telaDeListagem.tableWidget.setRowCount(17)
    telaDeListagem.botaoSalvar.clicked.connect(GeraPDF)



    for i in range(0, len(result)):
        for j in range(0, 17):
            telaDeListagem.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))

def ConsultarTodos():

    banco = ConectaBD()
    cursor = banco.cursor()    
    sus = listarCadastroPessoa.campoSUS.text()
    sus = str(sus)
    result = cursor.execute("SELECT * FROM Pessoa"); result = cursor.fetchall()
    telaDeListagem.show()
    telaDeListagem.tableWidget.setRowCount(len(result))
    telaDeListagem.tableWidget.setRowCount(17)

    for i in range(0, len(result)):
        for j in range(0, 17):
            telaDeListagem.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))







def ChamaCadastro():
    formCadastroPessoa.show()
    formCadastroPessoa.botaoSalvar.clicked.connect(CadastroPessoa)

def ChamaListagem():
    listarCadastroPessoa.show()
    listarCadastroPessoa.botaoConsultar.clicked.connect(ConsultaPessoa)
    listarCadastroPessoa.botaoListarTodos.clicked.connect(ConsultarTodos)



app = QtWidgets.QApplication([])

telaDeInicio = uic.loadUi("Telas/telaDeInicio.ui")
formCadastroPessoa = uic.loadUi("Telas/formCadastroPessoa.ui")
listarCadastroPessoa = uic.loadUi("Telas/listarCadastroPessoa.ui")
telaDeListagem = uic.loadUi("Telas/telaDeListagem.ui")

telaDeInicio.botaoCadastrar.clicked.connect(ChamaCadastro)
telaDeInicio.botaoListar.clicked.connect(ChamaListagem)

telaDeInicio.show()
app.exec()