# pip install pandas matplotlib
import pandas as pd
import matplotlib.pyplot as plt

SPEC = {
    "min_voltage": 3.1,
    "max_voltage": 3.5,
    "max_current": 0.45,
    "max_power": 1.5,
}

df = pd.read_csv("module_power_characterization.csv")

df["voltage_pass"] = df["measured_voltage"].between(
    SPEC["min_voltage"], SPEC["max_voltage"]
)

df["current_pass"] = df["measured_current"] <= SPEC["max_current"]
df["power_pass"] = df["power_w"] <= SPEC["max_power"]

df["overall_pass"] = (
    df["voltage_pass"] &
    df["current_pass"] &
    df["power_pass"]
)

df.to_csv("validation_results_with_limits.csv", index=False)

summary = {
    "total_tests": len(df),
    "passed": int(df["overall_pass"].sum()),
    "failed": int((~df["overall_pass"]).sum()),
}

with open("validation_summary.txt", "w") as f:
    f.write("Electrical Validation Summary\n")
    f.write("=============================\n")
    for k, v in summary.items():
        f.write(f"{k}: {v}\n")

plt.figure()
plt.plot(df["set_voltage"], df["power_w"], marker="o")
plt.xlabel("Set Voltage")
plt.ylabel("Measured Power W")
plt.title("Power Characterization")
plt.grid(True)
plt.savefig("power_characterization.png", dpi=200)

print(summary)
