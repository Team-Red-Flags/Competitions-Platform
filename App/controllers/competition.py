from App.database import db
from App.models import Competition
from datetime import date

def create_competition(name: str, description: str, start_date: str = None, end_date: str = None) -> Competition:
    new_competition = Competition(
        name=name, 
        description=description, 
        start_date=get_date_from_string(start_date), 
        end_date=get_date_from_string(end_date)
    )
    db.session.add(new_competition)
    db.session.commit()
    print("Created competition:", new_competition)
    return new_competition

def get_date_from_string(date_string: str) -> date:
    """Parse a date string of form 'dd-mm-yyyy', 'dd/mm/yyyy' or 'd Month, yyyy' into a date object

    Args:
        date_string (str): The input date string to convert to date object

    Raises:
        ValueError: Incorrect value parameter in string format

    Returns:
        date: The converted date
    """
    if '-' in date_string:
        year, month, day = date_string.split('-')
        if len(year) < 4: 
            raise ValueError('Unrecognised year in date string must be 4 digits. Received: ' + date_string)
        if len(month) > 2 and int(month) > 12 and int(month) < 1: 
            raise ValueError('Invalid month value for date format dd-mm-yyyy. Received: ' + date_string)
        if len(day) > 2 and int(day) > 31 and int(day) < 1: 
            raise ValueError('Invalid day value for date format dd-mm-yyyy. Received: ' + date_string)
        return date(int(year), int(month), int(day))
    
    if '/' in date_string:
        year, month, day = date_string.split('/')
        if len(year) < 4: 
            raise ValueError('Unrecognised year in date string must be 4 digits. Received: ' + date_string)
        if len(month) > 2 and int(month) > 12 and int(month) < 1: 
            raise ValueError('Invalid month value for date format dd/mm/yyyy. Received: ' + date_string)
        if len(day) > 2 and int(day) > 31 and int(day) < 1: 
            raise ValueError('Invalid day value for date format dd/mm/yyyy. Received: ' + date_string)
        return date(int(year), int(month), int(day))
    
    day, month, year = date_string.split(" ")
    month = month.split(",")[0].lower()
    if month in ['jan', 'january']:   month = 1
    if month in ['feb', 'february']:  month = 2
    if month in ['mar', 'march']:     month = 3
    if month in ['apr', 'april']:     month = 4
    if month in ['may']:              month = 5
    if month in ['jun', 'june']:      month = 6
    if month in ['jul', 'july']:      month = 7
    if month in ['aug', 'august']:    month = 8
    if month in ['sep', 'september']: month = 9
    if month in ['oct', 'october']:   month = 10
    if month in ['nov', 'november']:  month = 11
    if month in ['dec', 'december']:  month = 12
    return date(int(year), int(month), int(day))

def get_competition(id) -> Competition:
    return Competition.query.get(id)

def get_all_competitions() -> list:
    return Competition.query.all()

