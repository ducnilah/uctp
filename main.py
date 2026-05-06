# main.py
import math
from ortools.sat.python import cp_model
from data import data

def generate_classes(input_data):
    """
    Pha 1: Tự động sinh danh sách Lớp học phần dựa trên sức chứa và nhu cầu.
    """
    generated_classes = []
    class_id_counter = 0
    
    for sub in input_data["subjects"]:
        total_students = sum(c["s_k"] for c in input_data["cohorts"] if c["id"] in sub["mand"])
        
        # KỊCH BẢN 1: Môn học chung ghép toàn trường (Sức chứa lớp >= Tổng sinh viên)
        if sub["size"] >= total_students:
            generated_classes.append({
                "id": class_id_counter,
                "sub": sub["id"],
                "size": total_students,
                "dur": sub["dur"],
                "ses": sub["ses"],
                "mand": sub["mand"]
            })
            class_id_counter += 1
            
        # KỊCH BẢN 2: Chia thành nhiều lớp nhỏ cho từng ngành
        else:
            for k_id in sub["mand"]:
                s_k = next(c["s_k"] for c in input_data["cohorts"] if c["id"] == k_id)
                num_classes_needed = math.ceil(s_k / sub["size"])
                
                for _ in range(num_classes_needed):
                    generated_classes.append({
                        "id": class_id_counter,
                        "sub": sub["id"],
                        "size": sub["size"],
                        "dur": sub["dur"],
                        "ses": sub["ses"],
                        "mand": [k_id]
                    })
                    class_id_counter += 1
                    
    return generated_classes

def solve_timetabling():
    # =========================================================
    # 1. PHA TẠO LỚP & LOG KẾT QUẢ
    # =========================================================
    classes = generate_classes(data)
    
    print("=" * 85)
    print(f"PHA 1: HỆ THỐNG TỰ ĐỘNG TẠO {len(classes)} LỚP HỌC PHẦN TỪ {len(data['subjects'])} MÔN HỌC")
    print("=" * 85)
    for c in classes:
        sub_name = next(s["name"] for s in data["subjects"] if s["id"] == c["sub"])
        cohorts = [next(k["name"] for k in data["cohorts"] if k["id"] == k_id) for k_id in c["mand"]]
        
        # Log ra thông tin thời gian học của từng lớp
        time_info = f"{c['ses']} buổi x {c['dur']} tiết"
        print(f"Lớp L{c['id']:<2} | Môn: {sub_name:<15} | Sĩ số: {c['size']:<3} | Thời lượng: {time_info:<15} | Ngành: {','.join(cohorts)}")
    print("=" * 85 + "\n")
    
    # =========================================================
    # 2. KHỞI TẠO MÔ HÌNH VÀ BIẾN
    # =========================================================
    model = cp_model.CpModel()
    
    num_days = data["num_days"]
    P = data["periods_per_day"]
    total_periods = num_days * P

    valid_starts_by_dur = {}
    for c in classes:
        dur = c["dur"]
        if dur not in valid_starts_by_dur:
            allowed = [day * P + p for day in range(num_days) for p in range(P) if p + dur <= P]
            valid_starts_by_dur[dur] = allowed

    class_sessions = {}
    room_intervals = {r["id"]: [] for r in data["rooms"]}
    subject_intervals = {j["id"]: [] for j in data["subjects"]}
    cohort_intervals = {k["id"]: [] for k in data["cohorts"]}
    
    for c in classes:
        c_id = c["id"]
        dur = c["dur"]
        req_size = c["size"]
        
        for s in range(c["ses"]):
            start_var = model.NewIntVarFromDomain(
                cp_model.Domain.FromValues(valid_starts_by_dur[dur]), f"start_c{c_id}_s{s}"
            )
            end_var = model.NewIntVar(0, total_periods, f"end_c{c_id}_s{s}")
            interval_var = model.NewIntervalVar(start_var, dur, end_var, f"int_c{c_id}_s{s}")
            
            subject_intervals[c["sub"]].append(interval_var)
            for k in c["mand"]:
                cohort_intervals[k].append(interval_var)
                
            class_sessions[(c_id, s)] = {
                "start": start_var, "end": end_var, "interval": interval_var,
                "room_vars": {} 
            }
            
            valid_room_booleans = []
            
            for r in data["rooms"]:
                if r["cap"] >= req_size:
                    is_present = model.NewBoolVar(f"pres_c{c_id}_s{s}_r{r['id']}")
                    opt_interval = model.NewOptionalIntervalVar(
                        start_var, dur, end_var, is_present, f"opt_int_c{c_id}_s{s}_r{r['id']}"
                    )
                    room_intervals[r["id"]].append(opt_interval)
                    class_sessions[(c_id, s)]["room_vars"][r["id"]] = is_present
                    valid_room_booleans.append(is_present)
            
            if not valid_room_booleans:
                print(f"Lỗi dữ liệu: Không có phòng nào chứa nổi Lớp ID {c_id} (Cần {req_size} chỗ)!")
                return
                
            model.AddExactlyOne(valid_room_booleans)
            
        for s in range(c["ses"] - 1):
            model.Add(class_sessions[(c_id, s+1)]["start"] >= class_sessions[(c_id, s)]["end"])

    # =========================================================
    # 3. RÀNG BUỘC CỐT LÕI
    # =========================================================
    for r_id, intervals in room_intervals.items():
        if intervals:
            model.AddNoOverlap(intervals)
        
    for j in data["subjects"]:
        if subject_intervals[j["id"]]:
            demands = [1] * len(subject_intervals[j["id"]])
            model.AddCumulative(subject_intervals[j["id"]], demands, j["L_j"])
            
    for k_id, intervals in cohort_intervals.items():
        if intervals:
            model.AddNoOverlap(intervals)

    # =========================================================
    # 4. CHẠY SOLVER & IN THỜI KHÓA BIỂU
    # =========================================================
    print("PHA 2: BẮT ĐẦU CHẠY THUẬT TOÁN XẾP LỊCH (OR-TOOLS)...\n")
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0 
    
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"xếp lịch thành công (Thời gian chạy: {solver.WallTime():.2f} giây)")
        print("=" * 85)
        
        schedule_output = []
        for c in classes:
            sub_name = next(s["name"] for s in data["subjects"] if s["id"] == c["sub"])
            cohorts = [next(k["name"] for k in data["cohorts"] if k["id"] == k_id) for k_id in c["mand"]]
            
            for s in range(c["ses"]):
                start_val = solver.Value(class_sessions[(c["id"], s)]["start"])
                day = start_val // P
                period = start_val % P
                
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
                
        schedule_output.sort(key=lambda x: (x["day"], x["period"]))
        current_day = -1
        for item in schedule_output:
            if item["day"] != current_day:
                print("-" * 85)
                current_day = item["day"]
            print(item["info"])
        print("=" * 85)
            
    else:
        print("không thể xếp lịch")

if __name__ == "__main__":
    solve_timetabling()