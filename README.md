# Data-Engineering-ETL-Weather-Project 🌦️🚀

## Project Highlights ✨

This project is a simple ETL pipeline built using **Apache Airflow** on **Astronomer** to extract, transform, and load weather data into a **PostgreSQL** database. Here's what makes it awesome:

- **Technologies Used**:
  - 🐍 **Python**: For scripting the ETL tasks.
  - 🐳 **Docker**: To containerize the entire setup for easy deployment.
  - 🌬️ **Apache Airflow**: To orchestrate and automate the ETL workflow.
  - 🗄️ **PostgreSQL**: As the database to store the transformed weather data.
  - 🌌 **Astronomer**: As the platform to run and manage Airflow seamlessly.

- **ETL Workflow**:
  1. **Extract**: Fetch daily weather data from the Open-Meteo API.
  2. **Transform**: Process and structure the data for storage.
  3. **Load**: Insert the transformed data into a PostgreSQL database.

- **Key Features**:
  - Fully automated daily weather data ingestion. ⏰
  - Scalable and containerized using Docker. 🐳
  - Easy-to-use and deploy with Astronomer. 🌌

---

### How to Run the Project 🛠️

1. Clone the repository.
2. Start the services using Docker Compose.
3. Access the Airflow UI to monitor and trigger the ETL pipeline.

Enjoy building data pipelines with Airflow and Astronomer! 🚀