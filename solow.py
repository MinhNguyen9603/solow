import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Economics Decoded - Solow Growth Model",
    layout="wide"
)

st.title("📈 Solow Growth Model")
st.markdown(
"""
Explore how capital accumulation determines long-run economic growth.
"""
)


st.sidebar.header("Parameters")

alpha = st.sidebar.slider(
    "Capital Share α",
    0.10,
    0.80,
    0.35,
    0.01
)

s = st.sidebar.slider(
    "Saving Rate s",
    0.05,
    0.80,
    0.30,
    0.01
)

delta = st.sidebar.slider(
    "Depreciation δ",
    0.01,
    0.15,
    0.05,
    0.005
)

n = st.sidebar.slider(
    "Population Growth n",
    0.00,
    0.08,
    0.02,
    0.005
)

g = st.sidebar.slider(
    "Technology Growth g",
    0.00,
    0.08,
    0.02,
    0.005
)

k = np.linspace(0.01,30,400)

output = k**alpha

investment = s*output

break_even = (delta+n+g)*k

idx = np.argmin(np.abs(investment-break_even))

k_star = k[idx]

y_star = output[idx]

# --------------------
# Plot
# --------------------

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=k,
    y=output,
    name="Output y=f(k)",
    line=dict(width=4)
))

fig.add_trace(go.Scatter(
    x=k,
    y=investment,
    name="Investment sf(k)",
    line=dict(width=4)
))

fig.add_trace(go.Scatter(
    x=k,
    y=break_even,
    name="Break-even (δ+n+g)k",
    line=dict(width=4)
))

fig.add_trace(go.Scatter(
    x=[k_star],
    y=[investment[idx]],
    mode="markers",
    marker=dict(size=12),
    name="Steady State"
))

fig.add_vline(
    x=k_star,
    line_dash="dash"
)

fig.update_layout(

    title="Solow Growth Model",

    xaxis_title="Capital per Effective Worker (k)",

    yaxis_title="Output",

    height=650
)

st.plotly_chart(fig,use_container_width=True)

# --------------------
# Results
# --------------------

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Steady-State Capital",
    f"{k_star:.2f}"
)

col2.metric(
    "Output",
    f"{y_star:.2f}"
)

col3.metric(
    "Investment",
    f"{investment[idx]:.2f}"
)

col4.metric(
    "Break-even",
    f"{break_even[idx]:.2f}"
)

# --------------------
# Economic Explanation
# --------------------

st.header("Economic Interpretation")

if investment[idx] > break_even[idx]:
    st.success(
        """
Investment exceeds break-even.

Capital per worker is increasing.

GDP per worker will continue to grow.
"""
    )

elif investment[idx] < break_even[idx]:
    st.error(
        """
Investment is insufficient.

Capital per worker falls.

The economy becomes poorer.
"""
    )

else:
    st.info(
        """
The economy is at steady state.

Investment exactly replaces depreciation,
population growth and technology requirements.
"""
    )