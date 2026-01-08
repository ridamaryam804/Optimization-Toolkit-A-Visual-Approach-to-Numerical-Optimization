import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

# Streamlit settings
st.set_page_config(page_title="📈 Optimization Toolkit", layout="centered")

# CUSTOM CSS FOR AESTHETIC DESIGN
st.markdown("""
<style>
    /* Main Background - Sky Blue Gradient */
    .stApp {
        background: linear-gradient(135deg, #87CEEB 0%, #E0F7FF 50%, #B3E0FF 100%);
        background-attachment: fixed;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Title Styling - Bold and Shiny with DARK BLUE COLOR */
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #00008B, #1E3A8A, #00008B);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-shadow: 0 2px 20px rgba(30, 144, 255, 0.4);
        text-align: center;
        margin-bottom: 1rem;
        padding: 20px;
        letter-spacing: 1px;
    }
    
    /* Subheaders with shine effect */
    h2, h3 {
        color: #1E3A8A !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 3px rgba(255,255,255,0.9);
        background: linear-gradient(to right, rgba(255,255,255,0.9), rgba(135,206,235,0.3));
        padding: 15px 20px;
        border-radius: 15px;
        border-left: 6px solid #1E90FF;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-top: 20px !important;
    }
    
    /* Input Fields - Glossy and Shiny */
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #87CEEB !important;
        border-radius: 20px !important;
        padding: 15px 25px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        box-shadow: 0 5px 20px rgba(135, 206, 235, 0.4), 
                    inset 0 2px 5px rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease !important;
        color: #1E3A8A !important;
    }
    
    .stTextInput>div>div>input:focus, 
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #1E90FF !important;
        box-shadow: 0 0 25px rgba(30, 144, 255, 0.6), 
                    inset 0 2px 5px rgba(255, 255, 255, 0.9) !important;
        transform: scale(1.02) !important;
        outline: none !important;
    }
    
    /* Labels for inputs */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-weight: 700 !important;
        color: #1E3A8A !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
    }
    
    /* Buttons - Gradient and Shiny with 3D effect */
    .stButton>button {
        background: linear-gradient(145deg, #1E90FF, #87CEEB, #1E90FF) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 15px 35px !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        box-shadow: 0 6px 20px rgba(30, 144, 255, 0.5),
                    0 3px 0 rgba(30, 144, 255, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100%;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 30px rgba(30, 144, 255, 0.7),
                    0 5px 0 rgba(30, 144, 255, 0.4) !important;
        background: linear-gradient(145deg, #1C86EE, #63B8FF, #1C86EE) !important;
    }
    
    .stButton>button:active {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(30, 144, 255, 0.5) !important;
    }
    
    /* Sidebar Styling - Glass morphism effect */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 4px solid #87CEEB !important;
        box-shadow: 10px 0 30px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Sidebar headers */
    .sidebar .sidebar-content {
        background: transparent !important;
    }
    
    /* Radio Buttons and Checkboxes - Modern cards */
    .stRadio>div, .stCheckbox>div {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        border: 2px solid rgba(135, 206, 235, 0.6) !important;
        box-shadow: 0 4px 15px rgba(135, 206, 235, 0.2) !important;
        margin: 10px 0 !important;
    }
    
    /* Success/Error Messages - Modern alerts */
    .stAlert {
        border-radius: 20px !important;
        border-left: 6px solid !important;
        background: rgba(255, 255, 255, 0.95) !important;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1) !important;
        padding: 20px !important;
        font-weight: 500 !important;
    }
    
    /* Success message specific */
    .stAlert[data-baseweb="notification"] {
        border-left-color: #4CAF50 !important;
    }
    
    /* Error message specific */
    .stAlert[data-baseweb="notification"].st-ae {
        border-left-color: #FF5252 !important;
    }
    
    /* Dataframe Styling - Glass card */
    .dataframe {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15) !important;
        border: 2px solid rgba(135, 206, 235, 0.5) !important;
        overflow: hidden !important;
    }
    
    .dataframe th {
        background: linear-gradient(45deg, #1E90FF, #87CEEB) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 15px !important;
        text-align: center !important;
    }
    
    .dataframe td {
        padding: 12px !important;
        text-align: center !important;
        border-bottom: 1px solid rgba(135, 206, 235, 0.3) !important;
    }
    
    .dataframe tr:hover {
        background-color: rgba(135, 206, 235, 0.1) !important;
    }
    
    /* Cloud Effect Decoration */
    .clouds {
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }
    
    .cloud {
        position: absolute;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 50%;
        box-shadow: 0 0 60px rgba(255, 255, 255, 0.8);
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% { transform: translateX(0) translateY(0); }
        25% { transform: translateX(100px) translateY(50px); }
        50% { transform: translateX(200px) translateY(0); }
        75% { transform: translateX(100px) translateY(-50px); }
        100% { transform: translateX(0) translateY(0); }
    }
    
    /* Card-like containers */
    .css-1r6slb0 {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 25px !important;
        padding: 30px !important;
        box-shadow: 0 10px 35px rgba(135, 206, 235, 0.25) !important;
        border: 2px solid rgba(135, 206, 235, 0.4) !important;
        margin: 20px 0 !important;
    }
    
    /* Plot containers - FIXED RGBA ERROR */
    .stPlotlyChart, .stPyplot {
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.15);
        border: 2px solid rgba(135, 206, 235, 0.5);
        margin: 20px 0;
    }
    
    /* Slider styling */
    .stSlider>div>div>div {
        background: linear-gradient(90deg, #87CEEB, #1E90FF) !important;
    }
    
    .stSlider>div>div>div>div {
        background: white !important;
        border: 3px solid #1E90FF !important;
        box-shadow: 0 0 15px rgba(30, 144, 255, 0.7) !important;
    }
    
    /* File uploader styling */
    .stFileUploader>div {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px dashed #87CEEB !important;
        border-radius: 20px !important;
        padding: 30px !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader>div:hover {
        border-color: #1E90FF !important;
        background: rgba(255, 255, 255, 0.95) !important;
        box-shadow: 0 10px 30px rgba(135, 206, 235, 0.3) !important;
    }
    
    /* Metric cards */
    .stMetric {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(135,206,235,0.2)) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1) !important;
        border: 2px solid rgba(135, 206, 235, 0.5) !important;
    }
    
    /* Divider styling */
    hr {
        border: none !important;
        height: 3px !important;
        background: linear-gradient(90deg, transparent, #87CEEB, transparent) !important;
        margin: 30px 0 !important;
    }
    
    /* Tooltip styling */
    .stTooltip {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #87CEEB !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
        color: #1E3A8A !important;
        font-weight: 500 !important;
    }
    
    /* Progress bar */
    .stProgress>div>div>div {
        background: linear-gradient(90deg, #87CEEB, #1E90FF) !important;
        border-radius: 10px !important;
    }
    
    /* Info boxes */
    .stInfo {
        background: linear-gradient(135deg, rgba(30, 144, 255, 0.1), rgba(135, 206, 235, 0.2)) !important;
        border-left: 6px solid #1E90FF !important;
    }
    
    /* Make all text bold and clear */
    p, li, span {
        font-weight: 500 !important;
        color: #1E3A8A !important;
        text-shadow: 0.5px 0.5px 1px rgba(255,255,255,0.8);
    }
</style>

<!-- Cloud Animation -->
<div class="clouds">
    <div class="cloud" style="width: 200px; height: 80px; top: 10%; left: 5%; animation-delay: 0s;"></div>
    <div class="cloud" style="width: 150px; height: 60px; top: 25%; right: 15%; animation-delay: 5s;"></div>
    <div class="cloud" style="width: 180px; height: 70px; bottom: 20%; left: 10%; animation-delay: 10s;"></div>
    <div class="cloud" style="width: 120px; height: 50px; bottom: 35%; right: 8%; animation-delay: 15s;"></div>
    <div class="cloud" style="width: 160px; height: 65px; top: 40%; left: 20%; animation-delay: 7s;"></div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "steps" not in st.session_state:
    st.session_state.steps = []
if "results" not in st.session_state:
    st.session_state.results = {}

# SHINY TITLE WITH DARK BLUE COLOR
st.markdown('<h1 class="main-title">📈 OPTIMIZATION TOOLKIT ✨</h1>', unsafe_allow_html=True)

# Function parser
def parse_function(expr_str):
    x = sp.Symbol('x')
    f_expr = sp.sympify(expr_str)
    f = sp.lambdify(x, f_expr, "numpy")
    f_prime = sp.lambdify(x, sp.diff(f_expr, x), "numpy")
    f_double_prime = sp.lambdify(x, sp.diff(f_expr, x, 2), "numpy")
    return f, f_prime, f_double_prime, f_expr

# Plot function path - FIXED RGBA ERROR
def plot_path(f, path, title, color='#1E90FF', label=None):
    x_vals = np.linspace(min(path)-5, max(path)+5, 400)
    y_vals = f(x_vals)

    # FIX: Use tuple instead of string for facecolor
    plt.figure(figsize=(12, 7))
    
    # Set background color
    fig = plt.gcf()
    fig.set_facecolor((0.97, 0.97, 0.97, 0.9))  # Light gray with alpha
    
    ax = plt.gca()
    
    # Gradient background
    ax.set_facecolor((0.98, 0.98, 0.98))  # Light gray
    
    # Plot function
    plt.plot(x_vals, y_vals, color='#1E3A8A', linestyle='--', 
             linewidth=2.5, label='f(x)', alpha=0.8)
    
    # Plot optimization path
    plt.plot(path, f(np.array(path)), marker='o', color=color, 
             markersize=10, linewidth=3.5, label=label, 
             markerfacecolor='white', markeredgewidth=2, markeredgecolor=color)
    
    # Mark optimum point
    if len(path) > 0:
        opt_x = path[-1]
        opt_y = f(opt_x)
        plt.scatter([opt_x], [opt_y], s=200, color='#FF5252', 
                   zorder=5, label='Optimum', edgecolors='white', linewidth=3)
    
    # Gradient fill under curve
    plt.fill_between(x_vals, y_vals, alpha=0.15, color=color)
    
    # Grid and labels
    plt.grid(True, alpha=0.2, linestyle='--')
    plt.title(title, fontsize=20, fontweight='bold', color='#1E3A8A', pad=20)
    plt.xlabel('x', fontsize=16, fontweight='bold', color='#1E3A8A')
    plt.ylabel('f(x)', fontsize=16, fontweight='bold', color='#1E3A8A')
    
    # Styling spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_color('#87CEEB')
    ax.spines['bottom'].set_color('#87CEEB')
    
    if label:
        plt.legend(fontsize=12, framealpha=0.95, loc='best', 
                  frameon=True, edgecolor='#1E90FF')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.clf()

# Optimization methods
def golden_section_search(f, a, b, tol, max_iter):
    steps = []
    gr = (np.sqrt(5) + 1) / 2
    for i in range(max_iter):
        if abs(b - a) < tol:
            break
        c = b - (b - a) / gr
        d = a + (b - a) / gr
        steps.append((i+1, a, b, c, d, f(c), f(d), abs(b - a)))
        if f(c) < f(d):
            b = d
        else:
            a = c
    return (b + a) / 2, steps

def newtons_method(f, f_prime, f_double_prime, x0, tol, max_iter):
    steps = []
    x = x0
    for i in range(max_iter):
        fx = f(x)
        fpx = f_prime(x)
        fppx = f_double_prime(x)
        if fppx == 0: 
            st.warning("⚠️ Second derivative is zero. Stopping iteration.")
            break
        x_new = x - fpx / fppx
        steps.append((i+1, x, fx, fpx, fppx, abs(x_new - x)))
        if abs(x_new - x) < tol: 
            break
        x = x_new
    return x, steps

def gradient_descent(f, f_prime, x0, alpha, tol, max_iter):
    steps = []
    x = x0
    for i in range(max_iter):
        fx = f(x)
        grad = f_prime(x)
        x_new = x - alpha * grad
        steps.append((i+1, x, fx, grad, abs(x_new - x)))
        if abs(x_new - x) < tol: 
            break
        x = x_new
    return x, steps

# Function input with shiny styling
st.markdown("### ✍️ ENTER THE FUNCTION f(x)")
col1, col2 = st.columns([3, 1])
with col1:
    func_input = st.text_input(
        "**Mathematical Function:**", 
        value="x**2 + 4*x + 5",
        help="Enter a mathematical function of x (e.g., x**3 - 3*x**2 + 5, sin(x), exp(x))"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    example_func = st.selectbox(
        "**Quick Examples:**",
        ["x**2 + 4*x + 5", "x**3 - 3*x**2 + 5", "sin(x)", "exp(-x**2)", "x**4 - 8*x**2 + 10"]
    )
    if st.button("Use Example"):
        func_input = example_func
        st.rerun()

try:
    f, f_prime, f_double_prime, f_expr = parse_function(func_input)
    st.success(f"✅ **Function parsed successfully:** `{f_expr}`")
    
    # Display function info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("f(x)", f"`{f_expr}`")
    with col2:
        st.metric("f'(x)", f"`{sp.diff(f_expr, sp.Symbol('x'))}`")
    with col3:
        st.metric("f''(x)", f"`{sp.diff(f_expr, sp.Symbol('x'), 2)}`")
        
except Exception as e:
    st.error(f"❌ **Invalid function:** {str(e)}. Please enter a valid mathematical expression.")
    st.stop()

# Sidebar with improved styling
st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #1E90FF, #87CEEB); 
                padding: 25px; 
                border-radius: 20px;
                color: white;
                margin-bottom: 25px;
                text-align: center;
                box-shadow: 0 8px 30px rgba(30, 144, 255, 0.5);
                border: 3px solid white;'>
        <h2 style='color: white; margin: 0; font-size: 24px;'>⚙️ SETTINGS</h2>
        <p style='margin: 5px 0 0 0; opacity: 0.9;'>Configure your optimization parameters</p>
    </div>
""", unsafe_allow_html=True)

