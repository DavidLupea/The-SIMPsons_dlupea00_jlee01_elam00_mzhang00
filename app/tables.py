from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    code = db.Column(db.String(3), nullable=False)
    population = db.Column(db.Integer)

    cases = db.relationship('Cases', backref='country', lazy='dynamic')
    deaths = db.relationship('Deaths', backref='country', lazy='dynamic')
    recovered = db.relationship('Recovered', backref='country', lazy='dynamic')

    def __init__(self, code, population):
        self.code = code
        self.population = population


class Cases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    country_id = db.Column(db.ForeignKey('countries.id'))

    deaths = db.relationship('Deaths', backref='cases', uselist=False)
    recovered = db.relationship('Recovered', backref='cases', uselist=False)

    def __init__(self, date, amount, country_id):
        self.date = date
        self.amount = amount
        self.country_id = country_id


class Deaths(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    country_id = db.Column(db.ForeignKey('countries.id'))
    cases_id = db.Column(db.ForeignKey('cases.id'))

    def __init__(self, date, amount, country_id, cases_id):
        self.date = date
        self.amount = amount
        self.country_id = country_id
        self.cases_id = cases_id


class Recovered(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    country_id = db.Column(db.ForeignKey('countries.id'))
    cases_id = db.Column(db.ForeignKey('cases.id'))

    def __init__(self, date, amount, country_id, cases_id):
        self.date = date
        self.amount = amount
        self.country_id = country_id
        self.cases_id = cases_id

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #NAME AND SECTOR_NAME ARE SWITCHED IN THE DATABASE
    name = db.Column(db.String(10), nullable=False)
    sector_name = db.Column(db.String(10), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    market_cap = db.Column(db.Integer, nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))
    #relationships
    data_points = db.relationship('DailyData', backref='company')
    def __init__(self, name, sector_name, symbol, market_cap):
        self.sector_name = sector_name
        self.name = name
        self.symbol = symbol
        self.market_cap = market_cap

class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    #relationships
    companies = db.relationship('Company', backref='sector')
    data_points = db.relationship('DailyData', backref = 'sector')
    # data_points = db.relationship('SectorData', backref='sector')
    def __init__(self,name):
        self.name = name

class DailyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    company_id =  db.Column(db.Integer, db.ForeignKey('company.id'))
    sector_id = db.Column(db.Integer,db.ForeignKey('sector.id'))
    def __init__(self,date,price):
        self.date = date
        self.price = price
