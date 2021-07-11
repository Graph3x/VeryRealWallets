from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

def getkey():
	return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))


class Wallet(db.Model):
	idn = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
	owner = db.Column(db.String(20), nullable=False)
	balance = db.Column(db.Integer)
	key = db.Column(db.String(16), nullable=False)

	def __repr__(self):
		return f'{self.owner} - {self.balance}'


@app.route('/')
def index():
	return '''This is VeryRealWallets API. You can display wallets on /wallets.
	 Create one by sending a POST request. You will get your api key, that you can use to send other requests. Full documentation on github'''

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


@app.route('/wallets', methods=['POST'])
def add_wallet():
	k = getkey()
	wallet = Wallet(owner=request.json['owner'], balance=request.json['balance'], key = k)
	db.session.add(wallet)
	db.session.commit()
	return {'idn': wallet.idn, 'key': k}


@app.route('/wallets/<idn>', methods=['DELETE'])
def delete_wallet(idn):
	wallet = Wallet.query.get_or_404(idn)

	if request.json['key'] == wallet.key:
		db.session.delete(wallet)
		db.session.commit()
		return {'status': 200}
	else:
		return {'status': 401}


@app.route('/wallets/<idn>', methods=['PUT'])
def update_wallet(idn):
	wallet = Wallet.query.get_or_404(idn)
	wallet.owner = request.json['owner']
	wallet.balance = request.json['balance']
	if request.json['key'] == 'admin':
		db.session.commit()
		return {'status': 200}
	else:
		return {'status': 401}


@app.route('/transfer/<idn>', methods=['POST'])
def transfer(idn):
	wallet = Wallet.query.get_or_404(idn)
	transfer = int(request.json['transfer'])
	targeti = request.json['target']
	target = Wallet.query.get_or_404(int(targeti))

	if request.json['key'] == wallet.key:
		if transfer < wallet.balance:
			wallet.balance -= transfer
			target.balance += transfer

			db.session.commit()
			return {'status': 200}

		else:
			return {'status': 402}
	else:
		return {'status': 401}


if __name__ == '__main__':
	app.run()