
<p align="center">
	<img src="https://img.icons8.com/ios-filled/100/ECG.png" width="80" alt="ECG Icon"/>
</p>

# 🩺 ECG Signal Quality Assessment App

<p align="center">
	<b>Automated, reliable, and visually-rich ECG quality analysis for clinicians, researchers, and data scientists.</b>
</p>

---

## 🚀 Overview

This project provides a modern, production-ready web app and Python toolkit for:

- 🧹 **ECG Signal Quality Assessment**: Automated checks for noise, artifacts, baseline wander, clipping, lead-off, amplitude, and missing data.
- 📊 **Interactive Visualization**: Upload, view, and explore ECG signals in your browser.
- 📝 **Metrics Dashboard**: Clear pass/fail badges, explanations, and actionable recommendations.
- 🧑‍⚕️ **Clinical & Research Relevance**: Ensures only high-quality ECGs are used for diagnosis or machine learning.

---

## ✨ Features

|  | Feature | Description |
|--|---------|-------------|
| ⚡ | **Automated Quality Checks** | Detects noise, artifacts, baseline drift, clipping, lead-off, amplitude, and missing data |
| 📈 | **Signal Visualization** | Interactive time-domain plots with zoom and pan |
| 🟢 | **Pass/Fail Badges** | Instantly see which metrics pass or need attention |
| 🧑‍💻 | **Web & Notebook Ready** | Use as a Streamlit app or import functions in Python notebooks |
| ☁️ | **Easy Deployment** | Docker, Heroku, and Streamlit Community Cloud support |
| 🔒 | **Open Source** | MIT License, ready for extension |

---

## 🏥 Why ECG Quality Assessment Matters

<img src="https://img.icons8.com/ios-filled/50/heart-with-pulse.png" width="32" align="left" style="margin-right:10px;"/>

Poor-quality ECGs can lead to misdiagnosis, missed arrhythmias, and unreliable machine learning models. This app:

- Flags signals that need cleaning or reacquisition
- Saves time for clinicians and researchers
- Improves the reliability of downstream analysis

---

## 🛠️ Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/ecg-quality-app.git
cd ecg-quality-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Web App

```bash
streamlit run app.py
```

### 3. Or Use in Python

```python
from ecg_quality import assess_ecg_quality
quality = assess_ecg_quality(signal, fs)
print(quality)
```

---

## 🖥️ Outputs

- 📊 Interactive dashboard with all quality metrics
- 🟢/🔴 Pass/fail badges for each check
- 📁 Downloadable summary CSV
- 🖼️ PNG plots of ECG and power spectrum

---

## 📦 Deployment

- **Docker**: `docker build -t ecg-quality-app . && docker run -p 8501:8501 ecg-quality-app`
- **Heroku/Streamlit Cloud**: Ready with `Procfile` and `.streamlit/config.toml`

---

## 🤝 Contributing

Pull requests, issues, and feature suggestions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

<p align="center">
	<img src="https://img.icons8.com/ios-filled/50/000000/heart-monitor.png" width="32"/>
	<br/>
	<b>Empowering better heart health through open-source signal quality tools.</b>
</p>
