from sqlalchemy import Column, String, Integer, Text
from database.engine import Base

class DynamicORM:
    def __init__(self, session):
        self.session = session

    def create_dynamic_class_from_response(self, table_name, response):
        """
        Dynamically create a class and table based on the API response keys.
        """
        # Ensure the 'id' column is always included as the primary key
        attributes = {
            "__tablename__": table_name,
            "__table_args__": {"extend_existing": True},
        }

        # Add the 'id' column explicitly as the primary key
        

        # Dynamically add columns based on the response keys
        for key, value in response.items():
            column_type = String if isinstance(value, str) else Integer
            if(key == "id") :
                attributes[key] = Column(Integer, primary_key=True, autoincrement=True)
            else:
                attributes[key] = Column(column_type, nullable=True)

        # Dynamically create the class
        try:
            dynamic_class = type(table_name.capitalize(), (Base,), attributes)
        except Exception as e:
            print(f"Error creating dynamic class: {e}")
            raise

        # Create the table in the database
        try:
            Base.metadata.create_all(self.session.bind)
        except Exception as e:
            print(f"Error creating table in database: {e}")
            raise

        return dynamic_class

    def insert_data(self, dynamic_class, data):
        """
        Insert data into the dynamically created table.
        """
        try:
            obj = dynamic_class(**data)
            self.session.add(obj)
            self.session.commit()
        except Exception as e:
            print(f"Error inserting data: {e}")
            raise