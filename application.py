from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///produtos.db")

@app.route("/cadastrarproduto", methods=["GET", "POST"])
def cadastrarproduto():
   if request.method == "POST":
      nome = request.form.get("nome")
      preço = request.form.get("preço")
    
      if nome  =="" :
         return render_template("cadastrarproduto.html", mensagem="Preencha os campos")
      if preço =="":
         return render_template("cadastrarproduto.html", mensagem="Preencha os campos")
      db.execute("INSERT INTO Produtos (nome, preço) VALUES(?, ?)", nome, preço)
      db.execute("INSERT INTO Entradas (nomedoproduto, quantidade) VALUES(?, ?)", nome, 0)    
      db.execute("INSERT INTO Saídas (nomedoproduto, quantidade) VALUES(?, ?)", nome, 0)    


   return render_template("cadastrarproduto.html", mensagem="")
   
@app.route("/produtos", methods=["GET", "POST"])
def produtos():
    produtos = db.execute("SELECT * FROM produtos")
    if request.method == "POST":
      id = request.form.get("id")
      if id:
          db.execute("DELETE FROM Produtos WHERE id IN (?)", id )
          produtos = db.execute("SELECT * FROM Produtos")
          
      
    return render_template("produtos.html", produtos=produtos)

@app.route("/entrada", methods=["GET", "POST"])
def entrada():
    produtos = db.execute("SELECT * FROM Produtos")
    if request.method == "POST":
      nome = request.form.get("nome")
      quantidade =  request.form.get("quantidade")
      if quantidade == "0":
          return render_template("entrada.html", mensagem="Preencha os campos", produtos=produtos)
      db.execute("INSERT INTO Entradas (nomedoproduto, quantidade) VALUES(?, ?)", nome, quantidade)    

    return render_template("entrada.html", produtos=produtos, mensagem="")

@app.route("/entradas", methods=["GET", "POST"])
def entradas():
    entradas = db.execute("SELECT * FROM Entradas")
 
      
    return render_template("entradas.html", entradas=entradas)
    
@app.route("/saida", methods=["GET", "POST"])
def saida():
    produtos = db.execute("SELECT * FROM Produtos")
    if request.method == "POST":
      nome = request.form.get("nome")
      quantidade =  request.form.get("quantidade")
      if quantidade == "0":
          return render_template("saida.html", mensagem="Preencha os campos", produtos=produtos)
      db.execute("INSERT INTO Saídas (nomedoproduto, quantidade) VALUES(?, ?)", nome, quantidade)    
     
     
    return render_template("saida.html", produtos=produtos, mensagem="")

@app.route("/estoque", methods=["GET", "POST"])
def estoque():
    contagem = db.execute("SELECT COUNT(*) from Produtos")
    grupoentradas = db.execute("SELECT nomedoproduto, SUM(quantidade) quantidade FROM Entradas GROUP BY nomedoproduto ")
    gruposaidas = db.execute("SELECT nomedoproduto, SUM(quantidade) quantidade FROM Saídas GROUP BY nomedoproduto ")
    entradas= []
    saidas= []
    nomes=[]
    for chave in grupoentradas:
        entradas.append(float(chave['quantidade']))
        nomes.append(chave['nomedoproduto'])
    for chave in gruposaidas:
        saidas.append(float(chave['quantidade']))
    
    d= contagem[0]
    n=0
    for key in d:
        n= d[key]
    f=n-1
    total= []
    i=0
    while i<=f:
        total.append(entradas[i]-saidas[i])
        i += 1
        
 
    dicionário = dict(zip(nomes, total))
    
      
        
    return render_template("estoque.html", grupoentradas=grupoentradas, d=d,n=n, saidas=saidas, entradas=entradas, dicionário=dicionário, total=total, contagem=contagem)
    

    
@app.route("/saidas", methods=["GET", "POST"])
def saidas():
    saídas = db.execute("SELECT * FROM Saídas")
   
    return render_template("saídas.html", saídas=saídas)


@app.route("/")
def index():
     return render_template("home.html")

