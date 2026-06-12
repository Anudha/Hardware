# pip install pyvisa
import pyvisa
import time

rm = pyvisa.ResourceManager()
print("Detected instruments:")
for r in rm.list_resources():
    print(" ", r)

scope = rm.open_resource("USB0::YOUR_SCOPE_ID::INSTR")
psu = rm.open_resource("USB0::YOUR_POWER_SUPPLY_ID::INSTR")

print("Scope:", scope.query("*IDN?"))
print("PSU:", psu.query("*IDN?"))

psu.write("VOLT 3.3")
psu.write("CURR 0.5")
psu.write("OUTP ON")
time.sleep(1)

scope.write(":MEASure:VPP?")
vpp = float(scope.read())

scope.write(":MEASure:FREQuency?")
freq = float(scope.read())

psu.write("OUTP OFF")

print(f"Measured Vpp: {vpp:.3f} V")
print(f"Measured Freq: {freq:.3f} Hz")
