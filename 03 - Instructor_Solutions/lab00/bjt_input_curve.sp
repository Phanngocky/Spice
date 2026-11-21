* BJT INPUT CURVE - Dac Tuyen Ngo Vao Ib(Vbe) cua BJT 2N3904
* Mon hoc: Thuc hanh Thiet ke VLSI (5505382) - DH Su pham Ky thuat Da Nang
* Tac gia: Phan Ngoc Ky (2026)

.title Input Characteristic Curve Ib vs Vbe (2N3904 NPN)

* --- NGUON QUET AP BASE-EMITTER ---
Vbe 2 0 DC 0.7V
* Co dinh Vce de do dac tuyen vao (thuong lay Vce >= 1V hoac Vce = 5V)
Vce 3 0 DC 5.0V

* --- BJT TRANSISTOR ---
Q1 3 2 0 Q2N3904

* --- MODEL 2N3904 ---
.model Q2N3904 NPN(Is=1e-14 Bf=160 Vaf=74 Ikf=0.1 Xtb=1.5 Br=1.0 Nc=2
+ Isc=0 Ikr=0 Rc=1 Cjc=4p Mjc=0.333 Vjc=0.75 Fc=0.5 Cje=8p Mje=0.333
+ Vje=0.75 Tr=30.3n Tf=400p Itf=0.6 Vtf=1.7 Xtf=3 Rb=10)

* --- PHAN TICH DC SWEEP ---
* Quet Vbe tu 0 den 1.0V, buoc 5mV
.dc Vbe 0 1.0 0.005

* --- DO DIEN AP NGUONG BAT DAU DAN ---
* Tim dien ap Vbe khi dong Ib dat 10uA
.meas dc Vbe_at_10uA WHEN I(Q1:B)=10u
.meas dc Vbe_at_20uA WHEN I(Q1:B)=20u

.end