# Method selection with icons
method = st.sidebar.radio(
    "**🔍 SELECT OPTIMIZATION METHOD**", 
    [
        "Golden Section Search", 
        "Newton's Method", 
        "Gradient Descent", 
        "Compare All Methods"
    ],
    index=1,  # Default to Newton's Method
    help="Choose the optimization algorithm to use"
)

# REMOVED THEME SELECTION - Only one theme now

# Parameters in columns
st.sidebar.markdown("### **📊 OPTIMIZATION PARAMETERS**")

col1, col2 = st.sidebar.columns(2)
with col1:
    tolerance = float(st.selectbox(
        "**Precision Tolerance**", 
        ["1e-2", "1e-3", "1e-5", "1e-8"], 
        index=2,
        help="Stop when change is less than this value"
    ))
with col2:
    max_iter = st.slider(
        "**Maximum Iterations**", 
        5, 200, 75, 5,  # Changed default to 75
        help="Maximum number of iterations"
    )

show_logs = st.sidebar.checkbox("**📋 Show Detailed Iteration Logs**", value=True)

# Real-world applications section
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #FF7F50, #FFA07A); 
                padding: 20px; 
                border-radius: 20px;
                color: white;
                margin: 20px 0;
                text-align: center;
                box-shadow: 0 8px 30px rgba(255, 127, 80, 0.4);
                border: 3px solid white;'>
        <h3 style='color: white; margin: 0;'>📂 REAL-WORLD APPLICATIONS</h3>
    </div>
