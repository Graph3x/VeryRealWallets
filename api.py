from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)



class Wallet(db.Model):
	idn = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
	owner = db.Column(db.String(20), nullable=False)
	balance = db.Column(db.Integer)

	def __repr__(self):
		return f'{self.owner} - {self.balance}'


@app.route('/')
def index():
	return 'This is VeryRealWalletsAPI. You can display wallets on /wallets, '

@app.route('/wallets')
def get_wallets():
	wallets = Wallet.query.all()

	output = []
	for wallet in wallets:
		wdata = {'owner': wallet.owner, 'balance' : wallet.balance}
		output.append(wdata)
	return {'wallets':output}


@app.route('/wallets/<idn>')
def get_wallet(idn):
	wallet = Wallet.query.get_or_404(idn)
	return {'owner': wallet.owner, 'balance': wallet.balance}


@app.route('/wallets/', methods=['POST'])
def add_wallet():
	wallet = Wallet(owner=request.json['owner'], balance=request.json['balance'])
	db.session.add(wallet)
	db.session.commit()
	return {'idn': wallet.idn}


@app.route('/wallets/<idn>', methods=['DELETE'])
def delete_wallet(idn):
	wallet = Wallet.query.get_or_404(idn)

	db.session.delete(wallet)
	db.session.commit()
	return {'status': 200}


@app.route('/wallets/<idn>', methods=['PUT'])
def update_wallet(idn):
	wallet = Wallet.query.get_or_404(idn)
	wallet.owner = request.json['owner']
	wallet.balance = request.json['balance']
	
	db.session.commit()
	return {'status': 200}


if __name__ == '__main__':
	app.run()