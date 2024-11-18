# Calendar Events to ICS Converter
This repository contains a Python script that reads calendar events from a CSV file and generates an ICS file for importing into your favorite calendar application.

## Features
- Converts calendar events from CSV to ICS format
- Supports all-day events
- Logs the conversion process

## Requirements
- Docker and docker compose
OR
- Conda
OR
- Python 3.x
- [icalendar](https://pypi.org/project/icalendar/)
- [python-dateutil](https://pypi.org/project/python-dateutil/)
  
## CSV File Format
The `app/source.csv` file has the following columns:
- `DTSTART`: Start date and time of the event (for an all-day event, do not include a time)
- `DTEND`: End date and time of the event (leave blank for an all-day event)
- `DESCRIPTION`: Description of the event. If the description includes commas, the description field should be in quotations. 
- `SUMMARY`: Summary or heading of the event

A spreadsheet application can be used to generate the `app/sources.csv` file.

## Running the Project
### Using Docker
1. Clone the repository:
   ```git clone <repository-url>
   cd <repository-directory>```
2. Build and run the Docker container:
```docker compose up --build```
3. After the script completes, the generated `calendar.ics` file and `log.txt` file will be in the output folder.

### Using Conda
1. Clone the repository:
   ```git clone <repository-url>
   cd <repository-directory>```
2. Create a conda environment from the `.yml` file
    ```conda env create --file conda/environment.yml```
3. Activate the conda environment:
    ```conda activate py310_icsgenerator```
4. Run the Python script:
    ```cd app
    python script.py```
5. After the script completes, the generated `calendar.ics` file and `log.txt` file will be in the output folder.

## Cleaning Up
### Removing the Docker Image and Container
To delete the Docker image and container, run:
    ```docker-compose down
    docker rmi ics-generator-python```

### Removing the conda environment
To remove the conda environment after running the project:
    ```conda remove --name py310_icsgenerator --all```

## Acknowledgements
- [icalendar](https://pypi.org/project/icalendar/)
- [python-dateutil](https://pypi.org/project/python-dateutil/)

## Contact
Please feel free 