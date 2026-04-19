"""
Streamlit Dashboard for LangSmith Metrics Visualization
Run with: streamlit run metrics_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta
import numpy as np


# Page configuration
st.set_page_config(
    page_title="LangSmith Metrics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


def load_metrics_data():
    """Load metrics from JSON file"""
    metrics_file = "langsmith/metrics_log.json"

    if os.path.exists(metrics_file):
        with open(metrics_file, 'r') as f:
            data = json.load(f)
            return data
    else:
        # Generate sample data if file doesn't exist
        return generate_sample_data()


def generate_sample_data():
    """Generate sample metrics data for demonstration"""
    import random
    from datetime import datetime, timedelta

    models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]
    chains = ["qa", "summary", "code_gen", "translation"]

    metrics = []
    now = datetime.now()

    for i in range(50):
        model = random.choice(models)
        chain = random.choice(chains)
        success = random.random() > 0.1  # 90% success rate

        base_tokens = {
            "gpt-3.5-turbo": (50, 150),
            "gpt-4": (100, 300),
            "gpt-4-turbo-preview": (80, 250)
        }

        prompt_tokens = random.randint(*base_tokens[model])
        completion_tokens = random.randint(50, 200)

        # Cost calculation (approximate)
        costs = {
            "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
            "gpt-4": {"prompt": 0.03, "completion": 0.06},
            "gpt-4-turbo-preview": {"prompt": 0.01, "completion": 0.03}
        }

        cost = (prompt_tokens * costs[model]["prompt"] +
                completion_tokens * costs[model]["completion"]) / 1000

        metrics.append({
            "chain_name": chain,
            "model": model,
            "timestamp": (now - timedelta(hours=random.randint(0, 24))).isoformat(),
            "success": success,
            "execution_time_seconds": round(random.uniform(0.5, 5.0), 3),
            "total_tokens": prompt_tokens + completion_tokens,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_cost_usd": round(cost, 6),
            "error": None if success else f"Sample error {i}"
        })

    # Calculate report
    successful_runs = [m for m in metrics if m["success"]]
    failed_runs = [m for m in metrics if not m["success"]]

    report = {
        "summary": {
            "total_runs": len(metrics),
            "successful_runs": len(successful_runs),
            "failed_runs": len(failed_runs),
            "success_rate": round(len(successful_runs) / len(metrics) * 100, 2)
        },
        "token_usage": {
            "total_tokens": sum(m["total_tokens"] for m in successful_runs),
            "total_prompt_tokens": sum(m["prompt_tokens"] for m in successful_runs),
            "total_completion_tokens": sum(m["completion_tokens"] for m in successful_runs),
            "avg_tokens_per_run": round(sum(m["total_tokens"] for m in successful_runs) / len(successful_runs), 2) if successful_runs else 0
        },
        "cost_analysis": {
            "total_cost_usd": round(sum(m["total_cost_usd"] for m in successful_runs), 4),
            "avg_cost_per_run": round(sum(m["total_cost_usd"] for m in successful_runs) / len(successful_runs), 6) if successful_runs else 0
        },
        "performance": {
            "avg_execution_time": round(sum(m["execution_time_seconds"] for m in metrics) / len(metrics), 3) if metrics else 0
        }
    }

    return {"metrics": metrics, "report": report}


def main():
    st.title("🚀 LangSmith Metrics Dashboard")
    st.markdown("### Real-time monitoring of LLM application metrics")

    # Load data
    data = load_metrics_data()
    metrics = data.get("metrics", [])
    report = data.get("report", {})

    if not metrics:
        st.warning("No metrics data available. Run the demo script first!")
        st.code("python langsmith/langsmith_demo.py", language="bash")
        return

    # Convert to DataFrame
    df = pd.DataFrame(metrics)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Sidebar filters
    st.sidebar.header("🔍 Filters")

    # Model filter
    selected_models = st.sidebar.multiselect(
        "Select Models",
        options=df['model'].unique(),
        default=df['model'].unique()
    )

    # Chain filter
    selected_chains = st.sidebar.multiselect(
        "Select Chains",
        options=df['chain_name'].unique(),
        default=df['chain_name'].unique()
    )

    # Success filter
    show_failures = st.sidebar.checkbox("Show Failed Runs", value=True)

    # Apply filters
    filtered_df = df[
        (df['model'].isin(selected_models)) &
        (df['chain_name'].isin(selected_chains))
    ]

    if not show_failures:
        filtered_df = filtered_df[filtered_df['success'] == True]

    # Main metrics
    st.header("📊 Key Metrics Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Runs",
            value=len(filtered_df),
            delta=f"{len(filtered_df[filtered_df['success'] == True])} successful"
        )

    with col2:
        total_tokens = filtered_df[filtered_df['success'] == True]['total_tokens'].sum()
        st.metric(
            label="Total Tokens Used",
            value=f"{total_tokens:,}",
            delta=f"Avg: {int(total_tokens/len(filtered_df)) if len(filtered_df) > 0 else 0}"
        )

    with col3:
        total_cost = filtered_df[filtered_df['success'] == True]['total_cost_usd'].sum()
        st.metric(
            label="Total Cost (USD)",
            value=f"${total_cost:.4f}",
            delta=f"Avg: ${total_cost/len(filtered_df):.6f}" if len(filtered_df) > 0 else "$0"
        )

    with col4:
        success_rate = (len(filtered_df[filtered_df['success'] == True]) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric(
            label="Success Rate",
            value=f"{success_rate:.1f}%",
            delta=f"{len(filtered_df[filtered_df['success'] == False])} failures"
        )

    # Detailed visualizations
    st.header("📈 Detailed Analytics")

    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Token Usage", "Cost Analysis", "Performance", "Error Analysis", "Model Comparison"])

    with tab1:
        st.subheader("Token Usage Over Time")

        # Token usage timeline
        fig_tokens = px.line(
            filtered_df[filtered_df['success'] == True].sort_values('timestamp'),
            x='timestamp',
            y='total_tokens',
            color='model',
            title='Token Usage Timeline',
            labels={'total_tokens': 'Total Tokens', 'timestamp': 'Time'}
        )
        st.plotly_chart(fig_tokens, use_container_width=True)

        # Token distribution
        col1, col2 = st.columns(2)

        with col1:
            fig_prompt = px.pie(
                values=[
                    filtered_df[filtered_df['success'] == True]['prompt_tokens'].sum(),
                    filtered_df[filtered_df['success'] == True]['completion_tokens'].sum()
                ],
                names=['Prompt Tokens', 'Completion Tokens'],
                title='Token Distribution'
            )
            st.plotly_chart(fig_prompt, use_container_width=True)

        with col2:
            # Tokens by chain
            tokens_by_chain = filtered_df[filtered_df['success'] == True].groupby('chain_name')['total_tokens'].sum().reset_index()
            fig_chain_tokens = px.bar(
                tokens_by_chain,
                x='chain_name',
                y='total_tokens',
                title='Total Tokens by Chain Type',
                labels={'total_tokens': 'Total Tokens', 'chain_name': 'Chain Type'}
            )
            st.plotly_chart(fig_chain_tokens, use_container_width=True)

    with tab2:
        st.subheader("Cost Analysis")

        # Cost over time
        fig_cost = px.area(
            filtered_df[filtered_df['success'] == True].sort_values('timestamp'),
            x='timestamp',
            y='total_cost_usd',
            color='model',
            title='Cumulative Cost Over Time',
            labels={'total_cost_usd': 'Cost (USD)', 'timestamp': 'Time'}
        )
        st.plotly_chart(fig_cost, use_container_width=True)

        # Cost breakdown
        col1, col2 = st.columns(2)

        with col1:
            # Cost by model
            cost_by_model = filtered_df[filtered_df['success'] == True].groupby('model')['total_cost_usd'].agg(['sum', 'mean']).reset_index()
            fig_model_cost = px.bar(
                cost_by_model,
                x='model',
                y='sum',
                title='Total Cost by Model',
                labels={'sum': 'Total Cost (USD)', 'model': 'Model'}
            )
            st.plotly_chart(fig_model_cost, use_container_width=True)

        with col2:
            # Cost efficiency (tokens per dollar)
            efficiency_df = filtered_df[filtered_df['success'] == True].copy()
            efficiency_df['tokens_per_dollar'] = efficiency_df['total_tokens'] / (efficiency_df['total_cost_usd'] + 0.0001)

            efficiency_by_model = efficiency_df.groupby('model')['tokens_per_dollar'].mean().reset_index()
            fig_efficiency = px.bar(
                efficiency_by_model,
                x='model',
                y='tokens_per_dollar',
                title='Token Efficiency by Model',
                labels={'tokens_per_dollar': 'Tokens per Dollar', 'model': 'Model'},
                color='tokens_per_dollar',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_efficiency, use_container_width=True)

    with tab3:
        st.subheader("Performance Metrics")

        # Execution time distribution
        fig_exec_time = px.histogram(
            filtered_df,
            x='execution_time_seconds',
            nbins=30,
            title='Execution Time Distribution',
            labels={'execution_time_seconds': 'Execution Time (seconds)'}
        )
        st.plotly_chart(fig_exec_time, use_container_width=True)

        # Performance by model and chain
        col1, col2 = st.columns(2)

        with col1:
            perf_by_model = filtered_df.groupby('model')['execution_time_seconds'].mean().reset_index()
            fig_model_perf = px.bar(
                perf_by_model,
                x='model',
                y='execution_time_seconds',
                title='Average Execution Time by Model',
                labels={'execution_time_seconds': 'Avg Execution Time (s)', 'model': 'Model'}
            )
            st.plotly_chart(fig_model_perf, use_container_width=True)

        with col2:
            perf_by_chain = filtered_df.groupby('chain_name')['execution_time_seconds'].mean().reset_index()
            fig_chain_perf = px.bar(
                perf_by_chain,
                x='chain_name',
                y='execution_time_seconds',
                title='Average Execution Time by Chain',
                labels={'execution_time_seconds': 'Avg Execution Time (s)', 'chain_name': 'Chain Type'}
            )
            st.plotly_chart(fig_chain_perf, use_container_width=True)

    with tab4:
        st.subheader("Error Analysis")

        failed_df = filtered_df[filtered_df['success'] == False]

        if len(failed_df) > 0:
            # Error rate over time
            error_timeline = filtered_df.copy()
            error_timeline['hour'] = error_timeline['timestamp'].dt.floor('H')
            error_rate = error_timeline.groupby('hour').agg({
                'success': lambda x: (1 - x.mean()) * 100
            }).reset_index()

            fig_error_rate = px.line(
                error_rate,
                x='hour',
                y='success',
                title='Error Rate Over Time',
                labels={'success': 'Error Rate (%)', 'hour': 'Time'}
            )
            st.plotly_chart(fig_error_rate, use_container_width=True)

            # Errors by model and chain
            col1, col2 = st.columns(2)

            with col1:
                error_by_model = failed_df.groupby('model').size().reset_index(name='error_count')
                fig_model_errors = px.pie(
                    error_by_model,
                    values='error_count',
                    names='model',
                    title='Errors by Model'
                )
                st.plotly_chart(fig_model_errors, use_container_width=True)

            with col2:
                error_by_chain = failed_df.groupby('chain_name').size().reset_index(name='error_count')
                fig_chain_errors = px.pie(
                    error_by_chain,
                    values='error_count',
                    names='chain_name',
                    title='Errors by Chain Type'
                )
                st.plotly_chart(fig_chain_errors, use_container_width=True)

            # Error details table
            st.subheader("Recent Errors")
            error_display = failed_df[['timestamp', 'model', 'chain_name', 'error']].tail(10)
            st.dataframe(error_display, use_container_width=True)
        else:
            st.success("No errors found in the filtered data!")

    with tab5:
        st.subheader("Model Comparison")

        # Comprehensive model comparison
        model_stats = filtered_df[filtered_df['success'] == True].groupby('model').agg({
            'total_tokens': 'mean',
            'total_cost_usd': 'mean',
            'execution_time_seconds': 'mean',
            'success': 'count'
        }).round(4).reset_index()

        model_stats.columns = ['Model', 'Avg Tokens', 'Avg Cost (USD)', 'Avg Time (s)', 'Total Runs']

        # Create radar chart for model comparison
        categories = ['Avg Tokens', 'Cost Efficiency', 'Speed', 'Reliability']

        fig_radar = go.Figure()

        for model in model_stats['Model']:
            model_data = model_stats[model_stats['Model'] == model].iloc[0]

            # Normalize values for radar chart (0-100 scale)
            tokens_score = min(100, (model_data['Avg Tokens'] / model_stats['Avg Tokens'].max()) * 100)
            cost_score = 100 - min(100, (model_data['Avg Cost (USD)'] / model_stats['Avg Cost (USD)'].max()) * 100)
            speed_score = 100 - min(100, (model_data['Avg Time (s)'] / model_stats['Avg Time (s)'].max()) * 100)
            reliability_score = min(100, (model_data['Total Runs'] / model_stats['Total Runs'].max()) * 100)

            fig_radar.add_trace(go.Scatterpolar(
                r=[tokens_score, cost_score, speed_score, reliability_score],
                theta=categories,
                fill='toself',
                name=model
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Model Performance Comparison (Higher is Better)"
        )

        st.plotly_chart(fig_radar, use_container_width=True)

        # Model comparison table
        st.subheader("Detailed Model Statistics")
        st.dataframe(model_stats, use_container_width=True)

    # Raw data view
    with st.expander("View Raw Data"):
        st.dataframe(filtered_df, use_container_width=True)

    # Export options
    st.header("📥 Export Data")
    col1, col2, col3 = st.columns(3)

    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"langsmith_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    with col2:
        json_data = filtered_df.to_json(orient='records', date_format='iso')
        st.download_button(
            label="Download as JSON",
            data=json_data,
            file_name=f"langsmith_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

    # Footer
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("""
    - Use filters in the sidebar to focus on specific models or chain types
    - Click on legend items in charts to show/hide specific data series
    - Hover over chart elements for detailed information
    - Export data for further analysis in other tools
    """)


if __name__ == "__main__":
    main()