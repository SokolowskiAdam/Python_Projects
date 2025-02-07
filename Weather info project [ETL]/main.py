import os
import sqlite3
from datetime import datetime
import requests


class WeatherETL:
    def __init__(self, db_path, api_key):
        self.db_path = db_path
        self.api_key = api_key
        self.api_url = "http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
        self._create_tables()
        self._add_example_cities()

    def _connect(self):
        """Creates connection to SQLite database."""
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Database connection error: {e.sqlite_errorcode} - {e.sqlite_errorname}")
            return None

    def _create_tables(self) -> None:
        """Creates database tables if they don't exist."""
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS cities (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT UNIQUE NOT NULL
                        );
                """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS weather_info (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT NOT NULL,
                        current_weather TEXT,
                        temperature REAL,
                        load_datetime TEXT,
                        UNIQUE(city, load_datetime)
                    );
                """
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error during creation of the tables: {e.sqlite_errorcode} - {e.sqlite_errorname}")

    def _add_example_cities(self) -> None:
        """Checks if table with cities is empty and adds some example cities if needed."""
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT CASE WHEN EXISTS(SELECT 1 FROM cities) THEN 0 ELSE 1 END AS IsEmpty;"
                )
                is_empty = cursor.fetchone()[0]
                if is_empty == 1:
                    cities = [("London",), ("Warsaw",), ("Lodz",)]  # Example cities list
                    cursor.executemany("INSERT INTO cities (name) VALUES (?);", cities)
                    print("Example cities were added.")
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error during cities addition to db: {e.sqlite_errorcode} - {e.sqlite_errorname}")

    def get_cities(self) -> list:
        """Gets list of cities from database."""
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM cities;")
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error during getting list of cities from db: {e.sqlite_errorcode} - {e.sqlite_errorname}")
            return []

    def fetch_weather(self, city: str) -> tuple:
        """Gets current weather and temperature for each city."""
        try:
            response = requests.get(self.api_url.format(city=city, key=self.api_key))
            response.raise_for_status()  # Checks HTTP status code
            data = response.json()
            return data["weather"][0]["description"], data["main"]["temp"]
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh.args[0]}, for city: {city}")
            return None, None
        except requests.exceptions.ReadTimeout as errrt:
            print(f"Time out: {errrt}, for city: {city}")
            return None, None
        except requests.exceptions.ConnectionError as conerr:
            print(f"Connection error: {conerr}, for city: {city}")
            return None, None
        except requests.RequestException as errex:
            print(f"Error during downloading weather data for {city}: {errex}")
            return None, None

    def save_weather_data(self, data: list) -> None:
        """Saves downloaded weather data to Weather database."""
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                for city, weather, temp, timestamp in data:
                    cursor.execute(
                        """
                            INSERT OR IGNORE INTO weather_info (city, current_weather, temperature, load_datetime)
                            VALUES (?, ?, ?, ?);
                            """,
                        (city, weather, temp, timestamp),
                    )
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error during saving weather data to table: {e.sqlite_errorcode} - {e.sqlite_errorname}")


    def run_etl(self) -> None:
        """Runs ETL process."""
        cities = self.get_cities()
        if not cities:
            print("No cities found in database.")
            return

        weather_data = []
        for city in cities:
            weather, temp = self.fetch_weather(city)
            if weather and temp:
                weather_data.append(
                    (city, weather, temp, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )

        if not weather_data:
            print("Couldn't download weather data.")
            return

        self.save_weather_data(weather_data)


if __name__ == "__main__":
    etl = WeatherETL(db_path="database.db", api_key=os.getenv("API_KEY"))
    etl.run_etl()
