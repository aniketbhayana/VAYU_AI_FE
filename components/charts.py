"""
Chart Components using Plotly
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict
import pandas as pd


def sensor_history_chart(readings: List[Dict]):
    """Display sensor history as line chart"""
    if not readings:
        st.info("No historical data available")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(readings)
    
    # Ensure timestamp is datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['pm25'],
        name='PM2.5 (µg/m³)',
        line=dict(color='#FF5252', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['co2'],
        name='CO2 (ppm)',
        line=dict(color='#00D9FF', width=2),
        yaxis='y2'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['co'],
        name='CO (ppm)',
        line=dict(color='#FFB300', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['voc'],
        name='VOC (ppb)',
        line=dict(color='#00C853', width=2),
        yaxis='y2'
    ))
    
    # Update layout
    fig.update_layout(
        title='Sensor Readings Over Time',
        xaxis_title='Time',
        yaxis_title='PM2.5 & CO (ppm)',
        yaxis2=dict(
            title='CO2 (ppm) & VOC (ppb)',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        template='plotly_dark',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def aqi_gauge(pm25_value: float):
    """Display AQI as gauge chart"""
    from utils.formatters import get_aqi_category
    
    category, color = get_aqi_category(pm25_value)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pm25_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"PM2.5 Air Quality<br><span style='font-size:0.8em;color:gray'>{category}</span>"},
        gauge={
            'axis': {'range': [None, 300], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 12], 'color': '#00C85330'},
                {'range': [12, 35.5], 'color': '#00D9FF30'},
                {'range': [35.5, 55.5], 'color': '#FFB30030'},
                {'range': [55.5, 150.5], 'color': '#FF525230'},
                {'range': [150.5, 300], 'color': '#FF000030'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 150
            }
        }
    ))
    
    fig.update_layout(
        template='plotly_dark',
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def fan_intensity_bar(intensity: int):
    """Display fan intensity as horizontal bar"""
    fig = go.Figure(go.Bar(
        x=[intensity],
        y=['Fan Speed'],
        orientation='h',
        marker=dict(
            color=intensity,
            colorscale=[[0, '#1E1E1E'], [0.5, '#FFB300'], [1, '#00C853']],
            cmin=0,
            cmax=100,
            line=dict(color='#00D9FF', width=2)
        ),
        text=[f'{intensity}%'],
        textposition='inside',
        textfont=dict(size=20, color='white')
    ))
    
    fig.update_layout(
        template='plotly_dark',
        height=100,
        xaxis=dict(range=[0, 100], showticklabels=False),
        yaxis=dict(showticklabels=False),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
