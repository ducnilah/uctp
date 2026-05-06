# ==========================================
# MOCK DATA UCTP - CÓ LỚP HỌC CHUNG TOÀN TRƯỜNG
# ==========================================

data = {
    # -------------------------------------------------------------
    # 1. THỜI GIAN
    # -------------------------------------------------------------
    "num_days": 7,          
    "periods_per_day": 12,   

    # -------------------------------------------------------------
    # 2. PHÒNG HỌC
    # THÊM MỚI: Nha_Thi_Dau sức chứa 500 để chứa toàn trường (300 sv)
    # -------------------------------------------------------------
    "rooms": [
        {"id": 0, "name": "Room_Small_1", "cap": 40},
        {"id": 1, "name": "Room_Small_2", "cap": 40},
        {"id": 2, "name": "Room_Med_1",   "cap": 60},
        {"id": 3, "name": "Room_Med_2",   "cap": 60},
        {"id": 4, "name": "Room_Large",   "cap": 100},
        {"id": 5, "name": "Giant_Hall",   "cap": 150},
        {"id": 6, "name": "Nha_Thi_Dau",  "cap": 500} # Phòng dành cho lớp toàn trường
    ],

    # -------------------------------------------------------------
    # 3. NGÀNH HỌC (Tổng số sinh viên = 120 + 100 + 80 = 300)
    # -------------------------------------------------------------
    "cohorts": [
        {"id": 0, "name": "CNTT (CS)",   "s_k": 150},
        {"id": 1, "name": "KinhTe (BA)", "s_k": 100},
        {"id": 2, "name": "DienTu (EE)", "s_k": 80}
    ],

    # -------------------------------------------------------------
    # 4. MÔN HỌC
    # THÊM MỚI: Môn 12 là môn bắt buộc toàn trường
    # -------------------------------------------------------------
    "subjects": [
        {"id": 0, "name": "Toan Cao Cap", "L_j": 2},
        {"id": 1, "name": "Tieng Anh 1",  "L_j": 2},
        {"id": 2, "name": "Lap Trinh C",  "L_j": 1},
        {"id": 3, "name": "Cau Truc DL",  "L_j": 2},
        {"id": 4, "name": "Co So Du Lieu","L_j": 2},
        {"id": 5, "name": "Kinh Te Vi Mo","L_j": 1},
        {"id": 6, "name": "Ke Toan",      "L_j": 2},
        {"id": 7, "name": "Marketing",    "L_j": 2},
        {"id": 8, "name": "Quan Tri",     "L_j": 1},
        {"id": 9, "name": "Vat Ly 1",     "L_j": 1},
        {"id": 10, "name": "Mach Dien",   "L_j": 2},
        {"id": 11, "name": "Tin Hieu",    "L_j": 2},
        {"id": 12, "name": "Triet Hoc",   "L_j": 1} # Môn toàn trường
    ],

    # -------------------------------------------------------------
    # 5. LỚP HỌC PHẦN
    # -------------------------------------------------------------
    "classes": [
        # =========================================================
        # [THÊM MỚI] LỚP CHUNG TOÀN TRƯỜNG (Bắt buộc với cả 3 ngành)
        # =========================================================
        # id=28: Sinh viên cả 3 ngành cùng học. Kéo dài 3 tiết, 1 buổi.
        {"id": 28, "sub": 12, "size": 300, "dur": 3, "ses": 1, "mand": [0, 1, 2]},

        # --- CÁC LỚP CHO NGÀNH CNTT (S_0 = 120) ---
        {"id": 0, "sub": 0, "size": 60, "dur": 2, "ses": 2, "mand": [0]},
        {"id": 1, "sub": 0, "size": 60, "dur": 2, "ses": 2, "mand": [0]},
        {"id": 2, "sub": 1, "size": 40, "dur": 2, "ses": 2, "mand": [0]},
        {"id": 3, "sub": 1, "size": 40, "dur": 2, "ses": 2, "mand": [0]},
        {"id": 4, "sub": 1, "size": 40, "dur": 2, "ses": 2, "mand": [0]},
        {"id": 5, "sub": 2, "size": 120,"dur": 3, "ses": 1, "mand": [0]},
        {"id": 6, "sub": 3, "size": 60, "dur": 2, "ses": 2, "mand": [0]},
        {"id": 7, "sub": 3, "size": 60, "dur": 2, "ses": 2, "mand": [0]},
        {"id": 8, "sub": 4, "size": 60, "dur": 2, "ses": 2, "mand": [0]},
        {"id": 9, "sub": 4, "size": 60, "dur": 2, "ses": 2, "mand": [0]},

        # --- CÁC LỚP CHO NGÀNH KINH TẾ (S_1 = 100) ---
        {"id": 10,"sub": 1, "size": 40, "dur": 2, "ses": 2, "mand": [1]},
        {"id": 11,"sub": 1, "size": 40, "dur": 2, "ses": 2, "mand": [1]},
        {"id": 12,"sub": 1, "size": 40, "dur": 2, "ses": 2, "mand": [1]},
        {"id": 13,"sub": 5, "size": 100,"dur": 3, "ses": 1, "mand": [1]},
        {"id": 14,"sub": 6, "size": 60, "dur": 2, "ses": 2, "mand": [1]},
        {"id": 15,"sub": 6, "size": 60, "dur": 2, "ses": 2, "mand": [1]},
        {"id": 16,"sub": 7, "size": 60, "dur": 2, "ses": 2, "mand": [1]},
        {"id": 17,"sub": 7, "size": 60, "dur": 2, "ses": 2, "mand": [1]},
        {"id": 18,"sub": 8, "size": 100,"dur": 3, "ses": 1, "mand": [1]},

        # --- CÁC LỚP CHO NGÀNH ĐIỆN TỬ (S_2 = 80) ---
        {"id": 19,"sub": 0, "size": 40, "dur": 2, "ses": 2, "mand": [2]},
        {"id": 20,"sub": 0, "size": 40, "dur": 2, "ses": 2, "mand": [2]},
        {"id": 21,"sub": 1, "size": 40, "dur": 2, "ses": 2, "mand": [2]},
        {"id": 22,"sub": 1, "size": 40, "dur": 2, "ses": 2, "mand": [2]},
        {"id": 23,"sub": 9, "size": 80, "dur": 2, "ses": 2, "mand": [2]},
        {"id": 24,"sub": 10,"size": 40, "dur": 2, "ses": 2, "mand": [2]},
        {"id": 25,"sub": 10,"size": 40, "dur": 2, "ses": 2, "mand": [2]},
        {"id": 26,"sub": 11,"size": 40, "dur": 2, "ses": 2, "mand": [2]},
        {"id": 27,"sub": 11,"size": 40, "dur": 2, "ses": 2, "mand": [2]}
    ]
}