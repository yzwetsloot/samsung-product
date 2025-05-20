import argparse

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    text,
    func,
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"
    id = Column(String, primary_key=True)

    ean = Column(String(13), nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    score = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    modified_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        server_onupdate="CURRENT_TIMESTAMP",
    )

    reference_price = Column(Float)
    image = Column(String)
    color = Column(String)
    size = Column(String)

    _price = relationship(
        "Price", backref="product", passive_deletes=True, passive_updates=True
    )
    _quantity = relationship(
        "Quantity", backref="product", passive_deletes=True, passive_updates=True
    )


class Price(Base):
    __tablename__ = "price"
    id = Column(
        String,
        ForeignKey("product.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    value = Column(Float, primary_key=True)
    created_at = Column(DateTime, primary_key=True, server_default=func.now())

    modified_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    weight = Column(Integer, nullable=False, server_default="1")
    notified = Column(Boolean, server_default="f", nullable=False)


class Quantity(Base):
    __tablename__ = "quantity"
    id = Column(
        String,
        ForeignKey("product.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    value = Column(Float, primary_key=True)
    created_at = Column(DateTime, primary_key=True, server_default=func.now())

    modified_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    weight = Column(Integer, nullable=False, server_default="1")


class Promotion(Base):
    __tablename__ = "promotion"
    id = Column(
        String,
        ForeignKey("product.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    code = Column(Text, primary_key=True)

    description = Column(Text, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    modified_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )


def connect_db(user, password, host, port, database):
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    return engine


def get_session(user, password, host, port, database):
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--user", type=str, required=True)
    parser.add_argument("-p", "--password", type=str, required=True)
    parser.add_argument("-H", "--host", type=str, required=True)
    parser.add_argument("-P", "--port", type=str, required=True)
    parser.add_argument("-d", "--database", type=str, required=True)

    args = parser.parse_args()

    engine = connect_db(args.user, args.password, args.host, args.port, args.database)
    Product.__table__.create(bind=engine, checkfirst=True)
    Price.__table__.create(bind=engine, checkfirst=True)
    Quantity.__table__.create(bind=engine, checkfirst=True)
    Promotion.__table__.create(bind=engine, checkfirst=True)

    # auto-update `modified_at` columns
    create_refresh_modified_at_func = """
        CREATE FUNCTION {schema}.refresh_modified_at()
        RETURNS TRIGGER
        LANGUAGE plpgsql AS
        $func$
        BEGIN
        NEW.modified_at := now();
        RETURN NEW;
        END
        $func$;
    """

    create_trigger = """
        CREATE TRIGGER trig_{table}_updated BEFORE UPDATE ON {schema}.{table}
        FOR EACH ROW EXECUTE PROCEDURE {schema}.refresh_modified_at();
    """

    schema = "public"

    engine.execute(text(create_refresh_modified_at_func.format(schema=schema)))

    engine.execute(text(create_trigger.format(schema=schema, table="product")))
    engine.execute(text(create_trigger.format(schema=schema, table="price")))
    engine.execute(text(create_trigger.format(schema=schema, table="quantity")))
    engine.execute(text(create_trigger.format(schema=schema, table="promotion")))
