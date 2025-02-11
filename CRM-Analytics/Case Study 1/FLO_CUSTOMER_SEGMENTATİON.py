import pandas as pd
import numpy as np
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

###################### TASK 1 ##################################
# VERİYİ ANLAMA VE ANALİZ
################################################################

# Adım 1: flo_data_20K.csv verisini okuyunuz.Dataframe’in kopyasını oluşturunuz.
df_ = pd.read_csv("C:/Users/Monster/Desktop/MIUUL/CASE STUDY/CRM/flo_data_20k.csv")
df = df_.copy()

#  Adım 2: Veri setinde
# a. İlk 10 gözlem,
# b. Değişken isimleri,
# c. Boyut
# c. Betimsel istatistik,
# d. Boş değer,
# e. Değişken tipleri, incelemesi yapınız

df.head(10)
df.columns
df.shape
df.describe().T
df.isnull().sum()
df.info()

# Adım 3: Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir.
# Her bir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.
df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]
df.head()


# Adım 4: Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
df.info()
date_columns = [col for col in df.columns if "date" in col]
df[date_columns] = df[date_columns].apply(pd.to_datetime)



# Adım 5: Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısının ve toplam harcamaların dağılımına bakınız.
df.groupby("order_channel").agg({"master_id": "count",
                                 "order_num_total": "sum",
                                 "customer_value_total": "sum",})

# Adım 6: En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
df.sort_values("customer_value_total", ascending=False).head(10)

# Adım 7: En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
df.sort_values("order_num_total", ascending=False).head(10)

# Adım 8: Veri ön hazırlık sürecini fonksiyonlaştırınız.
def data_prep(dataframe):
    df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    df["customer_value_total"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]

    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)

    return dataframe
df = data_prep(df)

###################### TASK 2 ####################################
# RFM METRİKLERİNİN HESAPLANMASI
###################################################################

# Recency --> en son ne zmaan alisveris yapıldı
# Frequency --> alisveris yapma sıklıgı
# Monetary --> Ne kadarlık alisveris yapiyor

# recency degerini max degerden 2 gün sonrası alalim
df["last_order_date"].max()
analyses_date = dt.datetime(2021 , 6 , 1)


# customer id , recency ,frequency ,monetary nin oldugu yeni bir rfm yapalim
rfm = pd.DataFrame()
rfm['customer id'] = df['master_id']

rfm['recency'] = (analyses_date - df['last_order_date']).dt.days
rfm['frequency'] = df['order_num_total']
rfm['monetary'] = df['customer_value_total']

rfm.head()

######################################## TASK 3 ##########################################
##############################  RF Skorunun Hesaplanması #################################
###########################################################################################

rfm['recency_score'] = pd.qcut(rfm['recency'], 5, labels = [5,4,3,2,1])
rfm['frequency_score'] = pd.qcut(rfm['frequency'].rank(method = "first"), 5, labels = [1,2,3,4,5])
rfm['monetary_score'] = pd.qcut(rfm['monetary'], 5, labels = [1,2,3,4,5])

rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) +
                   rfm['frequency_score'].astype(str))

############################ TASK 4 #################################################
###############  RF Skorunun Segment Olarak Tanımlanması
##################################################################################

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

rfm["segment"] = rfm['RF_SCORE'].replace(seg_map,regex=True)


######################### TASK 5 ######################################
#   Aksiyon zamanı!
###############################################################

# Adım 1: Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
rfm[["segment", "recency", "frequency" , "monetary"]].groupby("segment").agg(["mean" , "count"])

# Adım 2: RFM analizi yardımıyla aşağıda verilen 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv olarak kaydediniz.

###  a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri
#  tercihlerinin üstünde. Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak
#  iletişime geçmek isteniliyor. Sadık müşterilerinden(champions, loyal_customers) ve kadın kategorisinden alışveriş
#  yapan kişiler özel olarak iletişim kurulacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına kaydediniz.

target_segments_customer_ids = rfm.loc[rfm["segment"].isin(["champions", "loyal_customers"]) , "customer id"]

cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) & (df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
cust_ids.head()
cust_ids.to_csv("yeni_marka_hedef_musteri_id.csv", index=False)
cust_ids.shape


#### b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşterilerden olan ama uzun süredir
# alışveriş yapmayan ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
# olarak kaydediniz.

target_segments_customer_ids = rfm[rfm["segment"].isin(["cant_loose","hibernating","new_customers", "about_to_sleep"])]["customer id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) & ((df["interested_in_categories_12"].str.contains("ERKEK"))
                                                                      |(df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
cust_ids.to_csv("indirim_hedef_müşteri_ids.csv", index=False)
cust_ids.shape


###############################################################
# BONUS
###############################################################

def create_rfm(dataframe):
    # Veriyi Hazırlma
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)


    # RFM METRIKLERININ HESAPLANMASI
    #dataframe["last_order_date"].max()  # 2021-05-30
    analysis_date = dt.datetime(2021, 6, 1)
    rfm = pd.DataFrame()
    rfm["customer_id"] = dataframe["master_id"]
    rfm["recency"] = (analysis_date - dataframe["last_order_date"]).dt.days
    rfm["frequency"] = dataframe["order_num_total"]
    rfm["monetary"] = dataframe["customer_value_total"]

    # RF ve RFM SKORLARININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
    rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str))


    # SEGMENTLERIN ISIMLENDIRILMESI
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
    rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

    return rfm[["customer_id", "recency","frequency","monetary","RF_SCORE","RFM_SCORE","segment"]]

rfm_df = create_rfm(df)
rfm_df




