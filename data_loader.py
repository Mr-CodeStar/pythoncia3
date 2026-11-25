"""
data_loader.py - Data loading, caching, and preprocessing for EduPulse Dashboard.
Handles OULAD dataset enriched with simulated CHRIST University academic fields.
Implements robust chunked pre-aggregation for 10M+ studentVle records.
"""

import os
import time
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st

DATA_DIR = Path("christ_dataset")
CACHE_DIR = DATA_DIR / ".cache"

COURSE_KEYS = ["code_module", "code_presentation"]


def ensure_preaggregations(force: bool = False):
    """
    Pre-aggregates the 10.6M+ row studentVle.csv into compact parquet files
    if they do not already exist, ensuring near-instantaneous dashboard responsiveness.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    daily_cache = CACHE_DIR / "daily_activity.parquet"
    res_type_cache = CACHE_DIR / "resource_types.parquet"
    res_sites_cache = CACHE_DIR / "resource_sites.parquet"
    course_cache = CACHE_DIR / "course_vle.parquet"
    timeline_cache = CACHE_DIR / "resource_timeline.parquet"
    
    needed_files = [daily_cache, res_type_cache, res_sites_cache, course_cache, timeline_cache]
    if not force and all(f.exists() for f in needed_files):
        return True

    vle_csv = DATA_DIR / "vle.csv"
    student_vle_csv = DATA_DIR / "studentVle.csv"

    if not student_vle_csv.exists():
        raise FileNotFoundError(
            "Pre-aggregated cache files are missing and christ_dataset/studentVle.csv is not present. "
            "Please ensure the christ_dataset/.cache/ folder is committed to your GitHub repository so Streamlit Cloud can load the pre-aggregated metrics."
        )

    vle_ref = pd.read_csv(vle_csv)[["id_site", "activity_type"]].drop_duplicates()
    vle_dict = dict(zip(vle_ref["id_site"], vle_ref["activity_type"]))

    daily_list = []
    res_type_list = []
    res_sites_list = []
    course_list = []
    timeline_list = []

    cols = [
        "code_module", "code_presentation", "id_student", "id_site", 
        "date", "sum_click", "campus", "programme", "department", "semester"
    ]

    chunk_size = 1500000
    for chunk in pd.read_csv(student_vle_csv, usecols=cols, chunksize=chunk_size):
        # 1. Daily activity aggregation
        d_agg = chunk.groupby(
            ["campus", "department", "programme", "semester", "code_module", "code_presentation", "date"], 
            as_index=False
        )["sum_click"].agg(total_clicks="sum", interactions="count")
        daily_list.append(d_agg)

        # 2. Activity type mapping
        chunk["activity_type"] = chunk["id_site"].map(vle_dict).fillna("other")

        # 3. Resource type by group
        r_agg = chunk.groupby(
            ["campus", "department", "programme", "semester", "code_module", "activity_type"], 
            as_index=False
        )["sum_click"].agg(total_clicks="sum", interactions="count")
        res_type_list.append(r_agg)

        # 4. Top sites
        top_sites = chunk.groupby(
            ["id_site", "activity_type"], 
            as_index=False
        )["sum_click"].agg(total_clicks="sum", interactions="count")
        res_sites_list.append(top_sites)

        # 5. Course engagement
        c_agg = chunk.groupby(
            ["campus", "department", "programme", "semester", "code_module", "code_presentation"], 
            as_index=False
        ).agg(
            total_clicks=("sum_click", "sum"), 
            active_interactions=("sum_click", "count"), 
            active_students=("id_student", "nunique")
        )
        course_list.append(c_agg)

        # 6. Timeline by activity type
        t_agg = chunk.groupby(["activity_type", "date"], as_index=False)["sum_click"].sum()
        timeline_list.append(t_agg)

    # Save merged summaries
    daily_df = pd.concat(daily_list).groupby(
        ["campus", "department", "programme", "semester", "code_module", "code_presentation", "date"], 
        as_index=False
    ).sum()
    daily_df.to_parquet(daily_cache, index=False)

    res_types_df = pd.concat(res_type_list).groupby(
        ["campus", "department", "programme", "semester", "code_module", "activity_type"], 
        as_index=False
    ).sum()
    res_types_df.to_parquet(res_type_cache, index=False)

    res_sites_df = pd.concat(res_sites_list).groupby(
        ["id_site", "activity_type"], 
        as_index=False
    ).sum()
    res_sites_df.to_parquet(res_sites_cache, index=False)

    course_df = pd.concat(course_list).groupby(
        ["campus", "department", "programme", "semester", "code_module", "code_presentation"], 
        as_index=False
    ).agg({"total_clicks": "sum", "active_interactions": "sum", "active_students": "max"})
    course_df.to_parquet(course_cache, index=False)

    timeline_df = pd.concat(timeline_list).groupby(["activity_type", "date"], as_index=False).sum()
    timeline_df.to_parquet(timeline_cache, index=False)

    return True


@st.cache_data(show_spinner=False)
def load_all_data():
    """
    Loads all primary CSV tables and cached parquet aggregations.
    Returns a unified dictionary of DataFrames.
    """
    ensure_preaggregations(force=False)

    # 1. Core tables
    student_info = pd.read_csv(DATA_DIR / "studentInfo.csv")
    student_reg = pd.read_csv(DATA_DIR / "studentRegistration.csv")
    assessments = pd.read_csv(DATA_DIR / "assessments.csv")
    courses = pd.read_csv(DATA_DIR / "courses.csv")
    vle = pd.read_csv(DATA_DIR / "vle.csv")
    profile = pd.read_csv(DATA_DIR / "christ_student_profile.csv")
    
    # 2. Student assessments joined with assessments table
    student_ass = pd.read_csv(DATA_DIR / "studentAssessment.csv")
    # Merge assessments metadata (assessment_type, date, weight)
    # Note: avoid duplicate columns if both have code_module
    ass_meta = assessments[["id_assessment", "code_module", "code_presentation", "assessment_type", "date", "weight"]].copy()
    ass_meta = ass_meta.rename(columns={"date": "assessment_date"})
    
    merged_ass = student_ass.merge(ass_meta, on="id_assessment", how="left")
    # Calculate submission delay (days late: positive = late, negative = early)
    merged_ass["days_delay"] = merged_ass["date_submitted"] - merged_ass["assessment_date"]

    # 3. Load pre-aggregated VLE parquets
    daily_activity = pd.read_parquet(CACHE_DIR / "daily_activity.parquet")
    resource_types = pd.read_parquet(CACHE_DIR / "resource_types.parquet")
    resource_sites = pd.read_parquet(CACHE_DIR / "resource_sites.parquet")
    course_vle = pd.read_parquet(CACHE_DIR / "course_vle.parquet")
    resource_timeline = pd.read_parquet(CACHE_DIR / "resource_timeline.parquet")

    # Add course_name identifier to courses
    courses["course_id"] = courses["code_module"] + " (" + courses["code_presentation"] + ")"
    student_info["course_id"] = student_info["code_module"] + " (" + student_info["code_presentation"] + ")"
    daily_activity["course_id"] = daily_activity["code_module"] + " (" + daily_activity["code_presentation"] + ")"
    course_vle["course_id"] = course_vle["code_module"] + " (" + course_vle["code_presentation"] + ")"
    merged_ass["course_id"] = merged_ass["code_module"] + " (" + merged_ass["code_presentation"] + ")"

    return {
        "student_info": student_info,
        "student_reg": student_reg,
        "assessments": assessments,
        "courses": courses,
        "vle": vle,
        "profile": profile,
        "student_assessment": merged_ass,
        "daily_activity": daily_activity,
        "resource_types": resource_types,
        "resource_sites": resource_sites,
        "course_vle": course_vle,
        "resource_timeline": resource_timeline,
    }


def filter_data(data: dict, filters: dict) -> dict:
    """
    Applies the active sidebar filters to all relevant DataFrames synchronously.
    
    filters dict keys:
    - campus: 'All' or specific campus string
    - department: 'All' or specific department string
    - programme: 'All' or specific programme string
    - semester: 'All' or specific int
    - course_module: 'All' or specific code_module string (e.g. 'AAA')
    - course_presentation: 'All' or specific code_presentation string
    - date_range: tuple of (min_date, max_date) for VLE activity
    """
    campus = filters.get("campus", "All")
    department = filters.get("department", "All")
    programme = filters.get("programme", "All")
    semester = filters.get("semester", "All")
    course_module = filters.get("course_module", "All")
    course_presentation = filters.get("course_presentation", "All")
    date_range = filters.get("date_range", None)

    filtered = {}

    def apply_common_filters(df):
        m = pd.Series(True, index=df.index)
        if campus != "All" and "campus" in df.columns:
            m &= (df["campus"] == campus)
        if department != "All" and "department" in df.columns:
            m &= (df["department"] == department)
        if programme != "All" and "programme" in df.columns:
            m &= (df["programme"] == programme)
        if semester != "All" and "semester" in df.columns:
            m &= (df["semester"] == semester)
        if course_module != "All" and "code_module" in df.columns:
            m &= (df["code_module"] == course_module)
        if course_presentation != "All" and "code_presentation" in df.columns:
            m &= (df["code_presentation"] == course_presentation)
        return df[m]

    filtered["student_info"] = apply_common_filters(data["student_info"])
    filtered["student_reg"] = apply_common_filters(data["student_reg"])
    filtered["student_assessment"] = apply_common_filters(data["student_assessment"])
    filtered["course_vle"] = apply_common_filters(data["course_vle"])
    filtered["resource_types"] = apply_common_filters(data["resource_types"])

    # Daily activity also filters by date_range
    daily = apply_common_filters(data["daily_activity"])
    if date_range is not None:
        min_d, max_d = date_range
        daily = daily[(daily["date"] >= min_d) & (daily["date"] <= max_d)]
    filtered["daily_activity"] = daily

    # Resource timeline
    res_timeline = data["resource_timeline"]
    if date_range is not None:
        min_d, max_d = date_range
        res_timeline = res_timeline[(res_timeline["date"] >= min_d) & (res_timeline["date"] <= max_d)]
    filtered["resource_timeline"] = res_timeline

    # Reference tables
    filtered["assessments"] = data["assessments"]
    filtered["courses"] = data["courses"]
    filtered["vle"] = data["vle"]
    filtered["resource_sites"] = data["resource_sites"]
    filtered["profile"] = data["profile"]

    return filtered
