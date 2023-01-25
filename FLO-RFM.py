#FLO_RFM 

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

df_ = pd.read_csv("FLO_RFM_Analizi/flo_data_20k.csv")
df = df_.copy()

def check_df(dataframe, head=10):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


check_df(df, head=10)

# the total number of purchases by each customer.
df.info()
df["omni_channel_count"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["omni_channel_sum"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]

#Variables containing dates are converted to date.
date_change = df.columns[df.columns.str.contains("date")]
df[date_change] = df[date_change].apply(pd.to_datetime)
df.info()

# a different solution
datetime = ["first_order_date", "last_order_date", "last_order_date_online", "last_order_date_offline"]
df[datetime] = df[datetime].apply(pd.to_datetime)

# look at the relevant distributions

df.groupby("order_channel").agg({"master_id": "count",
                                 "omni_channel_count": "count",
                                 "omni_channel_sum": "sum"}).head()

# Top 10 highest earning customers.

df.groupby("master_id").agg({"omni_channel_sum": "sum"}).sort_values("omni_channel_sum", ascending=False).head(10)

#Top 10 customers with the most orders.

df.groupby("master_id").agg({"omni_channel_count": "sum"}).sort_values("omni_channel_count", ascending=False).head(10)

#Functionalization of data preparation process.


def flo_data(df):
    check_df(df)
    df["omni_channel_count"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    df["omni_channel_sum"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]
    date_change = df.columns[df.columns.str.contains("date")]
    df[date_change] = df[date_change].apply(pd.to_datetime)
    df.info()
    return df


df = df_.copy()

flo_data(df)

#Calculation of RFM metrics.

df["last_order_date"].max()
today_date = dt.datetime(2021, 6, 1)
type(today_date)

rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (today_date - df["last_order_date"]).astype('timedelta64[D]')
rfm["frequency"] = df["omni_channel_count"]
rfm["monetary"] = df["omni_channel_sum"]

rfm.head()

#Calculation of RF Score

rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
rfm.head()

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])


rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm.head()

#Definition of RF Score as Segments.
#Segment definitions.
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

#Converting scores into segments with the help of seg_map.

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

#Examine the recency, frequency and monetary averages of the segments.

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean"])

#Creation of desired csv files.
target_segments = rfm[rfm["segment"].isin(["champions", "loyal_customers"])]["customer_id"]
tar_cust = df[(df["master_id"].isin(target_segments)) & (df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
tar_cust.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)
tar_cust.shape
tar_cust.head()


target_segments = rfm[rfm["segment"].isin(["cant_loose", "hibernating","new_customers"])]["customer_id"]
tar_cust = df[(df["master_id"].isin(target_segments)) & ((df["interested_in_categories_12"].str.contains("ERKEK")) |
                                                         (df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
tar_cust.to_csv("indirim_hedef_müşteri_ids.csv", index=False)

tar_cust.shape
tar_cust.head()

rfm["segment"].value_counts()
