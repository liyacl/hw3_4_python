from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, BigInteger, Boolean, TIMESTAMP
from db.db_conf import Base


class ShortLink(Base):

    __tablename__ = 'short_link'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(800), nullable=False)
    short_url = Column(String(800), nullable=False)
    custom_alias = Column(String(800))
    
    last_usage_date = Column(TIMESTAMP)
    usage_count = Column(Integer)
    expires_at = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey("users.id"))
    creation_date = Column(TIMESTAMP)

    def __repr__(self):
        return '<ShortLink %r>' % self.id