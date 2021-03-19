from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import date
from datetime import datetime
import base64
import io
import traceback


class CsvFile:

    def __init__(self, file):
        self.file = file
        self.plot_all()

    def make_float(self, x):
        return float(x.replace(',', '.'))

    def pre_processing(self):
        try:
            data = self.file.decode('utf-8')
            df = pd.read_csv(StringIO(data))
            df.columns = ['datetime', 'kWh']

            df['datetime'] = pd.to_datetime(df['datetime'], format='%d/%m/%Y %H:%M')

            df = df[~df.index.duplicated(keep='first')]

            df["kWh"] = df['kWh'].apply(self.make_float)
            return df
        except Exception as e:
            traceback.print_exc()

    def detect_anomaly(self, x, q1, q3):
        try:
            return 1 if x > q3 or x < q1 else 0
        except Exception as e:
            traceback.print_exc()

    def detect_week_days_working_hours(self):
        try:
            df_week_day = self.pre_processing()

            df_week_day['week_day'] = df_week_day['datetime'].dt.strftime("%w")
            df_week_day['hour'] = df_week_day['datetime'].dt.strftime("%H")
            df_week_day['hour'] = df_week_day['hour'].astype(int)

            df_week_day = df_week_day.drop(
                df_week_day[(df_week_day['week_day'] == str(6)) | (df_week_day['week_day'] == str(7))].index)
            df_week_day = df_week_day.drop(df_week_day[(df_week_day['hour'] > 18)].index)
            df_week_day = df_week_day.drop(df_week_day[(df_week_day['hour'] < 9)].index)

            df_week_day.index = df_week_day['datetime']
            df_week_day = df_week_day.drop("datetime", axis=1)
            df_week_day = df_week_day.drop("week_day", axis=1)
            df_week_day = df_week_day.drop("hour", axis=1)

            df_week_day['is_anomaly'] = df_week_day['kWh']
            if df_week_day['kWh'].any():

                q1, q3 = np.percentile(df_week_day['kWh'], [2, 98
                                                            ])

                df_week_day["is_anomaly"] = df_week_day['is_anomaly'].apply(self.detect_anomaly, args=(q1, q3))

                fig, ax = plt.subplots()
                plt.rcParams['figure.figsize'] = [15, 10]
                ax.set_xlabel('Date-Time')
                ax.set_ylabel('kWh')
                plotdf_week_day = df_week_day.reset_index()
                obj_week_days = []
                ax.plot(plotdf_week_day['datetime'], plotdf_week_day['kWh'], alpha=0.7)

                for index, row in plotdf_week_day.iterrows():
                    if int(row['is_anomaly']):
                        obj_week_days.append({"datetime": row['datetime'], "kWh": row['kWh']})
                        ax.scatter(row['datetime'], row['kWh'], color='red')

                return obj_week_days
            else:
                return []
        except Exception as e:
            traceback.print_exc()

    def detect_weekends(self):
        try:
            df_weekend = self.pre_processing()

            df_weekend['week_day'] = df_weekend['datetime'].dt.strftime("%w")

            df_weekend = df_weekend.drop(
                df_weekend[~(df_weekend['week_day'] == str(6)) | (df_weekend['week_day'] == str(7))].index)
            df_weekend.index = df_weekend['datetime']
            df_weekend = df_weekend.drop("datetime", axis=1)
            df_weekend = df_weekend.drop("week_day", axis=1)

            df_weekend['is_anomaly'] = df_weekend['kWh']
            if df_weekend['kWh'].any():

                q1, q3 = np.percentile(df_weekend['kWh'], [2, 98])

                df_weekend["is_anomaly"] = df_weekend['is_anomaly'].apply(self.detect_anomaly, args=(q1, q3))

                fig, ax = plt.subplots()
                plt.rcParams['figure.figsize'] = [15, 10]  # plot size width and height
                ax.set_xlabel('Date-Time')
                ax.set_ylabel('kWh')
                plotdf_weekend = df_weekend.reset_index()

                obj_weekend = []
                ax.plot(plotdf_weekend['datetime'], plotdf_weekend['kWh'], alpha=0.7)
                for index, row in plotdf_weekend.iterrows():
                    if int(row['is_anomaly']):
                        obj_weekend.append({"datetime": row['datetime'], "kWh": row['kWh']})
                        ax.scatter(row['datetime'], row['kWh'], color='red')

                return obj_weekend
            else:
                return []
        except Exception as e:
            traceback.print_exc()

    def detect_week_days_non_working_hours(self):
        try:
            df_non_working_hours = self.pre_processing()

            df_non_working_hours['week_day'] = df_non_working_hours['datetime'].dt.strftime("%w")
            df_non_working_hours['hour'] = df_non_working_hours['datetime'].dt.strftime("%H")
            df_non_working_hours['hour'] = df_non_working_hours['hour'].astype(int)

            df_non_working_hours = df_non_working_hours.drop(df_non_working_hours[
                                                                 (df_non_working_hours['week_day'] == str(6)) | (
                                                                         df_non_working_hours['week_day'] == str(
                                                                     7))].index)
            df_non_working_hours = df_non_working_hours.drop(
                df_non_working_hours[(df_non_working_hours['hour'] < 18) & (df_non_working_hours['hour'] > 9)].index)

            df_non_working_hours.index = df_non_working_hours['datetime']
            df_non_working_hours = df_non_working_hours.drop("datetime", axis=1)
            df_non_working_hours = df_non_working_hours.drop("week_day", axis=1)
            df_non_working_hours = df_non_working_hours.drop("hour", axis=1)

            df_non_working_hours['is_anomaly'] = df_non_working_hours['kWh']
            if df_non_working_hours['kWh'].any():

                q1, q3 = np.percentile(df_non_working_hours['kWh'], [2, 98])

                df_non_working_hours["is_anomaly"] = df_non_working_hours['is_anomaly'].apply(self.detect_anomaly,
                                                                                              args=(q1, q3))

                fig, ax = plt.subplots()
                plt.rcParams['figure.figsize'] = [15, 10]  # plot size width and height
                ax.set_xlabel('Date-Time')
                ax.set_ylabel('kWh')
                plotdf_non_working_hours = df_non_working_hours.reset_index()

                obj_no_working_hours = []
                ax.plot(plotdf_non_working_hours['datetime'], plotdf_non_working_hours['kWh'], alpha=0.7)

                for index, row in plotdf_non_working_hours.iterrows():
                    if int(row['is_anomaly']):
                        obj_no_working_hours.append({"datetime": row['datetime'], "kWh": row['kWh']})
                        ax.scatter(row['datetime'], row['kWh'], color='red')
                return obj_no_working_hours
            else:
                return []
        except Exception as e:
            traceback.print_exc()

    def plot_all(self):
        try:
            df = self.pre_processing()
            self.all_data = self.detect_week_days_non_working_hours() + \
                            self.detect_week_days_working_hours() + \
                            self.detect_weekends()
            fig, ax = plt.subplots()
            plt.rcParams['figure.figsize'] = [55, 40]  # plot size width and height
            ax.set_xlabel('Date-Time')
            ax.set_ylabel('kWh')
            ax.plot(df['datetime'], df['kWh'], alpha=0.7)

            for row in self.all_data:
                ax.scatter(row['datetime'], row['kWh'], color='red')

            pic_IObytes = io.BytesIO()
            plt.savefig(pic_IObytes, format='png')
            pic_IObytes.seek(0)
            self.pic_hash = base64.b64encode(pic_IObytes.read()).decode("utf-8")
        except Exception as e:
            traceback.print_exc()


def handle_json(data):
    new_data = data
    for i, j in enumerate(data):
        new_data[i]['datetime'] = j['datetime'].to_pydatetime().strftime("%Y %B %A %H:%M:%S")
    return new_data
