from sqlalchemy import create_engine
from sqlalchemy import (CheckConstraint, Column, Integer, String, DateTime, Float, ForeignKey, Text)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BikeTerminal(Base):
    __tablename__ = 'bike_terminals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    moment = Column(DateTime)
    station_id = Column(Integer, ForeignKey('stations.id', ondelete='CASCADE'), nullable=False)
    bikes = Column(Integer)
    spaces = Column(Integer)


class Station(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'), nullable=False)
    name = Column(String)

    def __repr__(self):
        return '<Station #{} [City {}]>'.format(self.id, self.city_id)

    def __str__(self):
        return '<{}>'.format(self.name)


class Coordinates(Base):
    __tablename__ = 'coordinates'

    station_id = Column(Integer, ForeignKey('stations.id', ondelete='CASCADE'),
                        primary_key=True, nullable=False)
    altitude = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)

    def __repr__(self):
        return '<Station #{} [City {}]: ({},{})>'.format(self.id, self.city_id, self.latitude, self.longitude)

    def __str__(self):
        return '<({},{}) - {}>'.format(self.latitude, self.longitude, self.name)


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return '<City #{}>'.format(self.name)

    def __str__(self):
        return '<{}>'.format(self.name)


class Weather(Base):
    __tablename__ = 'weathers'

    moment = Column(DateTime, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    clouds = Column(String)
    description = Column(String)
    humidity = Column(Float)
    pressure = Column(Float)
    temperature = Column(Float)
    wind = Column(Float)


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
