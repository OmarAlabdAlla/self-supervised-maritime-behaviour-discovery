import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


def create_db_engine():

    load_dotenv()

    engine = create_engine(
        f"postgresql://{os.getenv('USERNAME_db')}:{os.getenv('PASSWORD_db')}"
        f"@{os.getenv('HOST_db')}:{os.getenv('PORT_db')}/{os.getenv('DB_db')}",
        pool_size=10,
        max_overflow=2,
    )

    return engine


# if __name__ == "__main__":
#     engine = create_db_engine()

#     try:
#         with engine.connect() as conn:
#             print(" Database connection successful")
#     except Exception as e:
#         print(" Connection failed:")
#         print(e)
#     load_dotenv()
    
#     print("USERNAME_db =", os.getenv("USERNAME_db"))
#     print("PASSWORD_db =", "***" if os.getenv("PASSWORD_db") else None)
#     print("HOST_db =", os.getenv("HOST_db"))
#     print("PORT_db =", os.getenv("PORT_db"))
#     print("DB_db =", os.getenv("DB_db"))