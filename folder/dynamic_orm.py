import logging
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class ORMClassGenerator:
    def __init__(self, engine):
        self.engine = engine
        self.metadata = MetaData()
        self.metadata.bind = self.engine
        self.Session = sessionmaker(bind=self.engine)

    def create_dynamic_class(self, table_name, columns, primary_key):
        """
        Dynamically creates an ORM class based on provided structure.
        """
        attributes = {"__tablename__": table_name}

        col_type_mapping = {
            "int": Integer,
            "string": String,
            "bool": Boolean,
            "float": Float,
            "datetime": DateTime,
        }

        for col_name, col_type in columns.items():
            attributes[col_name] = Column(
                col_type_mapping.get(col_type.lower(), String), primary_key=(col_name == primary_key)
            )

        orm_class = type(table_name, (Base,), attributes)
        return orm_class

    def insert_data(self, orm_class, data):
        """
        Inserts data into the table dynamically.
        """
        session = self.Session()
        try:
            obj = orm_class(**data)
            session.add(obj)
            session.commit()
            logging.info(f"Inserted data into {orm_class.__tablename__}")
        except Exception as e:
            session.rollback()
            logging.error(f"Error inserting data: {e}")
        finally:
            session.close()

    def fetch_all_data(self, orm_class):
        """
        Fetches all data from the table.
        """
        session = self.Session()
        try:
            result = session.query(orm_class).all()
            return result
        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            return None
        finally:
            session.close()

    def update_data(self, orm_class, primary_key, primary_key_value, data):
        """
        Updates an existing record.
        """
        session = self.Session()
        try:
            obj = session.query(orm_class).get(primary_key_value)
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                session.commit()
                logging.info("Updated record successfully")
            else:
                logging.info("No record found to update.")
        except Exception as e:
            session.rollback()
            logging.error(f"Error updating data: {e}")
        finally:
            session.close()

    def delete_data(self, orm_class, primary_key, primary_key_value):
        """
        Deletes a record from the table.
        """
        session = self.Session()
        try:
            obj = session.query(orm_class).get(primary_key_value)
            if obj:
                session.delete(obj)
                session.commit()
                logging.info("Deleted record successfully")
            else:
                logging.info("No record found to delete.")
        except Exception as e:
            session.rollback()
            logging.error(f"Error deleting data: {e}")
        finally:
            session.close()