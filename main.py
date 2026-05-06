from ortools.sat.python import cp_model
from data import data

def solve_timetabling():
    model = cp_model.CpModel()
    
    # ---------------------------------------------------------
    # 1. TRÍCH XUẤT THAM SỐ
    # ---------------------------------------------------------
    num_days = data["num_days"]
    P = data["periods_per_day"]
    total_periods = num_days * P

    # Đảm bảo 1 buổi học không vắt qua ngày hôm sau
    valid_starts_by_dur = {}
    for c in data["classes"]:
        dur = c["dur"]
        if dur not in valid_starts_by_dur:
            allowed = []
            for day in range(num_days):
                for p in range(P):
                    if p + dur <= P:  # Nếu bắt đầu tại p và kéo dài dur tiết mà vẫn nằm trong ngày
                        allowed.append(day * P + p)
            valid_starts_by_dur[dur] = allowed

    # Khởi tạo các cấu trúc lưu trữ biến
    class_sessions = {}
    room_intervals = {r["id"]: [] for r in data["rooms"]}
    subject_intervals = {j["id"]: [] for j in data["subjects"]}
    cohort_intervals = {k["id"]: [] for k in data["cohorts"]}
    
    # ---------------------------------------------------------
    # 2. KHAI BÁO BIẾN (VARIABLES)
    # ---------------------------------------------------------
    for c in data["classes"]:
        c_id = c["id"]
        dur = c["dur"]
        req_size = c["size"]
        
        for s in range(c["ses"]):
            # Biến Start và End của 1 buổi học
            start_var = model.NewIntVarFromDomain(
                cp_model.Domain.FromValues(valid_starts_by_dur[dur]), f"start_c{c_id}_s{s}"
            )
            end_var = model.NewIntVar(0, total_periods, f"end_c{c_id}_s{s}")
            interval_var = model.NewIntervalVar(start_var, dur, end_var, f"int_c{c_id}_s{s}")
            
            # Lưu trữ interval cho Ràng buộc Môn học và Ràng buộc Ngành học
            subject_intervals[c["sub"]].append(interval_var)
            for k in c["mand"]:
                cohort_intervals[k].append(interval_var)
                
            class_sessions[(c_id, s)] = {
                "start": start_var, "end": end_var, "interval": interval_var,
                "room_vars": {} 
            }
            
            valid_room_booleans = []
            
            # Duyệt các phòng, chỉ tạo biến nến phòng đủ sức chứa (Ràng buộc Sức chứa)
            for r in data["rooms"]:
                if r["cap"] >= req_size:
                    is_present = model.NewBoolVar(f"pres_c{c_id}_s{s}_r{r['id']}")
                    opt_interval = model.NewOptionalIntervalVar(
                        start_var, dur, end_var, is_present, f"opt_int_c{c_id}_s{s}_r{r['id']}"
                    )
                    room_intervals[r["id"]].append(opt_interval)
                    class_sessions[(c_id, s)]["room_vars"][r["id"]] = is_present
                    valid_room_booleans.append(is_present)
            
            # Mỗi buổi học phải được gán vào ĐÚNG MỘT phòng hợp lệ
            if not valid_room_booleans:
                print(f"LỖI: Không có phòng nào đủ sức chứa cho Lớp ID {c_id} (size={req_size})")
                return
            model.AddExactlyOne(valid_room_booleans)
            
        # Ràng buộc thứ tự buổi học (Tránh symmetry: Buổi s+1 phải học sau buổi s)
        for s in range(c["ses"] - 1):
            model.Add(class_sessions[(c_id, s+1)]["start"] >= class_sessions[(c_id, s)]["end"])

    # ---------------------------------------------------------
    # 3. THÊM RÀNG BUỘC (CONSTRAINTS)
    # ---------------------------------------------------------
    
    # Ràng buộc: Tại 1 phòng, các buổi học không được chồng lấn thời gian
    for r_id, intervals in room_intervals.items():
        if intervals:
            model.AddNoOverlap(intervals)
        
    # Ràng buộc: Giới hạn số lớp học của một môn diễn ra đồng thời (L_j)
    for j in data["subjects"]:
        if subject_intervals[j["id"]]:
            demands = [1] * len(subject_intervals[j["id"]])
            model.AddCumulative(subject_intervals[j["id"]], demands, j["L_j"])
            
    # Ràng buộc: Các môn bắt buộc của cùng một ngành học (Cohort) không được trùng lịch
    for k_id, intervals in cohort_intervals.items():
        if intervals:
            model.AddNoOverlap(intervals)

    # ---------------------------------------------------------
    # 4. CHẠY SOLVER & IN KẾT QUẢ
    # ---------------------------------------------------------
    print("Mô hình đã xây dựng xong. Đang giải...")
    solver = cp_model.CpSolver()
    # solver.parameters.log_search_progress = True  # Bỏ comment dòng này nếu muốn xem log chạy của solver
    solver.parameters.max_time_in_seconds = 60.0    # Chạy tối đa 60s
    
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"\nĐÃ TÌM THẤY LỊCH HỌC KHẢ THI! ({solver.WallTime():.2f} giây)\n")
        
        # Format kết quả để in
        schedule_output = []
        for c in data["classes"]:
            sub_name = next(s["name"] for s in data["subjects"] if s["id"] == c["sub"])
            cohorts = [next(k["name"] for k in data["cohorts"] if k["id"] == k_id) for k_id in c["mand"]]
            
            for s in range(c["ses"]):
                start_val = solver.Value(class_sessions[(c["id"], s)]["start"])
                day = start_val // P
                period = start_val % P
                
                # Tìm phòng được thuật toán chọn
                assigned_room_id = -1
                for r_id, is_present in class_sessions[(c["id"], s)]["room_vars"].items():
                    if solver.Value(is_present):
                        assigned_room_id = r_id
                        break
                room_name = next(r["name"] for r in data["rooms"] if r["id"] == assigned_room_id)
                
                schedule_output.append({
                    "day": day, "period": period,
                    "info": f"Ngày {day+1} | Tiết {period+1}-{period+c['dur']} | Phòng: {room_name:<12} | Lớp: L{c['id']:<2} | Môn: {sub_name:<15} | Ngành: {','.join(cohorts)}"
                })
                
        # In ra màn hình theo ngày và tiết
        schedule_output.sort(key=lambda x: (x["day"], x["period"]))
        current_day = -1
        for item in schedule_output:
            if item["day"] != current_day:
                print("-" * 90)
                current_day = item["day"]
            print(item["info"])
            
    else:
        print("KHÔNG THỂ TÌM THẤY LỊCH (INFEASIBLE). Hãy kiểm tra lại số lượng lớp hoặc nới lỏng các ràng buộc.")

if __name__ == "__main__":
    solve_timetabling()