""", unsafe_allow_html=True)

application = st.sidebar.selectbox(
    "**Choose Application Area**",
    [
        "— Select —",
        "1. 📊 Portfolio Optimization (Gradient Descent)",
        "2. 🤖 Machine Learning Cost Minimization (Gradient Descent)",
        "3. 🏗️ Engineering Design Optimization (Golden Section)",
        "4. ⚛️ Root Finding in Physics (Newton's Method)",
        "5. ⚡ Power Grid Optimization (Newton's Method)"
    ],
    index=4  # Default to Power Grid Optimization
)

# File uploader with styling and error handling
st.sidebar.markdown("### **📤 UPLOAD DATA FILE (OPTIONAL)**")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file", 
    type=["csv", "xlsx"],
    help="Upload data for optimization analysis (optional)"
)

data = None
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        st.sidebar.success(f"✅ **File uploaded successfully!**\n{len(data)} rows × {len(data.columns)} columns")
    except Exception as e:
        st.sidebar.error(f"❌ Failed to load file: {str(e)}")
else:
    # Show message when no file is uploaded
    st.sidebar.info("ℹ️ **No file uploaded.** You can still use the toolkit with manual function input.")

# Application description
if application != "— Select —":
    st.sidebar.markdown("### **📘 APPLICATION DESCRIPTION**")
    descriptions = {
        "Portfolio": "**Portfolio Optimization:** Used in finance to optimize asset allocations. Gradient Descent minimizes risk-return functions to find optimal portfolio weights.",
        "Machine Learning": "**Machine Learning:** Gradient Descent trains models by minimizing the cost function (loss). This is fundamental in neural networks and linear regression.",
        "Engineering Design": "**Engineering Design:** Golden Section optimizes parameters like shape or material properties where derivatives are not available or expensive to compute.",
        "Root Finding": "**Physics Applications:** Newton's Method solves equations in physics like Kepler's equation for orbital mechanics or finding equilibrium points.",
        "Power Grid": "**Power Systems:** Newton's Method solves load flow equations in electrical grid systems to ensure stable and efficient power distribution."
    }
    
    for key in descriptions:
        if key in application:
            st.sidebar.info(descriptions[key])
            break

# Main content area
st.markdown("---")

# File-based Optimization with error handling
if data is not None:
    st.markdown("## 📊 UPLOADED DATASET ANALYSIS")
    
    # Check if data is not empty
    if data.empty:
        st.warning("⚠️ The uploaded file is empty. Please upload a valid file with data.")
    else:
        st.dataframe(data.head(10), use_container_width=True)
        
        st.markdown("### **📈 DATA VISUALIZATION**")
        numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
        
        if numeric_cols:
            selected_col = st.selectbox(
                "**Select column to optimize (as f(x))**", 
                numeric_cols,
                help="Choose which column represents the function values"
            )
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["📊 Chart", "📝 Statistics", "⚙️ Optimization"])
            
            with tab1:
                st.line_chart(data[selected_col])
                
            with tab2:
                st.write(f"**Statistics for {selected_col}:**")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Mean", f"{data[selected_col].mean():.4f}")
                with col2:
                    st.metric("Std Dev", f"{data[selected_col].std():.4f}")
                with col3:
                    st.metric("Min", f"{data[selected_col].min():.4f}")
                with col4:
                    st.metric("Max", f"{data[selected_col].max():.4f}")
            
            with tab3:
                y = data[selected_col].dropna().values
                x = np.arange(len(y))
                
                st.markdown("### **🎯 RUNNING GRADIENT DESCENT ON UPLOADED DATA**")
                
                col1, col2 = st.columns(2)
                with col1:
                    x0 = st.number_input(
                        "**Initial Point (x₀)**", 
                        value=float(len(y)/2),
                        min_value=0.0,
                        max_value=float(len(y)),
                        step=1.0
                    )
                with col2:
                    alpha = st.number_input(
                        "**Learning Rate (α)**", 
                        value=0.01,
                        min_value=0.0001,
                        max_value=1.0,
                        step=0.001,
                        format="%.4f"
                    )
                
                # Fit polynomial and run optimization
                if len(y) >= 3:
                    try:
                        coeffs = np.polyfit(x, y, 2)
                        func_expr = f"{coeffs[0]:.6f}*x**2 + {coeffs[1]:.6f}*x + {coeffs[2]:.6f}"
                        f2, f2_prime, _, _ = parse_function(func_expr)
                        
                        if st.button("🚀 Run Optimization on Data", use_container_width=True):
                            with st.spinner("Optimizing..."):
                                x_opt, steps = gradient_descent(f2, f2_prime, x0, alpha, tolerance, max_iter)
                            
                            # Results
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("📌 Optimized x", f"{x_opt:.6f}")
                            with col2:
                                st.metric("📊 f(x) at optimum", f"{f2(x_opt):.6f}")
                            with col3:
                                st.metric("⚡ Iterations", len(steps))
                            
                            # Plot
                            plot_path(f2, [s[1] for s in steps] + [x_opt], 
                                     "Optimization on Uploaded Column", 
                                     color='#9C27B0', label='Gradient Descent Path')
                            
                            # Display steps
                            if show_logs:
                                st.markdown("### **📋 ITERATION LOGS**")
                                df_steps = pd.DataFrame(steps, 
                                                       columns=["Iteration", "x", "f(x)", "Gradient", "Change"])
                                st.dataframe(df_steps, use_container_width=True)
                    except Exception as e:
                        st.error(f"❌ Error in optimization: {str(e)}")
        else:
            st.warning("⚠️ No numeric columns found in the uploaded data. Please upload a file with numeric data.")
else:
    # Show message when no file is uploaded
    st.info("ℹ️ **No data file uploaded.** Continue with manual function optimization below.")

# Export results button
st.sidebar.markdown("---")
if st.sidebar.button("📁 EXPORT RESULTS TO CSV", use_container_width=True):
    if st.session_state.results:
        results = []
        for method_name, steps in st.session_state.results.items():
            for i, x in enumerate(steps):
                results.append({
                    "Method": method_name, 
                    "Step": i+1, 
                    "x": x, 
                    "f(x)": f(x),
                    "f'(x)": f_prime(x) if f_prime else None
                })
        df = pd.DataFrame(results)
        csv = df.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button(
            "⬇ DOWNLOAD CSV", 
            csv, 
            file_name="optimization_results.csv", 
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.sidebar.warning("No results to export. Run an optimization first.")

# Method execution based on selection
st.markdown("---")

if method == "Golden Section Search":
    st.markdown("## 🔸 GOLDEN SECTION SEARCH")
    st.info("""
    **Golden Section Search** is a bracket method that doesn't require derivatives. 
    It's excellent for unimodal functions where you know a minimum exists in an interval.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("**Lower Bound (a)**", value=-10.0, step=1.0)
    with col2:
        b = st.number_input("**Upper Bound (b)**", value=10.0, step=1.0)
    
    if a >= b:
        st.error("❌ **Error:** Lower bound must be less than upper bound.")
    else:
        if st.button("🚀 RUN GOLDEN SECTION SEARCH", use_container_width=True):
            with st.spinner("Searching for optimum..."):
                x_opt, steps = golden_section_search(f, a, b, tolerance, max_iter)
                st.session_state.results["Golden"] = [s[2] for s in steps] + [x_opt]
            
            # Display results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🎯 Optimum x", f"{x_opt:.8f}")
            with col2:
                st.metric("📊 f(x) at optimum", f"{f(x_opt):.8f}")
            with col3:
                st.metric("⚡ Iterations", len(steps))
            
            # Plot
            plot_path(f, [s[2] for s in steps] + [x_opt], 
                     "Golden Section Search Path", 
                     color="#FF9800", label='Golden Section')
            
            # Display steps
            if show_logs:
                st.markdown("### **📋 ITERATION DETAILS**")
                df_steps = pd.DataFrame(steps, 
                                       columns=["Iteration", "a", "b", "c", "d", "f(c)", "f(d)", "Interval Size"])
                st.dataframe(df_steps, use_container_width=True)

