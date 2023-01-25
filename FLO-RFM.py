#FLO_RFM ANalizi


import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

#Adım1: flo_data_20K.csv verisini okuyunuz.Dataframe’in kopyasını oluşturunuz.
df_ = pd.read_csv("FLO_RFM_Analizi/flo_data_20k.csv")
df = df_.copy()

#Adım2: Veri setinde
#a. İlk 10 gözlem,
#b. Değişken isimleri,
#c. Betimsel istatistik,
#d. Boş değer,
#e. Değişken tipleri, incelemesi yapınız.

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

#Adım3: Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Her bir müşterinin toplam
#alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.
df.info()
df["omni_channel_count"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["omni_channel_sum"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]

#Adım4: Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.

date_change = df.columns[df.columns.str.contains("date")]
df[date_change] = df[date_change].apply(pd.to_datetime)
df.info()

#diğer bir çözüm
datetime = ["first_order_date", "last_order_date", "last_order_date_online", "last_order_date_offline"]
df[datetime] = df[datetime].apply(pd.to_datetime)

#Adım5: Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısının ve toplam harcamaların dağılımına bakınız.

df.groupby("order_channel").agg({"master_id": "count",
                                 "omni_channel_count": "count",
                                 "omni_channel_sum": "sum"}).head()

#Adım6: En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.

df.groupby("master_id").agg({"omni_channel_sum": "sum"}).sort_values("omni_channel_sum", ascending=False).head(10)

#Adım7: En fazla siparişi veren ilk 10 müşteriyi sıralayınız.

df.groupby("master_id").agg({"omni_channel_count": "sum"}).sort_values("omni_channel_count", ascending=False).head(10)

#Adım8: Veri ön hazırlık sürecini fonksiyonlaştırınız.


def flo_data(df):
    check_df(df)
    #online offline sipariş sayısı ve tutarı
    df["omni_channel_count"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    df["omni_channel_sum"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]
    #değişkenleri time çevirme
    date_change = df.columns[df.columns.str.contains("date")]
    df[date_change] = df[date_change].apply(pd.to_datetime)
    df.info()
    return df


df = df_.copy()

flo_data(df)


#Görev 2: RFM Metriklerinin Hesaplanması
#Adım1:
#Recency(Yenilik) :  Müşterinin en son ne zaman alışveriş yaptığını ifade eder.
#Frequency(Sıklık) : Müşterinin toplam yaptığı alışveri sayısıdır. İşlem sayısı, İşlem sıklığı anlamında kullanılabilir.
#Monetary(Parasal Değer) : Müşterinin bıraktığı parasal değeri ifade eder.

#Adım 2, 3 ve 4

df["last_order_date"].max()
today_date = dt.datetime(2021, 6, 1)
type(today_date)
#2günü daha farklı bir şekilde eklemek istersek
#pd.DateOffset(days=2)

rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (today_date - df["last_order_date"]).astype('timedelta64[D]')
rfm["frequency"] = df["omni_channel_count"]
rfm["monetary"] = df["omni_channel_sum"]

rfm.head()

#Görev 3: RF Skorunun Hesaplanması

#Adım 1 ve 2 : Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.

rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
rfm.head()

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])


#Adım 3: recency_score ve frequency_score’u tek bir değişken olarak ifade ediniz ve RF_SCORE olarak kaydediniz.

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm.head()

#Görev 4: RF Skorunun Segment Olarak Tanımlanması

#Adım 1: Oluşturulan RF skorları için segment tanımlamaları yapınız.
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

#Adım 2: Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz.

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

#Görev 5: Aksiyon Zamanı !

#Adım1: Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean"])

#Adım2: Adım2: RFM analizi yardımıyla aşağıda verilen 2 case için ilgili
# profildeki müşterileri bulun ve müşteri id'lerini csv olarak kaydediniz.

# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri
# tercihlerinin üstünde. Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak
# iletişime geçmek isteniliyor. Sadık müşterilerinden(champions, loyal_customers) ve kadın kategorisinden alışveriş
# yapan kişiler özel olarak iletişim kurulacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına kaydediniz.

target_segments = rfm[rfm["segment"].isin(["champions", "loyal_customers"])]["customer_id"]
tar_cust = df[(df["master_id"].isin(target_segments)) & (df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
tar_cust.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)
tar_cust.shape
tar_cust.head()

#b. Erkek ve Çocuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte
#iyi müşteri olan ama uzun süredir alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni
#gelen müşteriler özel olarak hedef alınmak isteniyor. Uygun profildeki müşterilerin id'lerini csv dosyasına kaydediniz.

target_segments = rfm[rfm["segment"].isin(["cant_loose", "hibernating","new_customers"])]["customer_id"]
tar_cust = df[(df["master_id"].isin(target_segments)) & ((df["interested_in_categories_12"].str.contains("ERKEK")) |
                                                         (df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
tar_cust.to_csv("indirim_hedef_müşteri_ids.csv", index=False)

tar_cust.shape
tar_cust.head()


rfm["segment"].value_counts()
