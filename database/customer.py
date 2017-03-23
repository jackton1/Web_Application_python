from sqlalchemy import (Integer, CheckConstraint, Table, Boolean,
                        Column, DateTime, Numeric, ForeignKeyConstraint,
                        Text, String, ForeignKey, event,
                        UniqueConstraint, create_engine)
from sqlalchemy import Unicode

from zope.sqlalchemy import ZopeTransactionExtension

from passlib.hash import sha256_crypt
from sqlalchemy import case
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.schema import MetaData, CreateSchema
from sqlalchemy.engine import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_session, synonym, sessionmaker, scoped_session

engine = create_engine('sqlite:///customer.db')
metadata = MetaData(bind=engine)
Base = declarative_base()

db = sessionmaker(bind=engine)
_db = scoped_session(sessionmaker(bind=engine,
                                  extension=ZopeTransactionExtension()))

db_ = sessionmaker(bind=engine)
db_ = db_()


# event.listen(metadata, 'before_create', )
# engine.execute(CreateSchema('web', bind=engine))


class Customer(Base):
    __tablename__ = 'customers'
    __metadata__ = metadata

    __table_args__ = (
        CheckConstraint('age > 0', name='customer_age_check'),
        # {'schema': 'web'},
        UniqueConstraint('pass_phrase')
    )

    user_id = Column('user_id', Integer, primary_key=True)
    age = Column('age', Integer, server_default='1', nullable=False)
    first_name = Column('first_name', String(255), nullable=False)
    middle_name = Column('middle_name', String(255), nullable=True)
    last_name = Column('last_name', String(255), nullable=False)
    pass_phrase = Column('pass_phrase', String(255))
    active = Column('active', Boolean, server_default='True')
    _password = Column('password', Unicode, nullable=False)

    def _set_pswd(self, password):
        self._password = sha256_crypt.hash(password)

    def _get_pswd(self):
        return self._password

    password = synonym('_password',
                       descriptor=property(fget=_get_pswd, fset=_set_pswd))

    # def _set_password(self, password):
    #     """Hash password using sha1 and a random salt before saving."""
    #     db = object_session(self)
    #     self._password = func.crypt(password, func.gen_salt('bf', 8))
    #
    # def _get_password(self):
    #     return self._password
    #
    # password = synonym('_password', descriptor=property(_get_password,
    #                                                     _set_password))

    def __str__(self):
        return repr('%s %s' % (self.first_name, self.last_name))

    @hybrid_property
    def status(self):
        if self.active and self.age != 1:
            return True
        else:
            return False

    @status.expression
    def status(cls):
        return case([(cls.active and cls.age > 1, True)], _else=False)

    def validate_password(self, password):
        valid = sha256_crypt.verify(password, self._password)
        return valid


def _run(database=None):
    Base.metadata.bind = database
    tables = [tb for tb in Base.metadata.sorted_tables]
    metadata.create_all(tables=tables)


def test_():
    users = db_.query(Customer).all()
    if not users:
#         engine.execute("""INSERT INTO customers (age, first_name, last_name,
#                        pass_phrase, active, password)
# VALUES (20,  'Tonye', 'Jack', 'Test phrase', :status, 'abc123')""", {'status': True})
#         db_.begin()
        user = Customer()
        user.first_name = 'Tonye'
        user.last_name = 'Jack'
        user.pass_phrase = 'Test Phrase'
        user.active = True
        user.password = 'abe123'

        db_.add(user)

        db_.flush()
    print([user for user in db_.query(Customer).all()])

_run(db)
test_()