elif method == "Newton's Method":
    st.markdown("## 🔹 NEWTON'S METHOD")
    st.info("""
    **Newton's Method** uses first and second derivatives for fast convergence. 
    Requires the function to be twice differentiable. May converge to local minima.
    """)
    
    x0 = st.number_input("**Initial Guess (x₀)**", value=0.0, step=1.0)
    
    if st.button("🚀 RUN NEWTON'S METHOD", use_container_width=True):
        with st.spinner("Iterating..."):
            x_opt, steps = newtons_method(f, f_prime, f_double_prime, x0, tolerance, max_iter)
            st.session_state.results["Newton"] = [s[1] for s in steps] + [x_opt]
        
        # Display results
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Optimum x", f"{x_opt:.8f}")
        with col2:
            st.metric("📊 f(x) at optimum", f"{f(x_opt):.8f}")
        with col3:
            st.metric("⚡ Iterations", len(steps))
        
        # Plot
        plot_path(f, [s[1] for s in steps] + [x_opt], 
                 "Newton's Method Path", 
                 color="#4CAF50", label="Newton's Method")
        
        # Display steps
        if show_logs:
            st.markdown("### **📋 ITERATION DETAILS**")
            df_steps = pd.DataFrame(steps, 
                                   columns=["Iteration", "x", "f(x)", "f'(x)", "f''(x)", "Change"])
            st.dataframe(df_steps, use_container_width=True)

