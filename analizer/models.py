from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

offer_skill_association = Table(
    'offer_skill', Base.metadata,
    Column('offer_id', Integer, ForeignKey('offer.id')),
    Column('skill_id', Integer, ForeignKey('skill.id'))
)

class Offer(Base):
    __tablename__ = 'offer'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    level = Column(String(20))
    link_to_offer = Column(String)
    description = Column(String)
    operating_mode = Column(String)
    salary = Column(String)
    
    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship('Company', back_populates='offers')
    skills = relationship('Skill', secondary=offer_skill_association, back_populates='offers')

class Company(Base):
    __tablename__ = 'company'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    offers = relationship('Offer', back_populates='company')

class Skill(Base):
    __tablename__ = 'skill'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    
    offers = relationship('Offer', secondary=offer_skill_association, back_populates='skills')

def init_db(uri='sqlite:///dupa.db'):
    engine = create_engine(uri)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

if __name__ == "__main__":
    Session = init_db()
    session = Session()