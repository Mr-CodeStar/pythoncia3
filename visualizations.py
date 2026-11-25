"""
visualizations.py - Modern Light SaaS visual styling for EduPulse Dashboard.
Recreates the clean, elegant light lavender/white dashboard aesthetic from the design reference.
Uses crisp white card backings, deep indigo titles, slate labels, and vibrant purple/magenta/cyan accents.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Theme Color Constants - Light SaaS Palette
COLOR_TEXT_MAIN = "#0F172A"       # Deep slate / dark navy for high contrast
COLOR_TEXT_MUTED = "#64748B"      # Cool slate gray for labels
COLOR_GRID = "#F1F5F9"            # Very subtle light gray gridlines

# Vibrant Accents
ACCENT_PURPLE = "#6366F1"        # Primary Indigo / Purple
ACCENT_PINK = "#EC4899"          # Magenta / Vibrant Pink
ACCENT_CYAN = "#0284C7"          # Electric Sky Blue
ACCENT_AMBER = "#F59E0B"         # Warm Amber / Orange
ACCENT_GREEN = "#10B981"         # Emerald Green
ACCENT_MUTED = "#94A3B8"         # Cool Slate

THEME_PALETTE = [ACCENT_PURPLE, ACCENT_PINK, ACCENT_CYAN, ACCENT_AMBER, "#8B5CF6", "#06B6D4", "#F43F5E"]

RESULT_COLORS = {
    "Distinction": ACCENT_CYAN,
    "Pass": ACCENT_PURPLE,
    "Fail": ACCENT_PINK,
    "Withdrawn": ACCENT_MUTED,
}


def _apply_light_theme(fig, height=350, show_legend=True, margin=None):
    """Applies common clean light theme with subtle gridlines and crisp typography."""
    if margin is None:
        margin = dict(l=30, r=30, t=40, b=30)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color=COLOR_TEXT_MAIN, size=12),
        margin=margin,
        height=height,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=COLOR_TEXT_MUTED),
            bgcolor="rgba(0,0,0,0)"
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor=ACCENT_PURPLE,
            font=dict(color=COLOR_TEXT_MAIN, size=12, family="Plus Jakarta Sans, Inter, sans-serif")
        )
    )
    fig.update_xaxes(
        gridcolor=COLOR_GRID,
        zerolinecolor=COLOR_GRID,
        tickfont=dict(color=COLOR_TEXT_MUTED, size=11),
        title_font=dict(color=COLOR_TEXT_MAIN, size=12)
    )
    fig.update_yaxes(
        gridcolor=COLOR_GRID,
        zerolinecolor=COLOR_GRID,
        tickfont=dict(color=COLOR_TEXT_MUTED, size=11),
        title_font=dict(color=COLOR_TEXT_MAIN, size=12)
    )
    return fig


def create_engagement_donut(df: pd.DataFrame, center_rate: float, center_label: str = "Pass Rate"):
    """
    Creates the clean circular donut chart for Student Engagement / Final Results
    with central percentage metric and high-contrast light aesthetics.
    """
    if df.empty:
        fig = go.Figure()
        return _apply_light_theme(fig)

    colors = [RESULT_COLORS.get(res, ACCENT_PURPLE) for res in df["final_result"]]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=df["final_result"],
                values=df["count"],
                hole=0.72,
                marker=dict(colors=colors, line=dict(color="#FFFFFF", width=3)),
                textinfo="percent",
                textposition="outside",
                textfont=dict(color=COLOR_TEXT_MAIN, size=11),
                hovertemplate="<b>%{label}</b><br>Students: %{value:,.0f}<br>Share: %{percent}<extra></extra>",
                direction="clockwise",
                sort=False
            )
        ]
    )

    # Center annotation
    fig.add_annotation(
        text=f"<b style='font-size:30px; color:{COLOR_TEXT_MAIN};'>{center_rate}%</b><br><span style='font-size:12px; color:{COLOR_TEXT_MUTED}; text-transform:uppercase; font-weight:600; letter-spacing:0.8px;'>{center_label}</span>",
        x=0.5, y=0.5,
        font=dict(size=14, color=COLOR_TEXT_MAIN),
        showarrow=False
    )

    fig = _apply_light_theme(fig, height=330, show_legend=True, margin=dict(l=20, r=20, t=20, b=20))
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.05,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color=COLOR_TEXT_MUTED)
        )
    )
    return fig


def create_activity_timeline_chart(df: pd.DataFrame, aggregation: str = "Daily"):
    """
    Creates the Student Activity area and line chart over the course timeline
    matching the smooth lavender/purple area chart in the light design reference.
    """
    fig = go.Figure()

    if df.empty:
        return _apply_light_theme(fig)

    # Smooth purple line with translucent purple area fill
    fig.add_trace(
        go.Scatter(
            x=df["timeline_label"],
            y=df["total_clicks"],
            name="Total Clicks",
            mode="lines+markers",
            line=dict(color=ACCENT_PURPLE, width=2.5, shape="spline"),
            marker=dict(size=5, color=ACCENT_PURPLE),
            fill="tozeroy",
            fillcolor="rgba(99, 102, 241, 0.12)",
            hovertemplate="<b>%{x}</b><br>Total Clicks: %{y:,.0f}<extra></extra>"
        )
    )

    # Trend moving average overlay
    if "rolling_avg" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["timeline_label"],
                y=df["rolling_avg"],
                name="7-Day Trend",
                mode="lines",
                line=dict(color=ACCENT_PINK, width=2, dash="dot"),
                hovertemplate="Trend Avg: %{y:,.0f}<extra></extra>"
            )
        )

    fig = _apply_light_theme(fig, height=330, show_legend=True)
    fig.update_layout(
        xaxis=dict(
            title="Study Timeline" if aggregation != "Daily" else "Presentation Day Index",
            nticks=18 if aggregation == "Daily" else 25,
            showgrid=False
        ),
        yaxis=dict(title="Digital Clicks", showgrid=True)
    )
    return fig


def create_department_engagement_bars(dept_df: pd.DataFrame, prog_df: pd.DataFrame):
    """
    Creates bottom comparison panel for 'Where Students Study the Most'
    comparing Department & Programme engagement.
    """
    fig = go.Figure()

    if dept_df.empty:
        return _apply_light_theme(fig)

    fig.add_trace(
        go.Bar(
            y=dept_df["department"],
            x=dept_df["avg_clicks_per_student"],
            orientation="h",
            name="Avg Clicks / Student",
            marker=dict(
                color=ACCENT_PURPLE,
                line=dict(color="rgba(99, 102, 241, 0.4)", width=1)
            ),
            text=dept_df["avg_clicks_per_student"].apply(lambda v: f"{v:,.1f} clicks"),
            textposition="auto",
            textfont=dict(color="#FFFFFF", size=11, family="Plus Jakarta Sans"),
            hovertemplate="<b>%{y}</b><br>Avg Clicks/Student: %{x:,.1f}<br>Total Students: " + 
                          dept_df["unique_students"].astype(str) + "<extra></extra>"
        )
    )

    fig = _apply_light_theme(fig, height=260, show_legend=False)
    fig.update_layout(
        xaxis=dict(title="Average Clicks per Enrolled Student", showgrid=True),
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=20, t=20, b=30)
    )
    return fig


def create_resource_infographic_chart(type_summary: pd.DataFrame):
    """
    Horizontal infographic progress bar layout for Resource Analytics in clean light SaaS styling.
    """
    if type_summary.empty:
        fig = go.Figure()
        return _apply_light_theme(fig)

    top_types = type_summary.head(8).sort_values("total_clicks", ascending=True)

    palette = [ACCENT_PURPLE, ACCENT_PINK, ACCENT_CYAN, ACCENT_AMBER, "#8B5CF6", "#06B6D4", "#F43F5E", "#10B981"]
    bar_colors = palette[:len(top_types)]

    fig = go.Figure(
        go.Bar(
            y=top_types["activity_type"].str.upper(),
            x=top_types["total_clicks"],
            orientation="h",
            marker=dict(
                color=bar_colors,
                line=dict(color="#FFFFFF", width=1.5)
            ),
            text=top_types.apply(lambda r: f"{r['share_pct']}% ({r['total_clicks']:,.0f} clicks)", axis=1),
            textposition="inside",
            textfont=dict(color="#FFFFFF", size=11, family="Plus Jakarta Sans"),
            hovertemplate="<b>%{y}</b><br>Total Clicks: %{x:,.0f}<extra></extra>"
        )
    )

    fig = _apply_light_theme(fig, height=350, show_legend=False)
    fig.update_layout(
        xaxis=dict(title="Total Clicks", showgrid=True),
        yaxis=dict(title=None),
        margin=dict(l=20, r=30, t=20, b=30)
    )
    return fig


def create_resource_timeline_chart(timeline_df: pd.DataFrame):
    """Resource usage over presentation time by activity type in clean light theme."""
    if timeline_df.empty:
        fig = go.Figure()
        return _apply_light_theme(fig)

    fig = px.line(
        timeline_df,
        x="date",
        y="sum_click",
        color="activity_type",
        color_discrete_sequence=[ACCENT_PURPLE, ACCENT_PINK, ACCENT_CYAN, ACCENT_AMBER, ACCENT_GREEN],
        labels={"date": "Study Day", "sum_click": "Total Clicks", "activity_type": "Resource Type"}
    )
    fig = _apply_light_theme(fig, height=340, show_legend=True)
    fig.update_xaxes(title="Presentation Day Index")
    fig.update_yaxes(title="Daily Interaction Clicks")
    return fig


def create_score_distribution_chart(valid_scores: pd.Series, score_bands: pd.DataFrame):
    """
    Creates score distribution histogram and band breakdown for Assessment Analytics.
    """
    fig = go.Figure()

    if valid_scores.empty:
        return _apply_light_theme(fig)

    fig.add_trace(
        go.Histogram(
            x=valid_scores,
            nbinsx=25,
            marker=dict(
                color=ACCENT_PURPLE,
                line=dict(color="#FFFFFF", width=1)
            ),
            opacity=0.85,
            name="Score Frequency",
            hovertemplate="Score Range: %{x}<br>Submissions: %{y:,.0f}<extra></extra>"
        )
    )

    # Vertical threshold line at pass mark (40) and distinction mark (70)
    fig.add_vline(x=40, line_width=2, line_dash="dash", line_color=ACCENT_PINK, annotation_text="Pass (40)", annotation_font_color=ACCENT_PINK)
    fig.add_vline(x=70, line_width=2, line_dash="dash", line_color=ACCENT_CYAN, annotation_text="Distinction (70)", annotation_font_color=ACCENT_CYAN)

    fig = _apply_light_theme(fig, height=320, show_legend=False)
    fig.update_layout(
        xaxis=dict(title="Assessment Score (0 - 100)", range=[0, 105]),
        yaxis=dict(title="Submission Count")
    )
    return fig


def create_assessment_type_comparison(type_stats: pd.DataFrame):
    """Grouped bar chart comparing TMA, CMA, Exam average scores and submission counts."""
    if type_stats.empty:
        fig = go.Figure()
        return _apply_light_theme(fig)

    fig = go.Figure(
        data=[
            go.Bar(
                name="Average Score",
                x=type_stats["assessment_type"],
                y=type_stats["avg_score"],
                marker=dict(color=ACCENT_PURPLE),
                text=type_stats["avg_score"].apply(lambda s: f"{s:.1f}"),
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>Avg Score: %{y:.1f}<extra></extra>"
            ),
            go.Bar(
                name="Pass Rate (%)",
                x=type_stats["assessment_type"],
                y=type_stats["pass_rate"],
                marker=dict(color=ACCENT_PINK),
                text=type_stats["pass_rate"].apply(lambda p: f"{p:.1f}%"),
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>Pass Rate: %{y:.1f}%<extra></extra>"
            )
        ]
    )

    fig = _apply_light_theme(fig, height=300, show_legend=True)
    fig.update_layout(barmode="group", yaxis=dict(title="Percentage / Score", range=[0, 110]))
    return fig


def create_course_engagement_scatter(course_summary: pd.DataFrame):
    """Bubble scatter comparing Course Clicks vs Enrolled Students vs Pass Rate."""
    if course_summary.empty:
        fig = go.Figure()
        return _apply_light_theme(fig)

    fig = px.scatter(
        course_summary,
        x="enrolled_students",
        y="total_clicks",
        size="avg_clicks_per_student",
        color="pass_rate",
        hover_name="course_id",
        color_continuous_scale=[[0, ACCENT_PINK], [0.5, ACCENT_PURPLE], [1, ACCENT_CYAN]],
        labels={
            "enrolled_students": "Enrolled Students",
            "total_clicks": "Total Learning Clicks",
            "pass_rate": "Pass Rate (%)",
            "avg_clicks_per_student": "Avg Clicks/Student"
        }
    )

    fig = _apply_light_theme(fig, height=350, show_legend=False)
    fig.update_coloraxes(colorbar=dict(title="Pass Rate %", tickfont=dict(color=COLOR_TEXT_MUTED)))
    return fig


def create_generic_donut(df: pd.DataFrame, label_col: str, value_col: str, title: str = "", palette=None):
    """Creates a generic clean donut chart for demographic distributions in light theme."""
    if df.empty:
        fig = go.Figure()
        return _apply_light_theme(fig)

    if palette is None:
        palette = THEME_PALETTE

    fig = go.Figure(
        data=[
            go.Pie(
                labels=df[label_col],
                values=df[value_col],
                hole=0.6,
                marker=dict(colors=palette, line=dict(color="#FFFFFF", width=2.5)),
                textinfo="percent+label",
                textposition="outside",
                textfont=dict(color=COLOR_TEXT_MAIN, size=11),
                hovertemplate="<b>%{label}</b><br>Count: %{value:,.0f}<br>Share: %{percent}<extra></extra>",
                sort=False
            )
        ]
    )
    fig = _apply_light_theme(fig, height=290, show_legend=False, margin=dict(l=15, r=15, t=25, b=15))
    return fig


def create_generic_bar(df: pd.DataFrame, x_col: str, y_col: str, color=ACCENT_PURPLE, horizontal=False):
    """Creates a sleek single-series bar chart in light theme."""
    if df.empty:
        fig = go.Figure()
        return _apply_light_theme(fig)

    if horizontal:
        fig = go.Figure(
            go.Bar(
                y=df[y_col],
                x=df[x_col],
                orientation="h",
                marker=dict(color=color, line=dict(color="#FFFFFF", width=1)),
                text=df[x_col].apply(lambda v: f"{v:,.0f}" if isinstance(v, (int, float)) else str(v)),
                textposition="auto",
                textfont=dict(color="#FFFFFF", size=11, family="Plus Jakarta Sans"),
                hovertemplate="<b>%{y}</b>: %{x:,.0f}<extra></extra>"
            )
        )
    else:
        fig = go.Figure(
            go.Bar(
                x=df[x_col],
                y=df[y_col],
                marker=dict(color=color, line=dict(color="#FFFFFF", width=1)),
                text=df[y_col].apply(lambda v: f"{v:,.0f}" if isinstance(v, (int, float)) else str(v)),
                textposition="auto",
                textfont=dict(color="#FFFFFF", size=11, family="Plus Jakarta Sans"),
                hovertemplate="<b>%{x}</b>: %{y:,.0f}<extra></extra>"
            )
        )

    fig = _apply_light_theme(fig, height=280, show_legend=False)
    return fig
