from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
from sqlalchemy.orm import mapper, sessionmaker, scoped_session

engine = create_engine('sqlite:///:memory:', echo=True)
metadata = MetaData()
users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('user_id', String),
                    Column('link', String),
                    )


class User(object):
    def __init__(self, user_id, link):
        self.user_id = user_id
        self.link = link

    def __repr__(self):
        return "<User('%s','%s')>" % (self.user_id, self.link)


metadata.create_all(engine)
mapper(User, users_table)
Session = sessionmaker(bind=engine)
session = Session()
vasiaUser = User("1111", "lol")
session.add(vasiaUser)
ourUser = session.query(User).filter_by(user_id="1111").first()


def add_user(user_id):
    new_user = User(user_id, "")
    session.add(new_user)
    print(new_user)


def add_link(user_id, link):
    ourUser = session.query(User).filter_by(user_id=user_id).first()
    ourUser.link = link


def print_link(user_id):
    ourUser = session.query(User).filter_by(user_id=user_id).first()
    return ourUser.link


"""if __name__ == "__main__":
    add_user("111")
    new = session.query(User).filter_by(user_id="111").first()
    print(new)
    add_link("111", "axaxaxa")
    new2 = session.query(User).filter_by(user_id="111").first()
    print(print_link("111"))"""

