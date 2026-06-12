# pip install pyvisa pandas
import pyvisa
import pandas as pd
import time
from datetime import datetime

rm = pyvisa.ResourceManager()

psu = rm.open_resource("USB0::PSU_ID::INSTR")
dmm = rm.open_resource("USB0::DMM_ID::INSTR")

results = []

voltages = [1.8, 2.5, 3.0, 3.3, 3.6]

for v in voltages:
    psu.write(f"VOLT {v}")
    psu.write("CURR 1.0")
    psu.write("OUTP ON")
    time.sleep(0.5)

    measured_v = float(dmm.query("MEAS:VOLT:DC?"))
    measured_i = float(psu.query("MEAS:CURR?"))
    power = measured_v * measured_i

    results.append({
        "timestamp": datetime.now().isoformat(),
        "set_voltage": v,
        "measured_voltage": measured_v,
        "measured_current": measured_i,
        "power_w": power,
    })

psu.write("OUTP OFF")

df = pd.DataFrame(results)
df.to_csv("module_power_characterization.csv", index=False)
print(df)
