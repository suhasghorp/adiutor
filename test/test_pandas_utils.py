import datetime as dt
import os
import tempfile
import unittest
import zipfile

import pandas as pd

import thalesians.adiutor.pandas_utils as pandas_utils

class TestPandasUtils(unittest.TestCase):
    def test_read_csv(self):
        content = \
"""
2020-09-09 09:16:00,21.0785,21.0785,21.0785,21.0785,237
2020-09-09 11:55:00,21.0785,21.0785,21.0785,21.0785,130
2020-09-09 11:56:00,21.0824,21.0824,21.0824,21.0824,119
2020-09-09 12:04:00,21.0869,21.0945,21.0869,21.0945,617
2020-09-09 12:10:00,21.0869,21.0869,21.0869,21.0869,398
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(content)
            f.flush()
        try:
            df = pandas_utils.read_csv(f.name, header=None, names=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            self.assertEqual(len(df), 5)
            self.assertEqual(df.columns.tolist(), ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            self.assertEqual(df['Time'].iloc[0], '2020-09-09 09:16:00')
            self.assertEqual(df['Time'].iloc[1], '2020-09-09 11:55:00')
            self.assertEqual(df['Time'].iloc[2], '2020-09-09 11:56:00')
            self.assertEqual(df['Time'].iloc[3], '2020-09-09 12:04:00')
            self.assertEqual(df['Time'].iloc[4], '2020-09-09 12:10:00')
            self.assertEqual(df['Open'].tolist(), [21.0785, 21.0785, 21.0824, 21.0869, 21.0869])
            self.assertEqual(df['High'].tolist(), [21.0785, 21.0785, 21.0824, 21.0945, 21.0869])
            self.assertEqual(df['Low'].tolist(), [21.0785, 21.0785, 21.0824, 21.0869, 21.0869])
            self.assertEqual(df['Close'].tolist(), [21.0785, 21.0785, 21.0824, 21.0945, 21.0869])
            self.assertEqual(df['Volume'].tolist(), [237, 130, 119, 617, 398])
        finally:
            os.remove(f.name)
        
    def test_read_csv_from_zip_file(self):
        content = \
"""
2020-09-09 09:16:00,21.0785,21.0785,21.0785,21.0785,237
2020-09-09 11:55:00,21.0785,21.0785,21.0785,21.0785,130
2020-09-09 11:56:00,21.0824,21.0824,21.0824,21.0824,119
2020-09-09 12:04:00,21.0869,21.0945,21.0869,21.0945,617
2020-09-09 12:10:00,21.0869,21.0869,21.0869,21.0869,398
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(content)
            f.flush()
        zipfile.ZipFile(f.name + '.zip', 'w').write(f.name, os.path.basename(f.name))
        os.remove(f.name)
        try:
            df = pandas_utils.read_csv(path_to_archive=f.name + '.zip', path=os.path.basename(f.name), header=None, names=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            self.assertEqual(len(df), 5)
            self.assertEqual(df.columns.tolist(), ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            self.assertEqual(df['Time'].iloc[0], '2020-09-09 09:16:00')
            self.assertEqual(df['Time'].iloc[1], '2020-09-09 11:55:00')
            self.assertEqual(df['Time'].iloc[2], '2020-09-09 11:56:00')
            self.assertEqual(df['Time'].iloc[3], '2020-09-09 12:04:00')
            self.assertEqual(df['Time'].iloc[4], '2020-09-09 12:10:00')
            self.assertEqual(df['Open'].tolist(), [21.0785, 21.0785, 21.0824, 21.0869, 21.0869])
            self.assertEqual(df['High'].tolist(), [21.0785, 21.0785, 21.0824, 21.0945, 21.0869])
            self.assertEqual(df['Low'].tolist(), [21.0785, 21.0785, 21.0824, 21.0869, 21.0869])
            self.assertEqual(df['Close'].tolist(), [21.0785, 21.0785, 21.0824, 21.0945, 21.0869])
            self.assertEqual(df['Volume'].tolist(), [237, 130, 119, 617, 398])
        finally:
            os.remove(f.name + '.zip')
                    
    def test_read_parquet(self):
        df = pd.DataFrame({
            'Time': [dt.datetime(2020, 9, 9, 9, 16), dt.datetime(2020, 9, 9, 11, 55), dt.datetime(2020, 9, 9, 11, 56), dt.datetime(2020, 9, 9, 12, 4), dt.datetime(2020, 9, 9, 12, 10)],
            'Open': [21.0785, 21.0785, 21.0824, 21.0869, 21.0869],
            'High': [21.0785, 21.0785, 21.0824, 21.0945, 21.0869],
            'Low': [21.0785, 21.0785, 21.0824, 21.0869, 21.0869],
            'Close': [21.0785, 21.0785, 21.0824, 21.0945, 21.0869],
            'Volume': [237, 130, 119, 617, 398],
            })
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            pass
        try:
            df.to_parquet(f.name)
            zipfile.ZipFile(f.name + '.zip', 'w').write(f.name, os.path.basename(f.name))
            os.remove(f.name)
            df = pandas_utils.read_parquet(path_to_archive=f.name + '.zip', path=os.path.basename(f.name))
            self.assertEqual(len(df), 5)
            self.assertEqual(df.columns.tolist(), ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            self.assertEqual(df['Time'].iloc[0], dt.datetime(2020, 9, 9, 9, 16))
            self.assertEqual(df['Time'].iloc[1], dt.datetime(2020, 9, 9, 11, 55))
            self.assertEqual(df['Time'].iloc[2], dt.datetime(2020, 9, 9, 11, 56))
            self.assertEqual(df['Time'].iloc[3], dt.datetime(2020, 9, 9, 12, 4))
            self.assertEqual(df['Time'].iloc[4], dt.datetime(2020, 9, 9, 12, 10))
            self.assertEqual(df['Open'].tolist(), [21.0785, 21.0785, 21.0824, 21.0869, 21.0869])
            self.assertEqual(df['High'].tolist(), [21.0785, 21.0785, 21.0824, 21.0945, 21.0869])
            self.assertEqual(df['Low'].tolist(), [21.0785, 21.0785, 21.0824, 21.0869, 21.0869])
            self.assertEqual(df['Close'].tolist(), [21.0785, 21.0785, 21.0824, 21.0945, 21.0869])
            self.assertEqual(df['Volume'].tolist(), [237, 130, 119, 617, 398])
        finally:
            os.remove(f.name + '.zip')
    
    def test_read_parquet_from_zip_file(self):
        df = pd.DataFrame({
            'Time': [dt.datetime(2020, 9, 9, 9, 16), dt.datetime(2020, 9, 9, 11, 55), dt.datetime(2020, 9, 9, 11, 56), dt.datetime(2020, 9, 9, 12, 4), dt.datetime(2020, 9, 9, 12, 10)],
            'Open': [21.0785, 21.0785, 21.0824, 21.0869, 21.0869],
            'High': [21.0785, 21.0785, 21.0824, 21.0945, 21.0869],
            'Low': [21.0785, 21.0785, 21.0824, 21.0869, 21.0869],
            'Close': [21.0785, 21.0785, 21.0824, 21.0945, 21.0869],
            'Volume': [237, 130, 119, 617, 398],
            })
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            pass
        try:
            df.to_parquet(f.name)
            df = pandas_utils.read_parquet(f.name)
            self.assertEqual(len(df), 5)
            self.assertEqual(df.columns.tolist(), ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            self.assertEqual(df['Time'].iloc[0], dt.datetime(2020, 9, 9, 9, 16))
            self.assertEqual(df['Time'].iloc[1], dt.datetime(2020, 9, 9, 11, 55))
            self.assertEqual(df['Time'].iloc[2], dt.datetime(2020, 9, 9, 11, 56))
            self.assertEqual(df['Time'].iloc[3], dt.datetime(2020, 9, 9, 12, 4))
            self.assertEqual(df['Time'].iloc[4], dt.datetime(2020, 9, 9, 12, 10))
            self.assertEqual(df['Open'].tolist(), [21.0785, 21.0785, 21.0824, 21.0869, 21.0869])
            self.assertEqual(df['High'].tolist(), [21.0785, 21.0785, 21.0824, 21.0945, 21.0869])
            self.assertEqual(df['Low'].tolist(), [21.0785, 21.0785, 21.0824, 21.0869, 21.0869])
            self.assertEqual(df['Close'].tolist(), [21.0785, 21.0785, 21.0824, 21.0945, 21.0869])
            self.assertEqual(df['Volume'].tolist(), [237, 130, 119, 617, 398])
        finally:
            os.remove(f.name)
        
    def test_augment_column_names(self):
        df = pd.DataFrame({
            'Time': [dt.datetime(2020, 9, 9, 9, 16), dt.datetime(2020, 9, 9, 11, 55), dt.datetime(2020, 9, 9, 11, 56), dt.datetime(2020, 9, 9, 12, 4), dt.datetime(2020, 9, 9, 12, 10)],
            'Open': [21.0785, 21.0785, 21.0824, 21.0869, 21.0869],
            'High': [21.0785, 21.0785, 21.0824, 21.0945, 21.0869],
            'Low': [21.0785, 21.0785, 21.0824, 21.0869, 21.0869],
            'Close': [21.0785, 21.0785, 21.0824, 21.0945, 21.0869],
            'Volume': [237, 130, 119, 617, 398],
            })
        df = pandas_utils.augment_column_names(df, prefix='AAA_')
        self.assertEqual(df.columns.tolist(), ['AAA_Time', 'AAA_Open', 'AAA_High', 'AAA_Low', 'AAA_Close', 'AAA_Volume'])
        self.assertEqual(df['AAA_Open'].tolist(), [21.0785, 21.0785, 21.0824, 21.0869, 21.0869])
        self.assertEqual(df['AAA_High'].tolist(), [21.0785, 21.0785, 21.0824, 21.0945, 21.0869])
        self.assertEqual(df['AAA_Low'].tolist(), [21.0785, 21.0785, 21.0824, 21.0869, 21.0869])
        self.assertEqual(df['AAA_Close'].tolist(), [21.0785, 21.0785, 21.0824, 21.0945, 21.0869])
        self.assertEqual(df['AAA_Volume'].tolist(), [237, 130, 119, 617, 398])
        
    def test_index_kind(self):
        self.assertEqual(pandas_utils.IndexKind.INTERSECTION, pandas_utils.IndexKind.INTERSECTION) 
        self.assertEqual(pandas_utils.IndexKind.UNION, pandas_utils.IndexKind.UNION) 
        self.assertEqual(pandas_utils.IndexKind.INDIVIDUAL, pandas_utils.IndexKind.INDIVIDUAL) 
        self.assertEqual(pandas_utils.IndexKind.CUSTOM, pandas_utils.IndexKind.CUSTOM) 

    def test_intersection_index(self):
        df_1 = pd.DataFrame({
            'Time': [dt.datetime(2020, 9, 9, 9, 16), dt.datetime(2020, 9, 9, 11, 55), dt.datetime(2020, 9, 9, 11, 56), dt.datetime(2020, 9, 9, 12, 4), dt.datetime(2020, 9, 9, 12, 10)],
            'Open': [21.0785, 21.0785, 21.0824, 21.0869, 21.0869],
            'High': [21.0785, 21.0785, 21.0824, 21.0945, 21.0869],
            'Low': [21.0785, 21.0785, 21.0824, 21.0869, 21.0869],
            'Close': [21.0785, 21.0785, 21.0824, 21.0945, 21.0869],
            'Volume': [237, 130, 119, 617, 398],
            })
        df_2 = pd.DataFrame({
            'Time': [dt.datetime(2020, 9, 9, 7, 14), dt.datetime(2020, 9, 9, 8, 33), dt.datetime(2020, 9, 9, 9, 4), dt.datetime(2020, 9, 9, 9, 16), dt.datetime(2020, 9, 9, 9, 30), dt.datetime(2020, 9, 9, 9, 31), dt.datetime(2020, 9, 9, 9, 32), dt.datetime(2020, 9, 9, 9, 33), dt.datetime(2020, 9, 9, 9, 34), dt.datetime(2020, 9, 9, 9, 35)],
            'Open': [19.15, 19.24, 19.29, 19.34, 19.37, 19.37, 19.38, 19.38, 19.38, 19.38],
            'High': [19.15, 19.24, 19.29, 19.34, 19.38, 19.37, 19.38, 19.385, 19.38, 19.38],
            'Low': [19.15, 19.24, 19.29, 19.34, 19.36, 19.37, 19.38, 19.38, 19.38, 19.38],
            'Close': [19.15, 19.24, 19.29, 19.34, 19.37, 19.37, 19.38, 19.385, 19.38, 19.38],
            'Volume': [100, 250, 300, 30000, 8098, 13485, 1250, 2250, 1400, 3750],
            })
        df_1 = df_1.set_index('Time').sort_index()
        df_2 = df_2.set_index('Time').sort_index()
        intersection_index = pandas_utils.intersection_index([df_1, df_2])
        self.assertEqual(list(intersection_index), [dt.datetime(2020, 9, 9, 9, 16)])
        self.assertEqual(set(intersection_index), set(df_1.index).intersection(set(df_2.index)))
        self.assertLessEqual(len(intersection_index), len(df_1.index))
        self.assertLessEqual(len(intersection_index), len(df_2.index))

    def test_union_index(self):
        df_1 = pd.DataFrame({
            'Time': [dt.datetime(2020, 9, 9, 11, 55), dt.datetime(2020, 9, 9, 11, 56), dt.datetime(2020, 9, 9, 9, 16), dt.datetime(2020, 9, 9, 12, 4), dt.datetime(2020, 9, 9, 12, 10)],
            'Open': [21.0785, 21.0824, 21.0785, 21.0869, 21.0869],
            'High': [21.0785, 21.0824, 21.0785, 21.0945, 21.0869],
            'Low': [21.0785, 21.0824, 21.0785, 21.0869, 21.0869],
            'Close': [21.0785, 21.0824, 21.0785, 21.0945, 21.0869],
            'Volume': [130, 119, 237, 617, 398],
            })
        df_2 = pd.DataFrame({
            'Time': [dt.datetime(2020, 9, 9, 7, 14), dt.datetime(2020, 9, 9, 8, 33), dt.datetime(2020, 9, 9, 9, 4), dt.datetime(2020, 9, 9, 9, 16), dt.datetime(2020, 9, 9, 9, 30), dt.datetime(2020, 9, 9, 9, 31), dt.datetime(2020, 9, 9, 9, 32), dt.datetime(2020, 9, 9, 9, 33), dt.datetime(2020, 9, 9, 9, 34), dt.datetime(2020, 9, 9, 9, 35)],
            'Open': [19.15, 19.24, 19.29, 19.34, 19.37, 19.37, 19.38, 19.38, 19.38, 19.38],
            'High': [19.15, 19.24, 19.29, 19.34, 19.38, 19.37, 19.38, 19.385, 19.38, 19.38],
            'Low': [19.15, 19.24, 19.29, 19.34, 19.36, 19.37, 19.38, 19.38, 19.38, 19.38],
            'Close': [19.15, 19.24, 19.29, 19.34, 19.37, 19.37, 19.38, 19.385, 19.38, 19.38],
            'Volume': [100, 250, 300, 30000, 8098, 13485, 1250, 2250, 1400, 3750],
            })
        df_1 = df_1.set_index('Time').sort_index()
        df_2 = df_2.set_index('Time').sort_index()
        union_index = pandas_utils.union_index([df_1, df_2])
        self.assertEqual(list(union_index), [dt.datetime(2020, 9, 9, 7, 14), dt.datetime(2020, 9, 9, 8, 33), dt.datetime(2020, 9, 9, 9, 4), dt.datetime(2020, 9, 9, 9, 16), dt.datetime(2020, 9, 9, 9, 30), dt.datetime(2020, 9, 9, 9, 31), dt.datetime(2020, 9, 9, 9, 32), dt.datetime(2020, 9, 9, 9, 33), dt.datetime(2020, 9, 9, 9, 34), dt.datetime(2020, 9, 9, 9, 35), dt.datetime(2020, 9, 9, 11, 55), dt.datetime(2020, 9, 9, 11, 56), dt.datetime(2020, 9, 9, 12, 4), dt.datetime(2020, 9, 9, 12, 10)])
        self.assertEqual(set(union_index), set(df_1.index).union(set(df_2.index)))
        self.assertGreaterEqual(len(union_index), len(df_1.index))
        self.assertGreaterEqual(len(union_index), len(df_2.index))

    def test_align(self):
        df_1 = pd.DataFrame({
            'Time': [dt.datetime(2020, 9, 9, 11, 55), dt.datetime(2020, 9, 9, 11, 56), dt.datetime(2020, 9, 9, 9, 16), dt.datetime(2020, 9, 9, 12, 4), dt.datetime(2020, 9, 9, 12, 10)],
            'Open': [21.0785, 21.0824, 21.0785, 21.0869, 21.0869],
            'High': [21.0785, 21.0824, 21.0785, 21.0945, 21.0869],
            'Low': [21.0785, 21.0824, 21.0785, 21.0869, 21.0869],
            'Close': [21.0785, 21.0824, 21.0785, 21.0945, 21.0869],
            'Volume': [130, 119, 237, 617, 398],
            })
        df_2 = pd.DataFrame({
            'Time': [dt.datetime(2020, 9, 9, 7, 14), dt.datetime(2020, 9, 9, 8, 33), dt.datetime(2020, 9, 9, 9, 4), dt.datetime(2020, 9, 9, 9, 16), dt.datetime(2020, 9, 9, 9, 30), dt.datetime(2020, 9, 9, 9, 31), dt.datetime(2020, 9, 9, 9, 32), dt.datetime(2020, 9, 9, 9, 33), dt.datetime(2020, 9, 9, 9, 34), dt.datetime(2020, 9, 9, 9, 35)],
            'Open': [19.15, 19.24, 19.29, 19.34, 19.37, 19.37, 19.38, 19.38, 19.38, 19.38],
            'High': [19.15, 19.24, 19.29, 19.34, 19.38, 19.37, 19.38, 19.385, 19.38, 19.38],
            'Low': [19.15, 19.24, 19.29, 19.34, 19.36, 19.37, 19.38, 19.38, 19.38, 19.38],
            'Close': [19.15, 19.24, 19.29, 19.34, 19.37, 19.37, 19.38, 19.385, 19.38, 19.38],
            'Volume': [100, 250, 300, 30000, 8098, 13485, 1250, 2250, 1400, 3750],
            })
        
        df = pandas_utils.align([df_1, df_2], index=pandas_utils.IndexKind.INTERSECTION)
        self.assertEqual(sorted(set(df.index)), sorted(set(df_1.index).intersection(set(df_2.index))))

        df = pandas_utils.align([df_1, df_2], index=pandas_utils.IndexKind.UNION)
        self.assertEqual(sorted(set(df.index)), sorted(set(df_1.index).union(set(df_2.index))))
        
        df = pandas_utils.align([df_1, df_2], index=0)
        self.assertEqual(list(df.index), list(df_1.index))

        df = pandas_utils.align([df_1, df_2], index=1)
        self.assertEqual(list(df.index), list(df_2.index))

if __name__ == '__main__':
    unittest.main()
    