from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class Audition(Base):
    __tablename__ = 'auditions'
    id = Column(Integer, primary_key=True)
    actor = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=False)  # Ensure phone is stored as a string
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', back_populates='auditions')

    def call_back(self):
        """ Marks an audition as hired. """
        self.hired = True
        session.commit()  # Automatically save the change

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)  # Prevent NULL values
    
    auditions = relationship('Audition', back_populates='role')

    @property
    def actors(self):
        return [audition.actor for audition in self.auditions]

    @property
    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        """ Returns the first hired audition or a message if no one is hired. """
        hired = next((audition for audition in self.auditions if audition.hired), None)
        return hired if hired else 'no actor has been hired for this role'

    def understudy(self):
        """ Returns the second hired audition if available. """
        hired = [audition for audition in self.auditions if audition.hired]
        return hired[1] if len(hired) > 1 else 'no actor has been hired for understudy for this role'


# Create DB and session
engine = create_engine('sqlite:///theatre.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
    
# Seeding data
role = Role(character_name='Tony Stark')

audition1 = Audition(actor='Khalid Abdi', location='London', phone='4478456789', role=role)
audition2 = Audition(actor='James Adam', location='Manchester', phone='4467896439', role=role) 
audition3 = Audition(actor='Susan Taylor', location='Birmingham', phone='4478098545', role=role)

session.add(role)
session.add_all([audition1, audition2, audition3])
session.commit()

print(role.lead())  # Returns the first hired audition or "no actor has been hired"
print(role.understudy())  # Returns the second hired audition or "no actor has been hired for understudy for ths role"