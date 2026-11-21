* BJT OUTPUT FAMILY - Ho Dac Tuyen Ngo Ra Ic(Vce, Ib) cua BJT 2N3904
* Mon hoc: Thuc hanh Thiet ke VLSI (5505382) - DH Su pham Ky thuat Da Nang
* Tac gia: Phan Ngoc Ky (2026)

.title Output Characteristic Family Ic vs Vce at Parametric Ib (2N3904)

* --- NGUON BOM DONG BASE (Tham so quet ngoai) ---
Ib 0 2 DC 10u

* --- NGUON QUET AP COLLECTOR-EMITTER (Quet chinh) ---
Vce 3 0 DC 0V

* --- BJT TRANSISTOR ---
Q1 3 2 0 Q2N3904

* --- MODEL 2N3904 ---
.model Q2N3904 NPN(Is=1e-14 Bf=160 Vaf=74 Ikf=0.1 Xtb=1.5 Br=1.0 Nc=2
+ Isc=0 Ikr=0 Rc=1 Cjc=4p Mjc=0.333 Vjc=0.75 Fc=0.5 Cje=8p Mje=0.333
+ Vje=0.75 Tr=30.3n Tf=400p Itf=0.6 Vtf=1.7 Xtf=3 Rb=10)

* --- PHAN TICH DC SWEEP 2 THAM SO ---
* Bien chinh: Vce tu 0V den 10V buoc 0.05V
* Bien tham so: Ib tu 10uA den 50uA buoc 10uA (5 duong dac tuyen)
.dc Vce 0 10 0.05 Ib 10u 50u 10u

* --- DO HE SO KHUECH DAI BETA TAI Vce = 5V ---
.meas dc Ic_at_Vce5 WHEN V(3)=5.0

.end
