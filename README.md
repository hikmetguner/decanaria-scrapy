# Project Title

Decanaria Software Engineer Take Home Project

## Installation

1. Clone the repository.
2. Run the docker compose file using `docker-compose up -d`.
3. Configure settings in `settings.py`.
4. In case the changes in the settings.py does not sync with the running containers use `docker-compose down --volumes` and redo step 2
5. Let the container `scrapy` run.

## Usage

After the container starts the docker environment and `run.sh` script handles all the execution, the program reads the given inputs `s01.json` and `s02.json`, yields them to pipelines JobItemPipeline, PostgreSQLPipeline and MongoDBPipeline in the given order. After `crawl` is successful the JSON data is itemized, converted into dictionaries and stored in PostgreSQL and MongoDB instances running within the same docker initialization. Finally the `query.py` script is executed, fetching the stored JSON data within both databases and turns them into readable CSV format.

## License

This project is probably licensed to Decanaria team

## Credits

- Decanaria Team
- Hikmet Güner
