import streamlit as st
from pymongo import MongoClient

# Koneksi ke MongoDB Atlas
client = MongoClient("mongodb+srv://bigdata_ghibran:1@ghibranti23a.otb7w.mongodb.net/?retryWrites=true&w=majority&appName=ghibranti23a")
db = client["TokoOnline"]  # Nama database
collection = db["KatalogSepatu"]  # Nama koleksi

# Judul Aplikasi
st.title("Tambah / Update Stok Produk")

st.markdown("""
### Nama Kelompok: Big Big Team 4
1. **Anggota 1** - Trena Gunawan
2. **Anggota 2** - M. Sechan Alfarisi 
3. **Anggota 3** - Inda Fadila A.H
4. **Anggota 4** - M. Gibran Muslih
""")

# Pilih kategori di luar form agar dinamis
kategori = st.selectbox("Pilih Kategori Produk", ["Elektronik", "Sepatu", "Tas", "Aksesoris", "Makanan", "Furnitur", "Lainnya"])

with st.form("form_tambah_produk"):
    nama_produk = st.text_input("Nama Produk")
    harga = st.number_input("Harga", min_value=0)
    stok_tambah = st.number_input("Tambah Stok", min_value=0)

    # Field tambahan khusus untuk produk sepatu
    if kategori == "Sepatu":
        ukuran_input = st.text_input("Masukkan Ukuran Sepatu (Pisahkan dengan koma, contoh: 38,39,40)")
        deskripsi = st.text_area("Deskripsi Produk")
        warna = st.text_input("Warna")
        merek = st.text_input("Merek")

    # Tombol Simpan
    submit = st.form_submit_button("Simpan")

    if submit:
        if nama_produk and harga > 0 and stok_tambah >= 0:
            # Jika kategori sepatu, validasi field tambahan
            if kategori == "Sepatu":
                if not ukuran_input or not deskripsi or not warna or not merek:
                    st.error("❌ Mohon isi data sepatu dengan lengkap (Ukuran, Deskripsi, Warna, Merek)!")
                else:
                    ukuran_list = [int(ukuran.strip()) for ukuran in ukuran_input.split(",") if ukuran.strip().isdigit()]
                    if not ukuran_list:
                        st.error("❌ Ukuran sepatu harus berupa angka yang dipisahkan dengan koma!")
                    else:
                        # Cek apakah produk sudah ada di database
                        existing_product = collection.find_one({"nama": nama_produk})
                        if existing_product:
                            new_stok = existing_product["stok"] + stok_tambah
                            update_data = {
                                "stok": new_stok,
                                "harga": harga,
                                "kategori": kategori,
                                "ukuran": ukuran_list,
                                "deskripsi": deskripsi,
                                "warna": warna,
                                "merek": merek
                            }
                            collection.update_one({"nama": nama_produk}, {"$set": update_data})
                            st.success(f"✅ Stok produk '{nama_produk}' berhasil diperbarui! Stok sekarang: {new_stok}")
                        else:
                            data_produk = {
                                "nama": nama_produk,
                                "harga": harga,
                                "kategori": kategori,
                                "stok": stok_tambah,
                                "ukuran": ukuran_list,
                                "deskripsi": deskripsi,
                                "warna": warna,
                                "merek": merek
                            }
                            collection.insert_one(data_produk)
                            st.success(f"✅ Produk baru '{nama_produk}' berhasil ditambahkan!")
            else:
                # Untuk produk selain sepatu
                existing_product = collection.find_one({"nama": nama_produk})
                if existing_product:
                    new_stok = existing_product["stok"] + stok_tambah
                    update_data = {"stok": new_stok, "harga": harga, "kategori": kategori}
                    collection.update_one({"nama": nama_produk}, {"$set": update_data})
                    st.success(f"✅ Stok produk '{nama_produk}' berhasil diperbarui! Stok sekarang: {new_stok}")
                else:
                    data_produk = {"nama": nama_produk, "harga": harga, "kategori": kategori, "stok": stok_tambah}
                    collection.insert_one(data_produk)
                    st.success(f"✅ Produk baru '{nama_produk}' berhasil ditambahkan!")
        else:
            st.error("❌ Mohon isi semua data dengan benar!")
