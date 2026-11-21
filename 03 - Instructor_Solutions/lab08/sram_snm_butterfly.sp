* LAB 08: 6T SRAM STATIC NOISE MARGIN (SNM) BUTTERFLY CURVE (.DC)
* Cong nghe: MOSIS SCMOS C5N 0.5um (lambda = 0.30um, VDD = 5.0V)
* Muc tieu: Mo phong dac tuyen VTC che do Hold (WL=0V) va Read (WL=5V, BL=BLB=5V)
*          ve duong cong buom (Butterfly Curve) xac dinh Hold SNM va Read SNM

.include "../../04 - Models_and_Libraries/C5_models.txt"

Vdd vdd 0 DC 5.0
Vwl_read wl_read 0 DC 5.0
Vbl bl 0 DC 5.0
Vblb blb 0 DC 5.0

* ==============================================================
* CHE DO 1: HOLD SNM (WL = 0V, ACCESS NGAT)
* ==============================================================
* Inverter 1 (Hold): Ngo vao Vin1, ngo ra Vq_hold
Mp_l1 vq_hold Vin1 vdd vdd P W=0.6u L=0.6u
Mn_d1 vq_hold Vin1 0   0   N W=2.4u L=0.6u

* Inverter 2 (Hold): Ngo vao Vin2, ngo ra Vqb_hold
Mp_l2 vqb_hold Vin2 vdd vdd P W=0.6u L=0.6u
Mn_d2 vqb_hold Vin2 0   0   N W=2.4u L=0.6u

* ==============================================================
* CHE DO 2: READ SNM (WL = 5.0V, BL = BLB = 5.0V)
* ==============================================================
* Nua o nho 1 (Read): Ngo vao Vin1, ngo ra Vq_read
Mp_l1_r vq_read Vin1 vdd vdd P W=0.6u L=0.6u
Mn_d1_r vq_read Vin1 0   0   N W=2.4u L=0.6u
Mn_ax1_r bl wl_read vq_read 0 N W=1.2u L=0.6u

* Nua o nho 2 (Read): Ngo vao Vin2, ngo ra Vqb_read
Mp_l2_r vqb_read Vin2 vdd vdd P W=0.6u L=0.6u
Mn_d2_r vqb_read Vin2 0   0   N W=2.4u L=0.6u
Mn_ax2_r blb wl_read vqb_read 0 N W=1.2u L=0.6u

* ==============================================================
* PHAN TICH DC SWEEP
* ==============================================================
* Quet Vin1 tu 0V den 5V
Vin1 Vin1 0 DC 0.0
Vin2 Vin2 0 DC 0.0

.dc Vin1 0 5.0 0.01

.print dc V(vq_hold) V(vq_read)

.end
