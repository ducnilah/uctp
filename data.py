# data.py

data = {
    "num_days": 5,          
    "periods_per_day": 6,   

    "rooms": [
        {"id": 0, "name": "Room_Small_1", "cap": 40},
        {"id": 1, "name": "Room_Small_2", "cap": 40},
        {"id": 2, "name": "Room_Med_1",   "cap": 60},
        {"id": 3, "name": "Room_Med_2",   "cap": 60},
        {"id": 4, "name": "Room_Large",   "cap": 100},
        {"id": 5, "name": "Giant_Hall",   "cap": 150},
        {"id": 6, "name": "Nha_Thi_Dau",  "cap": 500} 
    ],

    "cohorts": [
        {"id": 0, "name": "CNTT (CS)",   "s_k": 120},
        {"id": 1, "name": "KinhTe (BA)", "s_k": 100},
        {"id": 2, "name": "DienTu (EE)", "s_k": 80}
    ],

    "subjects": [
        # Môn chung toàn trường: Sĩ số 300, 1 buổi 3 tiết -> Sẽ sinh ra đúng 1 lớp khổng lồ cho cả 3 ngành
        {"id": 0, "name": "Triet Hoc",    "L_j": 1, "size": 300, "dur": 3, "ses": 1, "mand": [0, 1, 2]},
        
        # Môn chung nhiều ngành, nhưng chia lớp nhỏ
        {"id": 1, "name": "Tieng Anh 1",  "L_j": 2, "size": 40,  "dur": 2, "ses": 2, "mand": [0, 1, 2]},
        {"id": 2, "name": "Toan Cao Cap", "L_j": 2, "size": 60,  "dur": 2, "ses": 2, "mand": [0, 2]},
        
        # Môn chuyên ngành
        {"id": 3, "name": "Lap Trinh C",  "L_j": 1, "size": 70, "dur": 3, "ses": 1, "mand": [0]},
        {"id": 4, "name": "Kinh Te Vi Mo","L_j": 1, "size": 100, "dur": 3, "ses": 1, "mand": [1]},
        {"id": 5, "name": "Vat Ly 1",     "L_j": 1, "size": 80,  "dur": 2, "ses": 2, "mand": [2]},
    ]
}