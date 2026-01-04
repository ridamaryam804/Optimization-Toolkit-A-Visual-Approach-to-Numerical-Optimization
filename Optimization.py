import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

# Streamlit settings
st.set_page_config(page_title="📈 Optimization Toolkit", layout="centered")

# Initialize session state
if "steps" not in st.session_state:
    st.session_state.steps = []
if "results" not in st.session_state:
    st.session_state.results = {}

# Function parser
def parse_function(expr_str):
    x = sp.Symbol('x')
    f_expr = sp.sympify(expr_str)
    f = sp.lambdify(x, f_expr, "numpy")
    f_prime = sp.lambdify(x, sp.diff(f_expr, x), "numpy")
    f_double_prime = sp.lambdify(x, sp.diff(f_expr, x, 2), "numpy")
    return f, f_prime, f_double_prime, f_expr

# Plot function path
def plot_path(f, path, title, color='blue', label=None):
    x_vals = np.linspace(min(path)-5, max(path)+5, 400)
    y_vals = f(x_vals)

    plt.plot(x_vals, y_vals, 'k--', label='f(x)')
    plt.plot(path, f(np.array(path)), marker='o', color=color, label=label)
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    if label:
        plt.legend()
    st.pyplot(plt.gcf())
    plt.clf()

# Optimization methods
def golden_section_search(f, a, b, tol, max_iter):
    steps = []
    gr = (np.sqrt(5) + 1) / 2
    for _ in range(max_iter):
        if abs(b - a) < tol:
            break
        c = b - (b - a) / gr
        d = a + (b - a) / gr
        steps.append((a, b, c, d, f(c), f(d)))
        if f(c) < f(d):
            b = d
        else:
            a = c
    return (b + a) / 2, steps

def newtons_method(f, f_prime, f_double_prime, x0, tol, max_iter):
    steps = []
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        fpx = f_prime(x)
        fppx = f_double_prime(x)
        if fppx == 0: break
        x_new = x - fpx / fppx
        steps.append((x, fx))
        if abs(x_new - x) < tol: break
        x = x_new
    return x, steps

def gradient_descent(f, f_prime, x0, alpha, tol, max_iter):
    steps = []
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        grad = f_prime(x)
        x_new = x - alpha * grad
        steps.append((x, fx))
        if abs(x_new - x) < tol: break
        x = x_new
    return x, steps

# Header
st.title("📈 Optimization Toolkit")

# Function input
st.markdown("### ✍️ Enter the function f(x)")
func_input = st.text_input("Function (e.g., `x**2 + 4*x + 5`):", value="x**2 + 4*x + 5")
try:
    f, f_prime, f_double_prime, f_expr = parse_function(func_input)
except:
    st.error("❌ Invalid function. Please correct the expression.")
    st.stop()

# Sidebar
st.sidebar.header("⚙️ Settings & Preferences")
method = st.sidebar.radio("🔍 Select Optimization Method", [
    "Golden Section Search", "Newton's Method", "Gradient Descent", "Compare All Methods"
])
theme = st.sidebar.radio("🎨 Plot Theme", ["Light", "Dark"])
plt.style.use("seaborn-v0_8-dark" if theme == "Dark" else "seaborn-v0_8-colorblind")
tolerance = float(st.sidebar.selectbox("Precision Tolerance", ["1e-2", "1e-3", "1e-5", "1e-8"], index=2))
max_iter = st.sidebar.slider("Maximum Iterations", 5, 100, 50)
show_logs = st.sidebar.checkbox("Show Detailed Logs", value=True)

# Real-world applications
st.sidebar.markdown("---")
st.sidebar.markdown("📂 **Applications of Optimization**")

application = st.sidebar.selectbox("Choose Application Area", [
    "— Select —",
    "1. Portfolio Optimization (Gradient Descent)",
    "2. Machine Learning Cost Minimization (Gradient Descent)",
    "3. Engineering Design Optimization (Golden Section)",
    "4. Root Finding in Physics (Newton’s Method)",
    "5. Power Grid Optimization (Newton’s Method)"
])

uploaded_file = st.sidebar.file_uploader("📤 Upload Data File (.csv or .xlsx)", type=["csv", "xlsx"])
data = None
if uploaded_file:
    try:
        data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        st.sidebar.success("✅ File uploaded successfully!")
    except:
        st.sidebar.error("❌ Failed to load file")

