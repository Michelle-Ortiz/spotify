import webbrowser
from datetime import timedelta, date
import time
import pandas 
from pathlib import Path

def del_file(f):
    """Deletes file from folder.
    Args:
        f (pathlib.Path): location of file.
    """
    f.unlink()

#date code i copied
def daterange(start_date, end_date):
    """Date range generator.
    Args:
        start_date (datetime.date): starting date.
        end_date (datetime.date): end date.
    Yields:
        datetime.date: current date in iterator.
    """
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def build_csv_paths(csv_url_base, download_const, csv_name_base, csv_suffix, old_path, new_date):
    csv_url = f'{csv_url_base}{new_date}{download_const}'
    csv_name = f'{csv_name_base}{new_date}{csv_suffix}'
    old_csv_path = old_path/csv_name
    return csv_url,old_csv_path

def get_spotify_charts(csv_url_base, download_const, csv_name_base, csv_suffix, old_path, start_date, end_date):
    """Downloads all spotify top 200 charts. Reads into single list.

    Args:
        csv_url_base ([type]): [description]
        download_const ([type]): [description]
        csv_name_base ([type]): [description]
        csv_suffix ([type]): [description]
        old_path ([type]): [description]
        start_date ([type]): [description]
        end_date ([type]): [description]

    Returns:
        list: collection of charts.
    """
    tables = []
    for single_date in daterange(start_date, end_date):
        #setting date
        new_date = (single_date.strftime('%Y-%m-%d'))
        csv_url, old_csv_path = build_csv_paths(csv_url_base, download_const, csv_name_base, csv_suffix, old_path, new_date)
        #downloading csv
        webbrowser.open(csv_url)
        #moving csv to specified path
        while not old_csv_path.exists():
            time.sleep(1)
        #editing csv to rename columns and add date column, only top 50
        spotify_single_date_df = pandas.read_csv(old_csv_path, header=1, skiprows=0, nrows=50)
        #remove downloaded csv
        del_file(old_csv_path)
        spotify_single_date_df['Date'] = new_date
        tables.append(spotify_single_date_df)
    return tables

def main():
    """Downloads spotify charts and combines them into one csv.
    """
    #url of csv 
    csv_url_base = 'https://spotifycharts.com/regional/us/daily/'
    download_const = '/download'
    #name of csv
    csv_name_base = 'regional-us-daily-'
    csv_suffix = '.csv'
    #where it originally gets downloaded
    old_path = Path('C:/Users/miche/Downloads/')
    #where i want to move it
    new_path = Path('C:/Users/miche/OneDrive/Desktop/folder/github-repos/spotify/csv-files/')
    #super csv name
    csv_super_name = f'super{csv_suffix}'
    #start and end
    start_date = date(2020, 1, 1)
    end_date = date(2021, 1, 1)

    tables = get_spotify_charts(csv_url_base, download_const, csv_name_base, csv_suffix, old_path, start_date, end_date)
    super_table = pandas.concat(tables, axis=0)
    super_table.to_csv(new_path/csv_super_name, index=False)

if __name__ == "__main__":
    main()