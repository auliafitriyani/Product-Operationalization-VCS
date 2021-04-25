# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 15:12:50 2021

@author: auliaf067684
"""

#from typing import Optional
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

data = pd.read_csv('DataAPI.csv')

# Main Page: Keterangan mengenai data yang digunakan, dan halaman yang telah dibuat
@app.get("/")
def read_root():
    
    return{"Belongs to": "Aulia Fitriyani(67684)", 
           "Data About":"Data peserta KB Aktif menurut metode kontrasepsi per kecamatan di Kabupaten Bantul (https://data.go.id/)", 
           "Main Page":"This is Main Page",
           "Second Page": "/secondpage",
           "Third Page": "/thirdpage",
           "Fourth Page": "/fourthpage"}


# Second Page: Hasil analisis mengenai keberhasilan memenuhi target peserta KB Aktif
@app.get("/secondpage")
def persentasekb():
    
    # Menjumlahkan semua data pada jumlah peserta dan target lalu dilakukan perhitungan untuk mendapatkan persentase
    peserta_kb = sum(data['jumlah_peserta_kb_aktif'])
    target_kb = sum(data['target_kb_aktif'])
    persentase_target = str(round(peserta_kb/target_kb*100,2)) + "%"
    
    ket = "Jika target yang terpenuhi lebih dari 80%, dapat dikatakan bahwa hasil yang didapat pemerintah Bantul sudah cukup bagus mengenai pengguna KB Aktif di wilayahnya"
    
    return{"Target yang Terpenuhi": persentase_target, 
           "Keterangan": ket}


# Third Page: Hasil analisis berupa kecamatan pada Kabupaten Bantul yang paling tinggi persentasenya dalam memenuhi target
@app.get("/thirdpage")
def topkecamatan():
    
    # Mengurutkan data persentase per kecamatan yang sudah terdapat pada data
    top_target = data.sort_values(by=['persentase_trhdp_target_kb_aktif'], ascending = False)
    top_target = top_target.reset_index()
    del top_target['index']
    
    # Mengambil nama kecamatan dan persentasenya yang merupakan 3 persentase tertinggi
    satu = top_target['kapanewon'][0]; psatu = str(top_target['persentase_trhdp_target_kb_aktif'][0]) + "%"
    dua = top_target['kapanewon'][1]; pdua = str(top_target['persentase_trhdp_target_kb_aktif'][1]) + "%"
    tiga = top_target['kapanewon'][2]; ptiga = str(top_target['persentase_trhdp_target_kb_aktif'][2]) + "%"
    ket = "Berikut daftar 3 kecamatan yang memiliki persentase memenuhi target peserta KB aktif paling tinggi"
    
    return{"Keterangan": ket,
           "Pertama": {satu:psatu},
           "Kedua": {dua:pdua},
           "Ketiga": {tiga:ptiga}}


# Fourth Page: Hasil analisis berupa metode kontrasepsi yang paling banyak digunakan di kabupaten Bantul
@app.get("/fourthpage")
def toplastmethode():
    
    # Membuat 2 list yang diperuntukkan bagi nama metode dan persentase penggunaannya di kabupaten Bantul
    metode = []
    total = []
    # data.columns[1:-3] merupakan nama-nama metode yang digunakan
    for i in data.columns[1:-3]:
        metode.append(i)
        jumlah = round(sum(data[i])/sum(data['jumlah_peserta_kb_aktif'])*100,2)
        total.append(jumlah)
    
    # Menggabungkan 2 list di atas menjadi dataframe dan diurutkan dari persentase terbesar - terkecil    
    data_method = pd.DataFrame(list(zip(metode, total)),columns =['Metode', 'Persentase'])
    data_method = data_method.sort_values(by=['Persentase'], ascending = False)
    data_method = data_method.reset_index()
    del data_method['index']
    
    # Mengambil nama kecamatan dan persentase dari persentase terbesar dan terkecil
    top = str(data_method['Metode'][0]).replace("metode_kb_aktif_", "Metode "); ptop = str(data_method['Persentase'][0]) + "%"
    last = str(data_method['Metode'][len(data_method)-1]).replace("metode_kb_aktif_", "Metode "); plast = str(data_method['Persentase'][len(data_method)-1]) + "%"
    
    ket = "Berikut metode yang paling banyak serta yang paling sedikit digunakan pada kabupaten Bantul"
    
    return{"Keterangan": ket,
           "Terbanyak": {top:ptop},
           "Tersedikit": {last:plast}}
