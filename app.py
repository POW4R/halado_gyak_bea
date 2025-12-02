import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

st.title("Interaktív Lineáris Regresszió")

st.write("Töltsd fel az adatfájlt, majd válassz X és Y oszlopot!")

# ----------------------------
# CSV feltöltése
# ----------------------------
uploaded_file = st.file_uploader("Tölts fel egy CSV fájlt", type=["csv"])

df = None
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Adatok sikeresen beolvasva!")
    st.dataframe(df)

# ----------------------------
# X és Y oszlop kiválasztása
# ----------------------------
if df is not None:
    st.subheader("Válaszd ki az X és Y oszlopokat!")

    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_columns) < 2:
        st.error("Legalább két numerikus oszlop szükséges!")
    else:
        x_col = st.selectbox("X (input):", numeric_columns)
        y_col = st.selectbox("Y (output):", numeric_columns)


# ----------------------------
# Scatter plot + regressziós modell
# ----------------------------
if df is not None and "x_col" in locals() and "y_col" in locals():
    st.subheader("Scatter Plot + Regressziós Egyenes")

    # Adatok előkészítése
    X = df[[x_col]].values
    y = df[[y_col]].values

    # Modell tanítása
    model = LinearRegression()
    model.fit(X, y)

    # Előrejelzett értékek az egyenes megrajzolásához
    x_line = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
    y_line = model.predict(x_line)

    # Matplotlib grafikon kirajzolása
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(X, y, color="blue", label="Adatpontok")
    ax.plot(x_line, y_line, color="red", linewidth=2, label="Regressziós egyenes")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.legend()

    st.pyplot(fig)

    # Modell paraméterek kiírása
    st.write("### Modell paraméterek")
    st.write(f"**Intercept:** {model.intercept_[0]:.4f}")
    st.write(f"**Slope (Coef):** {model.coef_[0][0]:.8f}")

    # MSE
    mse = mean_squared_error(y, model.predict(X))
    st.write(f"**MSE (Mean Squared Error):** {mse:.6f}")

# ----------------------------
# Interaktív előrejelzés sliderrel
# ----------------------------
st.subheader("Interaktív előrejelzés")

pred_value = st.slider(
    f"Válassz egy {x_col} értéket a predikcióhoz:",
    min_value=float(X.min()),
    max_value=float(X.max()),
    value=float(X.mean()),
    step=float((X.max() - X.min()) / 100)
)

pred_input = np.array([[pred_value]])
pred_output = model.predict(pred_input)[0][0]

st.write(f"### Becsült {y_col}: **{pred_output:.4f}**")