elif method == "Gradient Descent":
    st.markdown("## 🔹 GRADIENT DESCENT")
    st.info("""
    **Gradient Descent** uses only first derivatives. Adjust learning rate carefully - 
    too small converges slowly, too large may diverge. Good for high-dimensional problems.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        x0 = st.number_input("**Initial Point (x₀)**", value=0.0, step=1.0)
    with col2:
        alpha = st.number_input("**Learning Rate (α)**", value=0.1, 
                               min_value=0.0001, max_value=1.0, step=0.01, format="%.4f")
    
    if st.button("🚀 RUN GRADIENT DESCENT", use_container_width=True):
        with st.spinner("Descending gradient..."):
            x_opt, steps = gradient_descent(f, f_prime, x0, alpha, tolerance, max_iter)
            st.session_state.results["GD"] = [s[1] for s in steps] + [x_opt]
        
        # Display results
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Optimum x", f"{x_opt:.8f}")
        with col2:
            st.metric("📊 f(x) at optimum", f"{f(x_opt):.8f}")
        with col3:
            st.metric("⚡ Iterations", len(steps))
        
        # Plot
        plot_path(f, [s[1] for s in steps] + [x_opt], 
                 "Gradient Descent Path", 
                 color="#2196F3", label="Gradient Descent")
        
        # Display steps
        if show_logs:
            st.markdown("### **📋 ITERATION DETAILS**")
            df_steps = pd.DataFrame(steps, 
                                   columns=["Iteration", "x", "f(x)", "Gradient", "Change"])
            st.dataframe(df_steps, use_container_width=True)

elif method == "Compare All Methods":
    st.markdown("## 📊 COMPARE ALL OPTIMIZATION METHODS")
    st.info("Run and compare the performance of different optimization algorithms on your function.")
    
    # Parameters for comparison
    col1, col2, col3 = st.columns(3)
    with col1:
        compare_a = st.number_input("**Bound a (for Golden)**", value=-10.0)
    with col2:
        compare_b = st.number_input("**Bound b (for Golden)**", value=10.0)
    with col3:
        compare_x0 = st.number_input("**Initial x₀ (for Newton/GD)**", value=0.0)
    
    alpha_gd = st.slider("**Learning Rate for GD**", 0.001, 0.5, 0.1, 0.001)
    
    if st.button("🚀 RUN ALL METHODS & COMPARE", use_container_width=True):
        results = {}
        
        # Run all methods
        with st.spinner("Running Golden Section Search..."):
            x_opt_golden, steps_golden = golden_section_search(f, compare_a, compare_b, tolerance, max_iter)
            results["Golden"] = {"x_opt": x_opt_golden, "steps": steps_golden, "color": "#FF9800"}
        
        with st.spinner("Running Newton's Method..."):
            x_opt_newton, steps_newton = newtons_method(f, f_prime, f_double_prime, compare_x0, tolerance, max_iter)
            results["Newton"] = {"x_opt": x_opt_newton, "steps": steps_newton, "color": "#4CAF50"}
        
        with st.spinner("Running Gradient Descent..."):
            x_opt_gd, steps_gd = gradient_descent(f, f_prime, compare_x0, alpha_gd, tolerance, max_iter)
            results["GD"] = {"x_opt": x_opt_gd, "steps": steps_gd, "color": "#2196F3"}
        
        # Store in session state
        st.session_state.results["Golden"] = [s[2] for s in steps_golden] + [x_opt_golden]
        st.session_state.results["Newton"] = [s[1] for s in steps_newton] + [x_opt_newton]
        st.session_state.results["GD"] = [s[1] for s in steps_gd] + [x_opt_gd]
        
        # Display comparison table
        st.markdown("### **📊 COMPARISON RESULTS**")
        
        comparison_data = []
        for method_name, data in results.items():
            comparison_data.append({
                "Method": method_name,
                "Optimum x": f"{data['x_opt']:.8f}",
                "f(x)": f"{f(data['x_opt']):.8f}",
                "Iterations": len(data['steps']),
                "Color": data['color']
            })
        
        df_comparison = pd.DataFrame(comparison_data)
        
        # Display as styled table
        st.dataframe(df_comparison[["Method", "Optimum x", "f(x)", "Iterations"]], 
                    use_container_width=True)
        
        # Plot all paths on same figure
        st.markdown("### **📈 COMPARISON OF PATHS**")
        
        # FIX: Use proper figure creation
        fig, ax = plt.subplots(figsize=(14, 8))
        fig.set_facecolor((0.97, 0.97, 0.97, 0.9))
        ax.set_facecolor((0.98, 0.98, 0.98))
        
        # Plot function
        x_vals = np.linspace(min([compare_a, compare_b, compare_x0])-3, 
                            max([compare_a, compare_b, compare_x0])+3, 400)
        y_vals = f(x_vals)
        ax.plot(x_vals, y_vals, 'k--', linewidth=2, alpha=0.7, label='f(x)')
        
        # Plot each method's path
        for method_name, data in results.items():
            if method_name == "Golden":
                path = [s[2] for s in data['steps']] + [data['x_opt']]
            else:
                path = [s[1] for s in data['steps']] + [data['x_opt']]
            
            ax.plot(path, f(np.array(path)), marker='o', 
                    color=data['color'], markersize=8, linewidth=2.5, 
                    label=f"{method_name} ({len(data['steps'])} iterations)")
            
            # Mark final point
            ax.scatter([data['x_opt']], [f(data['x_opt'])], 
                       s=200, color=data['color'], zorder=5, 
                       edgecolors='white', linewidth=3)
        
        ax.set_title("Comparison of Optimization Methods", fontsize=20, fontweight='bold', color='#1E3A8A')
        ax.set_xlabel('x', fontsize=16, fontweight='bold')
        ax.set_ylabel('f(x)', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.2)
        ax.legend(fontsize=12, framealpha=0.95)
        
        st.pyplot(fig)
        plt.clf()

# REMOVED FOOTER - No footer text now