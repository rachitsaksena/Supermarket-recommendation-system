import pandas as pd
import numpy as np
import turicreate as tc


def create_data_dummy(data_in):
    data_dummy_in = data_in.copy()
    data_dummy_in['purchase_dummy'] = 1
    return data_dummy_in


def main():
    transactions = pd.read_csv('trx_data.csv')  # replace "trx_data.csv" with the transaction data file

    transactions['products'] = transactions['products'].apply(lambda x: [int(i) for i in x.split('|')])

    data = pd.melt(transactions.set_index('customerId')['products'].apply(pd.Series).reset_index(),
                   id_vars=['customerId'],
                   value_name='products') \
        .dropna().drop(['variable'], axis=1) \
        .groupby(['customerId', 'products']) \
        .agg({'products': 'count'}) \
        .rename(columns={'products': 'purchase_count'}) \
        .reset_index() \
        .rename(columns={'products': 'productId'})
    data['productId'] = data['productId'].astype(np.int64)

    data_dummy = create_data_dummy(data)

    model = tc.item_similarity_recommender.create(data_dummy,
                                                  user_id='customerId',
                                                  item_id='productId',
                                                  target='purchase_dummy',
                                                  similarity_type='cosine')

    return model
