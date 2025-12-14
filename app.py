import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from ecg_quality import assess_ecg_quality

def render_header():
    st.set_page_config(
        page_title="ECG Signal Quality Assessment",
        layout="wide"
    )
    st.title("ECG Signal Quality Assessment Tool")
    st.subheader("Automated evaluation of ECG signal reliability")
    st.markdown(
        "This tool analyzes uploaded ECG signals for common quality issues before clinical interpretation or machine learning. "
        "Assessing signal quality helps ensure reliable diagnosis and robust modeling by flagging noise, artifacts, and other problems."
    )

def render_upload_section():
    st.header("1. Upload ECG Data")
    uploaded_file = st.file_uploader(
        "Upload a single-lead ECG file (.csv or .txt)", 
        type=["csv", "txt"]
    )
    fs = st.number_input("Sampling Frequency (Hz)", min_value=10, max_value=5000, value=360)
    lead_name = st.text_input("Lead Name (optional)", value="Lead I")
    return uploaded_file, fs, lead_name

def load_ecg_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            st.error("No numeric columns found in the uploaded file.")
            return None
        sig = df[numeric_cols[0]].astype(float).values
        return sig
    except Exception as e:
        st.error(f"Error loading ECG data: {e}")
        return None

def render_signal_plot(sig, fs, show_filtered=False):
    st.header("2. Signal Visualization")
    t = np.arange(len(sig)) / fs
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=sig, mode='lines', name='Raw ECG'))
    fig.update_layout(
        title="ECG Signal (Time Domain)",
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

def status_badge(status):
    if status is True:
        return "✅ Pass"
    elif status is False:
        return "❌ Fail"
    else:
        return "⚠ Warning"

def metric_explanation(metric):
    explanations = {
        "noise_ok": "Checks for high-frequency noise or artifacts that may distort the ECG.",
        "baseline_wander_ok": "Detects low-frequency drift in the ECG baseline (e.g., from breathing or movement).",
        "clipping_ok": "Checks for flat segments at signal limits, indicating possible hardware saturation.",
        "lead_off_ok": "Detects if the electrode is disconnected (flatline or near-zero variance).",
        "amplitude_ok": "Ensures the ECG amplitude is within physiological limits.",
        "missing_ok": "Checks for missing or invalid (NaN) data points."
    }
    return explanations.get(metric, "")

def render_quality_metrics(results):
    st.header("3. Quality Metrics Results")
    metrics = [
        ("Noise / Artifact Detection", "noise_ok"),
        ("Baseline Wander", "baseline_wander_ok"),
        ("Signal Clipping", "clipping_ok"),
        ("Lead-Off Detection", "lead_off_ok"),
        ("Amplitude Range Check", "amplitude_ok"),
        ("Missing Data Detection", "missing_ok"),
    ]
    cols = st.columns(len(metrics))
    for i, (label, key) in enumerate(metrics):
        with cols[i]:
            st.markdown(f"**{label}**")
            badge = status_badge(results[key])
            color = "green" if results[key] else "red"
            st.markdown(f"<span style='color:{color};font-size:1.2em'>{badge}</span>", unsafe_allow_html=True)
            st.caption(metric_explanation(key))

def render_overall_summary(results):
    st.header("4. Overall Quality Summary & Recommendations")
    all_ok = results.get("all_ok", False)
    n_pass = sum([results[k] for k in results if k.endswith("_ok")])
    n_total = len([k for k in results if k.endswith("_ok")])
    score = int(100 * n_pass / n_total)
    if all_ok:
        label = "Good"
        msg = "This ECG signal is suitable for clinical analysis."
        color = "green"
    elif score >= 67:
        label = "Fair"
        msg = "This ECG signal is usable but may require cleaning."
        color = "orange"
    else:
        label = "Poor"
        msg = "This ECG signal requires cleaning or reacquisition."
        color = "red"
    st.markdown(f"### **Overall Quality Score:** <span style='color:{color}'>{score}% ({label})</span>", unsafe_allow_html=True)
    st.info(msg)
    failed = [k for k in results if k.endswith("_ok") and not results[k]]
    if failed:
        st.warning("**Recommended Actions:**")
        for k in failed:
            st.write(f"- {metric_explanation(k)}")

def main():
    render_header()
    uploaded_file, fs, lead_name = render_upload_section()
    if uploaded_file:
        with st.spinner("Loading and analyzing ECG data..."):
            sig = load_ecg_data(uploaded_file)
            if sig is not None:
                render_signal_plot(sig, fs)
                results = assess_ecg_quality(sig, fs)
                render_quality_metrics(results)
                render_overall_summary(results)
    else:
        st.info("Please upload an ECG file to begin.")

if __name__ == "__main__":
    main()
