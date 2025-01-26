from services.app_service import fetch_api_data
from database.dynamic_orm import DynamicORM
from database.engine import init_db, get_session

if __name__ == "__main__":
    # Initialize the database
    init_db()

    # API URL for demonstration
    api_url = "https://jsonplaceholder.typicode.com/todos/1"

    # Fetch API response
    response = fetch_api_data(api_url)

    # Dynamically create a class and table based on the API response
    table_name = "dynamic_table"
    with get_session() as session:
        orm = DynamicORM(session)
        dynamic_class = orm.create_dynamic_class_from_response(table_name, response)
        orm.insert_data(dynamic_class, response)
        print(f"Data inserted into table: {table_name}")

    # Fetch and print the stored data
    with get_session() as session:
        data = session.query(dynamic_class).all()
        for row in data:
            print(row)
