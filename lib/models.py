from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Define the base class for SQLAlchemy models
Base = declarative_base()

# Define the Audition model
class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)  # Unique ID for each audition
    actor = Column(String(50), nullable=False)  # Name of the actor
    location = Column(String(50), nullable=False)  # Location of the audition
    phone = Column(String(15), nullable=False)  # Phone number (stored as string)
    hired = Column(Boolean, default=False)  # Whether the actor was hired or not
    role_id = Column(Integer, ForeignKey('roles.id'))  # Foreign key linking to a role

    # Define relationship to Role model
    role = relationship('Role', back_populates='auditions')

    def call_back(self):
        """Marks an audition as hired."""
        self.hired = True

# Define the Role model
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)  # Unique ID for each role
    character_name = Column(String, nullable=False)  # Name of the character

    # Define relationship to Audition model
    auditions = relationship('Audition', back_populates='role')

    @property
    def actors(self):
        """Returns a list of actor names."""
        return [audition.actor for audition in self.auditions]

    @property
    def locations(self):
        """Returns a list of locations."""
        return [audition.location for audition in self.auditions]

    def lead(self):
        """Returns the first hired actor's name or a message if no one is hired."""
        hired = next((audition for audition in self.auditions if audition.hired), None)
        return hired.actor if hired else 'no actor has been hired for this role'

    def understudy(self):
        """Returns the second hired actor's name or a message if no understudy is available."""
        hired = [audition for audition in self.auditions if audition.hired]
        return hired[1].actor if len(hired) > 1 else 'no actor has been hired for understudy for this role'
# Db setup
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

# Auditions 
audition1.call_back()  # Hire first actor
audition2.call_back()  # Hire second actor
session.commit()  # Save hiring changes

# Testing
print(role.lead())  # Expected: audition1 (Khalid Abdi)
print(role.understudy())  # Expected: audition2 (James Adam)
