from sqlalchemy import Column, String, Integer
from database.engine import Base

class DynamicORM:
    def __init__(self, session):
        self.session = session

    def create_dynamic_class_from_response(self, table_name, response):
        """
        Dynamically create a class and table based on the API response keys.
        """
        attributes = {
            "__tablename__": table_name,
            "__table_args__": {"extend_existing": True},
            "id": Column(Integer, primary_key=True, autoincrement=True),  # Define primary key
        }

        # Add columns based on the API response
        for key, value in response.items():
            column_type = String if isinstance(value, str) else Integer
            attributes[key] = Column(column_type, nullable=True)

        # Create the dynamic class
        dynamic_class = type(table_name.capitalize(), (Base,), attributes)

        # Create the table in the database
        Base.metadata.create_all(self.session.bind)

        return dynamic_class

    def insert_data(self, dynamic_class, data):
        """
        Insert data into the dynamically created table.
        """
        obj = dynamic_class(**data)
        self.session.add(obj)
        self.session.commit()