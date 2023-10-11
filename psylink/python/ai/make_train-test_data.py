
class PsylinkMediapipeDataset(Dataset):
    def __init__(self, psylink_csv, mp_csv, transform = None):
        self.landmarks_frame = pd.read_csv(mp_csv)
        self.data_frame = pd.read_csv(psylink_csv)
        
def get_training_data
