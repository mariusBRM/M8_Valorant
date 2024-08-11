import os

class Config:

    # set the base directory to from where it is called
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    SAVE_RAW_PATH = os.path.join(BASE_DIR, '..', 'data', 'raw')
    SAVE_PROCESSED_PATH = os.path.join(BASE_DIR, '..', 'data', 'processed')
    SAVE_FINAL_DATASET_PATH = os.path.join(BASE_DIR, '..', 'data', 'dataset')

    SAVE_IMAGES_PATH = os.path.join(BASE_DIR, '..', 'data', 'images')

    GENERAL_DATA = 'general_data'
    ECONOMY_DATA = 'economy_data'
    PERFORMANCE_DATA = 'performance_data'
    PICK_BAN_DATA = 'pick_ban_data'

    UNDERSCORE = '_'
    SLASH = '\\'
    CSV = '.csv'

    URLS = {
        'kickoff pacific' : 'https://www.vlr.gg/event/matches/1924/champions-tour-2024-pacific-kickoff/?series_id=all',
        'kickoff emea' : 'https://www.vlr.gg/event/matches/1925/champions-tour-2024-emea-kickoff/?series_id=all',
        'kickoff americas' : 'https://www.vlr.gg/event/matches/1923/champions-tour-2024-americas-kickoff/?series_id=all',
        'master madrid': 'https://www.vlr.gg/event/matches/1921/champions-tour-2024-masters-madrid/?series_id=all',
        'stage 1 pacific' : 'https://www.vlr.gg/event/matches/2002/champions-tour-2024-pacific-stage-1/?series_id=all',
        'stage 1 emea' : 'https://www.vlr.gg/event/matches/1998/champions-tour-2024-emea-stage-1/?series_id=all',
        'stage 1 americas' : 'https://www.vlr.gg/event/matches/2004/champions-tour-2024-americas-stage-1/?series_id=all'
    }

    Name_event = {
        'kickoff pacific' : 'champions-tour-2024-pacific-kickoff',
        'kickoff emea' : 'champions-tour-2024-emea-kickoff',
        'kickoff americas' : 'champions-tour-2024-americas-kickoff',
        'master madrid': 'champions-tour-2024-masters-madrid',
        'stage 1 pacific' : 'champions-tour-2024-pacific-stage-1',
        'stage 1 emea' : 'champions-tour-2024-emea-stage-1',
        'stage 1 americas' : 'champions-tour-2024-americas-stage-1'
    }

    def load_data(self, name_event, type_of_data):
        """ Make sure to target the endpoint in raw data"""    
        if name_event in self.Name_event:
            event_name = self.Name_event[name_event]
            path = os.path.join(
                self.SAVE_RAW_PATH,
                f"{event_name}_data",
                f"{type_of_data}{self.UNDERSCORE}{event_name}{self.CSV}"
            )
            return path
        else:
            raise ValueError(f"Event name '{name_event}' is not recognized.")