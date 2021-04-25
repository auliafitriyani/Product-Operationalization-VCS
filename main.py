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

@app.get("/")
def read_root():
    
    return{"Belongs to": "Aulia Fitriyani(67684)", 
           "Data About":"Data peserta KB Aktif menurut metode kontrasepsi per kecamatan di Kabupaten Bantul (https://data.go.id/)", 
           "Add this to your URL":"/persentasekb"}

@app.get("/persentasekb")
def persentasekb():
    
    peserta_kb = sum(data['jumlah_peserta_kb_aktif'])
    target_kb = sum(data['target_kb_aktif'])
    persentase_target = str(round(peserta_kb/target_kb*100,2)) + "%"
    ket = "Jika target yang terpenuhi lebih dari 80%, dapat dikatakan bahwa hasil yang didapat pemerintah Bantul sudah cukup bagus mengenai pengguna KB Aktif di wilayahnya"
    
    return{"Target yang Terpenuhi": persentase_target, 
           "Keterangan": ket,
           "Change letter after '/' in your URL to":"topkecamatan"}

@app.get("/topkecamatan")
def topkecamatan():
    
    top_target = data.sort_values(by=['persentase_trhdp_target_kb_aktif'], ascending = False)
    top_target = top_target.reset_index()
    del top_target['index']
    satu = top_target['kapanewon'][0]; psatu = str(top_target['persentase_trhdp_target_kb_aktif'][0]) + "%"
    dua = top_target['kapanewon'][1]; pdua = str(top_target['persentase_trhdp_target_kb_aktif'][1]) + "%"
    tiga = top_target['kapanewon'][2]; ptiga = str(top_target['persentase_trhdp_target_kb_aktif'][2]) + "%"
    ket = "Berikut daftar 3 kecamatan yang memiliki persentase memenuhi target peserta KB aktif paling tinggi"
    
    return{"Keterangan": ket,
           "Pertama": [satu,psatu],
           "Kedua": [dua,pdua],
           "Ketiga": [tiga,ptiga],
           "Change letter after '/' in your URL to":"toplastmethode"}

@app.get("/toplastmethode")
def toplastmethode():
    
    metode = []
    total = []
    for i in data.columns[1:-3]:
        metode.append(i)
        jumlah = round(sum(data[i])/sum(data['jumlah_peserta_kb_aktif'])*100,2)
        total.append(jumlah)
        
    data_method = pd.DataFrame(list(zip(metode, total)),columns =['Metode', 'Persentase'])
    data_method = data_method.sort_values(by=['Persentase'], ascending = False)
    data_method = data_method.reset_index()
    del data_method['index']
    
    top = str(data_method['Metode'][0]).replace("metode_kb_aktif_", "Metode "); ptop = str(data_method['Persentase'][0]) + "%"
    last = str(data_method['Metode'][len(data_method)-1]).replace("metode_kb_aktif_", "Metode "); plast = str(data_method['Persentase'][len(data_method)-1]) + "%"
    
    ket = "Berikut metode yang paling banyak serta yang paling sedikit digunakan pada kota Bantul"
    
    return{"Keterangan": ket,
           "Terbanyak": [top,ptop],
           "Tersedikit": [last,plast]}
