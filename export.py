import pandas as pd

class ExportData:
    def __init__(self):
        pass

    def export_to_csv(self, data, file_name):
        df = pd.DataFrame(data)
        df.to_csv(f'output/{file_name}.csv', index=False)