if application != "— Select —":
    st.sidebar.markdown("### 📘 Application Description")
    descriptions = {
        "Portfolio": "Used in finance to optimize asset allocations. Gradient Descent minimizes risk-return functions.",
        "Machine Learning": "Gradient Descent trains models by minimizing the cost function (loss).",
        "Engineering Design": "Golden Section optimizes parameters like shape or material with no need for derivatives.",
        "Root Finding": "Newton’s Method solves equations in physics like Kepler's equation.",
        "Power Grid": "Newton’s Method solves load flow equations in electrical grid systems."
    }
    for key in descriptions:
        if key in application:
            st.sidebar.write(descriptions[key])
            break

# File-based Optimization
if data is not None:
    st.markdown("## 📊 Uploaded Dataset")
    st.dataframe(data)
    numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        selected_col = st.selectbox("Select column to optimize (as f(x))", numeric_cols)
        y = data[selected_col].dropna().values
        x = np.arange(len(y))

        st.line_chart(pd.DataFrame({selected_col: y}))

        st.markdown("### Running Gradient Descent on Uploaded Column")
        x0 = st.number_input("Initial Point (x₀) for Uploaded Data", value=0.0)
        alpha = st.number_input("Learning Rate (α)", value=0.01)

        # Fit polynomial of degree 2 and run GD
        coeffs = np.polyfit(x, y, 2)
        func_expr = f"{coeffs[0]}*x**2 + {coeffs[1]}*x + {coeffs[2]}"
        f2, f2_prime, _, _ = parse_function(func_expr)
        x_opt, steps = gradient_descent(f2, f2_prime, x0, alpha, tolerance, max_iter)

        st.success(f"📍 Optimized x ≈ {x_opt:.6f}")
        st.dataframe(pd.DataFrame(steps, columns=["x", "f(x)"]))
        plot_path(f2, [s[0] for s in steps] + [x_opt], "Optimization on Uploaded Column", color='purple')

# Export results
if st.sidebar.button("📁 Export Results to CSV"):
    results = []
    for method_name, steps in st.session_state.results.items():
        for i, x in enumerate(steps):
            results.append({"Method": method_name, "Step": i+1, "x": x, "f(x)": f(x)})
    df = pd.DataFrame(results)
    csv = df.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button("⬇ Download CSV", csv, file_name="optimization_results.csv", mime="text/csv")

# Method execution
if method == "Golden Section Search":
    st.subheader("🔸 Golden Section Search")
    a = st.number_input("Lower Bound (a)", value=-10.0)
    b = st.number_input("Upper Bound (b)", value=10.0)
    if st.button("Run Golden Section Search"):
        x_opt, steps = golden_section_search(f, a, b, tolerance, max_iter)
        st.session_state.results["Golden"] = [s[2] for s in steps] + [x_opt]
        st.success(f"✅ x ≈ {x_opt:.6f}")
        st.dataframe(pd.DataFrame(steps, columns=["a", "b", "c", "d", "f(c)", "f(d)"]))
        plot_path(f, [s[2] for s in steps] + [x_opt], "Golden Section Path", color="orange")

elif method == "Newton's Method":
    st.subheader("🔹 Newton’s Method")
    x0 = st.number_input("Initial Guess (x₀)", value=0.0)
    if st.button("Run Newton’s Method"):
        x_opt, steps = newtons_method(f, f_prime, f_double_prime, x0, tolerance, max_iter)
        st.session_state.results["Newton"] = [s[0] for s in steps] + [x_opt]
        st.success(f"✅ x ≈ {x_opt:.6f}")
        st.dataframe(pd.DataFrame(steps, columns=["x", "f(x)"]))
        plot_path(f, [s[0] for s in steps] + [x_opt], "Newton's Method Path", color="green")

elif method == "Gradient Descent":
    st.subheader("🔹 Gradient Descent")
    x0 = st.number_input("Initial Point (x₀)", value=0.0)
    alpha = st.number_input("Learning Rate (α)", value=0.1)
    if st.button("Run Gradient Descent"):
        x_opt, steps = gradient_descent(f, f_prime, x0, alpha, tolerance, max_iter)
        st.session_state.results["GD"] = [s[0] for s in steps] + [x_opt]
        st.success(f"✅ x ≈ {x_opt:.6f}")
        st.dataframe(pd.DataFrame(steps, columns=["x", "f(x)"]))
        plot_path(f, [s[0] for s in steps] + [x_opt], "Gradient Descent Path", color="blue")

elif method == "Compare All Methods":
    st.subheader("📊 Compare Optimization Paths")
    available = st.session_state.results.keys()
    if len(available) < 2:
        st.warning("⚠️ Run at least 2 methods before comparing.")
    else:
        colors = {'Golden': 'orange', 'Newton': 'green', 'GD': 'blue'}
        for name in available:
            plot_path(f, st.session_state.results[name], f"{name} Path", color=colors.get(name, 'gray'), label=name)
