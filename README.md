- Cau hinh du an:
    pip install django djangorestframework djongo pymongo pillow hoac co the xu dung pip install -r requirement.txt

--- TAI LIEU THAM KHAO DE VIET CODE TUAN THEO CAC CLASS, FUNC, .... TRONG DU AN: https://github.com/TiCoder-coder/OOP_TS.git ----
----------------------------------- VIET THEM FUNC GI KHAC THI PHAI CHU THICH CHUC NANG VA GIAI THICH----------------------------------------


- Chuc nang cac file: 
    /ZOO_MANAGEMENT_PYTHON/ZOO_MANAGEMENT/zoo_app/enums.py                          ---- chua cac enums cua du an
    /ZOO_MANAGEMENT_PYTHON/ZOO_MANAGEMENT/manage.py                                 ---- dung de call API va ket noi
    /ZOO_MANAGEMENT_PYTHON/ZOO_MANAGEMENT/zoo_app/serializers.py                    ---- dung de kiem tra cac thuoc tinh
    /ZOO_MANAGEMENT_PYTHON/ZOO_MANAGEMENT/ZOO_MANAGEMENT/settings.py                ---- tuong tu nhu tsconfig
    /ZOO_MANAGEMENT_PYTHON/ZOO_MANAGEMENT/zoo_app/urls.py                           ---- nhu file index dung de call API
    /ZOO_MANAGEMENT/zoo_app/models.py                                               ---- dinh nghia cac lop


    /ZOO_MANAGEMENT_PYTHON/zoo_app/serializers                                      ---- tuong ung voi tang dtos (dung de create va update cac thuoc tinh)
    /ZOO_MANAGEMENT_PYTHON/zoo_app/models                                           ---- tang data layer dung de tuong tac va luu vao mongodb
    /ZOO_MANAGEMENT_PYTHON/zoo_app/services.py                                      ---- tuong tu tang services - code OOP
    /ZOO_MANAGEMENT_PYTHON/zoo_app/views                                            ---- dung de xu li request tu client
    /ZOO_MANAGEMENT_PYTHON/zoo_app/views                                            ---- dung de call API, chuc nang nhu tang controller



    /ZOO_MANAGEMENT_PYTHON/zoo_app/admin.py                                         ---- dung de truy cap voi chuc nang admin ma khong can thong qua API


- MO TA VE CAC CLASS VA ATTRIBUTE (BAT BUOC phai dat dung nhu yeu cau de dong nhat code);
    - enclosures: idEnclosure: str, nameEnclosure: str, areaSize: str, climate('Tropical', 'Desert', 'Aquatic', 'Temperate') --- lay tu enums.py, capacity: float.

    - animals: id: str, name: str, age: int, species: str, gender('Male', 'Female') --- lay tu enums.py, weight: float, healthStatus ('Healthy', 'Sick', 'Quarantined') --- lay tu enums.py, enclosureId: str, createAt: datetime, updateAt: datetime.

    -foods: idFood: str, nameFood: str, typeFood('Meat', 'Plant', 'Fish', 'Insect') --- lay tu enums.py, caloriesPerUnit

    -feedRecords: idFeedRecord: str, animalIdFeedRecord: str, foodId: str, quantity: int, feedAt: datetime

    -managers: id: str, name: str, userName: str, password: str, role('Staff', 'Manager') --- lay tu enums.py


- NHIEM VU:
    - NHI: testing --- du an hoan thanh thi viet unit-test cho du an
    - NGUYEN: code tang serializers (chi code cac file create) --- tham khao code mau ngon ngu TS
    - TIEN: code tang serializers (chi code cac file update) --- tham khao code mau ngon ngu TS
    - KHOI: code tang services: xu li oop theo nhu mo ta o tren

* LUU Y:
    - DAT TEN THEO NHU YEU CAU O TREN KHONG DUOC KHAC
    - MOI CLASS, MOI DEF CODE RA DEU PHAI CHU THICH CHUC NANG --- CHU THICH LUON VONG FOR, IF, WHILE DUNG DE XU LI TAC VU GI (PHAI RO RANG)
    - DAT TEN HAM, ... THEO QUY TAC CAMEL CASE VA HOAN TOAN SU DUNG TIENG ANH (BAT BUOC)
    - DEN HET NGAY 8/10/2025 PHAI PUSH TAT CA CODE CUA DU AN PYTHON PHAT HIEN DO VAT LEN CODE DE T CHINH SUA --- SAU DO CLONE NAY VE DE LAM
    - CAC CHUC NANG CUA CAC FILE VA NHIEM VU DA CHU THICH O TREN (CODE VI DU O LINK GITHUB: https://github.com/TiCoder-coder/OOP_TS.git)
    - KHI LAM MOI NGUOI LAM MOT CLASS NAO DO VI DU animals, ... ROI PUSH LEN GIT TRUOC, TAO KIEM TRA DUNG FORM THI SE NHAN LEN NHOM VA TIEP TUC CODE FILE DO

