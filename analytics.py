"""
analytics.py - Analytical computations and aggregations for EduPulse Dashboard.
Strictly adheres to real data from the OULAD & CHRIST-enriched dataset.
Handles missing values, banked assessments, and multi-dimensional filtering.
"""

import pandas as pd
import numpy as np


def get_overview_kpis(filtered_data: dict) -> dict:
    """
    Computes primary high-level KPI cards for the Overview page.
    """
    si = filtered_data["student_info"]
    daily = filtered_data["daily_activity"]
    courses = filtered_data["courses"]
    vle = filtered_data["vle"]
    sa = filtered_data["student_assessment"]

    # 1. Total unique students
    total_students = int(si["id_student"].nunique()) if not si.empty else 0

    # 2. Total learning interactions (total sum_click)
    total_interactions = int(daily["total_clicks"].sum()) if not daily.empty else 0

    # 3. Total distinct courses/presentations
    if not si.empty:
        total_courses = int(si[["code_module", "code_presentation"]].drop_duplicates().shape[0])
    else:
        total_courses = int(courses.shape[0])

    # 4. Total learning resources available
    total_resources = int(vle["id_site"].nunique())

    # Additional contextual metrics
    if not si.empty:
        passed = si["final_result"].isin(["Pass", "Distinction"]).sum()
        pass_rate = round((passed / len(si)) * 100, 1)
        distinctions = (si["final_result"] == "Distinction").sum()
        distinction_rate = round((distinctions / len(si)) * 100, 1)
        withdrawn = (si["final_result"] == "Withdrawn").sum()
        retention_rate = round(((len(si) - withdrawn) / len(si)) * 100, 1)
    else:
        pass_rate, distinction_rate, retention_rate = 0.0, 0.0, 0.0

    valid_scores = sa["score"].dropna()
    avg_score = round(float(valid_scores.mean()), 1) if not valid_scores.empty else 0.0

    return {
        "total_students": total_students,
        "total_interactions": total_interactions,
        "total_courses": total_courses,
        "total_resources": total_resources,
        "pass_rate": pass_rate,
        "distinction_rate": distinction_rate,
        "retention_rate": retention_rate,
        "avg_score": avg_score,
    }


def get_student_engagement_distribution(filtered_data: dict) -> dict:
    """
    Aggregates final_result distribution for the donut chart.
    """
    si = filtered_data["student_info"]
    if si.empty:
        return {
            "df": pd.DataFrame(columns=["final_result", "count", "percentage"]),
            "success_rate": 0.0,
            "retention_rate": 0.0,
            "total_enrollments": 0,
        }

    total = len(si)
    counts = si["final_result"].value_counts().reset_index()
    counts.columns = ["final_result", "count"]
    counts["percentage"] = (counts["count"] / total * 100).round(1)

    # Sort in standard academic order
    order_map = {"Distinction": 0, "Pass": 1, "Fail": 2, "Withdrawn": 3}
    counts["order"] = counts["final_result"].map(order_map).fillna(99)
    counts = counts.sort_values("order").drop(columns=["order"])

    pass_and_dist = si["final_result"].isin(["Pass", "Distinction"]).sum()
    success_rate = round((pass_and_dist / total) * 100, 1)
    
    withdrawn = (si["final_result"] == "Withdrawn").sum()
    retention_rate = round(((total - withdrawn) / total) * 100, 1)

    return {
        "df": counts,
        "success_rate": success_rate,
        "retention_rate": retention_rate,
        "total_enrollments": total,
    }


def get_student_activity_timeline(filtered_data: dict, aggregation: str = "Daily") -> pd.DataFrame:
    """
    Aggregates student learning clicks over the course presentation timeline.
    aggregation: 'Daily', 'Weekly', or 'Monthly'
    """
    daily = filtered_data["daily_activity"]
    if daily.empty:
        return pd.DataFrame(columns=["timeline_label", "total_clicks", "interactions"])

    if aggregation == "Daily":
        timeline = daily.groupby("date", as_index=False).agg(
            total_clicks=("total_clicks", "sum"),
            interactions=("interactions", "sum")
        ).sort_values("date")
        timeline["timeline_label"] = "Day " + timeline["date"].astype(str)
        # Add 7-day rolling average for smoother visualization
        timeline["rolling_avg"] = timeline["total_clicks"].rolling(window=7, min_periods=1, center=True).mean().round(1)

    elif aggregation == "Weekly":
        # Group into 7-day study week buckets
        # Note: negative days are pre-course registration period
        df = daily.copy()
        df["study_week"] = np.floor(df["date"] / 7).astype(int)
        timeline = df.groupby("study_week", as_index=False).agg(
            total_clicks=("total_clicks", "sum"),
            interactions=("interactions", "sum")
        ).sort_values("study_week")
        timeline["timeline_label"] = timeline["study_week"].apply(
            lambda w: f"Week {w}" if w >= 0 else f"Pre-Course (Wk {w})"
        )
        timeline["rolling_avg"] = timeline["total_clicks"].rolling(window=3, min_periods=1, center=True).mean().round(1)

    else:  # Monthly (30-day buckets)
        df = daily.copy()
        df["study_month"] = np.floor(df["date"] / 30).astype(int)
        timeline = df.groupby("study_month", as_index=False).agg(
            total_clicks=("total_clicks", "sum"),
            interactions=("interactions", "sum")
        ).sort_values("study_month")
        timeline["timeline_label"] = timeline["study_month"].apply(
            lambda m: f"Month {m+1}" if m >= 0 else f"Pre-Start (M{m})"
        )
        timeline["rolling_avg"] = timeline["total_clicks"]

    return timeline


def get_engagement_by_department_and_programme(filtered_data: dict) -> dict:
    """
    Computes comparative digital engagement across departments and programmes.
    Calculates total clicks and average clicks per student.
    """
    si = filtered_data["student_info"]
    daily = filtered_data["daily_activity"]

    if si.empty or daily.empty:
        return {
            "department": pd.DataFrame(),
            "programme": pd.DataFrame()
        }

    # Department level
    dept_clicks = daily.groupby("department", as_index=False)["total_clicks"].sum()
    dept_students = si.groupby("department")["id_student"].nunique().reset_index(name="unique_students")
    dept_summary = pd.merge(dept_clicks, dept_students, on="department", how="outer").fillna(0)
    dept_summary["avg_clicks_per_student"] = (
        dept_summary["total_clicks"] / dept_summary["unique_students"].replace(0, np.nan)
    ).fillna(0).round(1)
    dept_summary = dept_summary.sort_values("avg_clicks_per_student", ascending=False)

    # Programme level
    prog_clicks = daily.groupby("programme", as_index=False)["total_clicks"].sum()
    prog_students = si.groupby("programme")["id_student"].nunique().reset_index(name="unique_students")
    prog_summary = pd.merge(prog_clicks, prog_students, on="programme", how="outer").fillna(0)
    prog_summary["avg_clicks_per_student"] = (
        prog_summary["total_clicks"] / prog_summary["unique_students"].replace(0, np.nan)
    ).fillna(0).round(1)
    prog_summary = prog_summary.sort_values("avg_clicks_per_student", ascending=False)

    return {
        "department": dept_summary,
        "programme": prog_summary
    }


def get_student_demographics(filtered_data: dict) -> dict:
    """
    Computes breakdowns for the Student Analytics page.
    """
    si = filtered_data["student_info"]
    if si.empty:
        return {}

    # Total unique students in filtered set
    unique_students_count = si["id_student"].nunique()

    # Campus breakdown
    campus_dist = si.groupby("campus")["id_student"].nunique().reset_index(name="students")
    campus_dist["percentage"] = (campus_dist["students"] / unique_students_count * 100).round(1)
    campus_dist = campus_dist.sort_values("students", ascending=False)

    # Department breakdown
    dept_dist = si.groupby("department")["id_student"].nunique().reset_index(name="students")
    dept_dist["percentage"] = (dept_dist["students"] / unique_students_count * 100).round(1)
    dept_dist = dept_dist.sort_values("students", ascending=False)

    # Programme breakdown
    prog_dist = si.groupby("programme")["id_student"].nunique().reset_index(name="students")
    prog_dist["percentage"] = (prog_dist["students"] / unique_students_count * 100).round(1)
    prog_dist = prog_dist.sort_values("students", ascending=False)

    # Semester breakdown
    sem_dist = si.groupby("semester")["id_student"].nunique().reset_index(name="students")
    sem_dist["semester_label"] = "Semester " + sem_dist["semester"].astype(str)
    sem_dist["percentage"] = (sem_dist["students"] / unique_students_count * 100).round(1)
    sem_dist = sem_dist.sort_values("semester")

    # Gender breakdown
    gender_dist = si.groupby("gender")["id_student"].nunique().reset_index(name="students")
    gender_map = {"M": "Male", "F": "Female"}
    gender_dist["gender_label"] = gender_dist["gender"].map(gender_map).fillna(gender_dist["gender"])
    gender_dist["percentage"] = (gender_dist["students"] / unique_students_count * 100).round(1)

    # Age band
    age_dist = si.groupby("age_band")["id_student"].nunique().reset_index(name="students")
    age_dist["percentage"] = (age_dist["students"] / unique_students_count * 100).round(1)

    # Highest education
    edu_dist = si.groupby("highest_education")["id_student"].nunique().reset_index(name="students")
    edu_dist["percentage"] = (edu_dist["students"] / unique_students_count * 100).round(1)
    edu_dist = edu_dist.sort_values("students", ascending=False)

    # Final result by department cross-tabulation
    result_by_dept = pd.crosstab(
        si["department"], 
        si["final_result"], 
        normalize="index"
    ) * 100
    result_by_dept = result_by_dept.round(1).reset_index()

    return {
        "unique_students": unique_students_count,
        "campus": campus_dist,
        "department": dept_dist,
        "programme": prog_dist,
        "semester": sem_dist,
        "gender": gender_dist,
        "age_band": age_dist,
        "education": edu_dist,
        "result_by_dept": result_by_dept,
    }


def get_resource_analytics(filtered_data: dict) -> dict:
    """
    Computes digital learning resource metrics from resource_types and resource_sites.
    """
    rt = filtered_data["resource_types"]
    rs = filtered_data["resource_sites"]
    rt_timeline = filtered_data["resource_timeline"]

    if rt.empty:
        return {
            "type_summary": pd.DataFrame(),
            "timeline": pd.DataFrame(),
            "top_sites": pd.DataFrame()
        }

    # Aggregate by activity_type
    type_summary = rt.groupby("activity_type", as_index=False).agg(
        total_clicks=("total_clicks", "sum"),
        interactions=("interactions", "sum")
    ).sort_values("total_clicks", ascending=False)

    total_clicks = type_summary["total_clicks"].sum()
    type_summary["share_pct"] = (type_summary["total_clicks"] / total_clicks * 100).round(1) if total_clicks > 0 else 0

    # Top resource types timeline (Top 5 activity types)
    top_5_types = type_summary.head(5)["activity_type"].tolist()
    timeline_top = rt_timeline[rt_timeline["activity_type"].isin(top_5_types)].copy()
    timeline_top = timeline_top.sort_values(["activity_type", "date"])

    # Top individual resource sites
    top_sites = rs.sort_values("total_clicks", ascending=False).head(15).copy()
    top_sites["resource_name"] = top_sites["activity_type"].str.upper() + " #" + top_sites["id_site"].astype(str)

    return {
        "type_summary": type_summary,
        "timeline": timeline_top,
        "top_sites": top_sites,
    }


def get_course_analytics(filtered_data: dict) -> dict:
    """
    Computes course-level participation, engagement, and completion metrics.
    """
    si = filtered_data["student_info"]
    courses = filtered_data["courses"]
    cvle = filtered_data["course_vle"]

    if si.empty:
        return {"course_summary": pd.DataFrame(), "module_summary": pd.DataFrame()}

    # Group student registrations and results by course_id
    course_students = si.groupby(["code_module", "code_presentation", "course_id"]).agg(
        enrolled_students=("id_student", "nunique"),
        pass_count=("final_result", lambda x: x.isin(["Pass", "Distinction"]).sum()),
        distinction_count=("final_result", lambda x: (x == "Distinction").sum()),
        withdrawn_count=("final_result", lambda x: (x == "Withdrawn").sum()),
        total_records=("id_student", "count")
    ).reset_index()

    course_students["pass_rate"] = (
        course_students["pass_count"] / course_students["total_records"] * 100
    ).round(1)

    # Merge module presentation length
    course_merged = course_students.merge(
        courses[["code_module", "code_presentation", "module_presentation_length"]],
        on=["code_module", "code_presentation"],
        how="left"
    )

    # Merge VLE engagement
    cvle_grouped = cvle.groupby(["code_module", "code_presentation"], as_index=False).agg(
        total_clicks=("total_clicks", "sum"),
        active_interactions=("active_interactions", "sum"),
        vle_active_students=("active_students", "max")
    )

    course_summary = course_merged.merge(
        cvle_grouped,
        on=["code_module", "code_presentation"],
        how="left"
    ).fillna(0)

    course_summary["avg_clicks_per_student"] = (
        course_summary["total_clicks"] / course_summary["enrolled_students"].replace(0, np.nan)
    ).fillna(0).round(1)

    course_summary = course_summary.sort_values("total_clicks", ascending=False)

    # Module level aggregation
    module_summary = course_summary.groupby("code_module", as_index=False).agg(
        presentations=("code_presentation", "count"),
        total_students=("enrolled_students", "sum"),
        total_clicks=("total_clicks", "sum"),
        avg_pass_rate=("pass_rate", "mean"),
        avg_presentation_length=("module_presentation_length", "mean")
    ).round(1).sort_values("total_clicks", ascending=False)

    return {
        "course_summary": course_summary,
        "module_summary": module_summary
    }


def get_assessment_analytics(filtered_data: dict) -> dict:
    """
    Computes assessment score distributions, participation rates,
    banked assessments, and timeliness of submission.
    """
    sa = filtered_data["student_assessment"]
    if sa.empty:
        return {}

    total_submissions = len(sa)
    valid_scores = sa["score"].dropna()
    missing_scores = int(sa["score"].isna().sum())
    banked_submissions = int((sa["is_banked"] == 1).sum())
    unique_students_assessed = int(sa["id_student"].nunique())

    # Overall score statistics
    avg_score = round(float(valid_scores.mean()), 1) if not valid_scores.empty else 0.0
    median_score = round(float(valid_scores.median()), 1) if not valid_scores.empty else 0.0
    min_score = round(float(valid_scores.min()), 1) if not valid_scores.empty else 0.0
    max_score = round(float(valid_scores.max()), 1) if not valid_scores.empty else 0.0
    std_score = round(float(valid_scores.std()), 1) if not valid_scores.empty else 0.0

    # Score bands
    # Distinction (70-100), Merit/Pass (55-69), Borderline Pass (40-54), Fail (0-39)
    bins = [-1, 39, 54, 69, 100]
    labels = ["Fail (<40)", "Borderline Pass (40-54)", "Merit / Good (55-69)", "Distinction (70-100)"]
    score_bands = pd.cut(valid_scores, bins=bins, labels=labels).value_counts().reindex(labels).reset_index()
    score_bands.columns = ["band", "count"]
    score_bands["percentage"] = (score_bands["count"] / len(valid_scores) * 100).round(1)

    # Assessment type comparison (TMA, CMA, Exam)
    type_stats = sa.groupby("assessment_type").agg(
        submissions=("id_student", "count"),
        avg_score=("score", "mean"),
        min_score=("score", "min"),
        max_score=("score", "max"),
        pass_rate=("score", lambda x: (x >= 40).sum() / x.dropna().count() * 100 if x.dropna().count() > 0 else 0)
    ).round(1).reset_index()

    # Performance by Programme
    prog_stats = sa.groupby("programme").agg(
        submissions=("id_student", "count"),
        avg_score=("score", "mean"),
        pass_rate=("score", lambda x: (x >= 40).sum() / x.dropna().count() * 100 if x.dropna().count() > 0 else 0)
    ).round(1).reset_index().sort_values("avg_score", ascending=False)

    # Performance by Department
    dept_stats = sa.groupby("department").agg(
        submissions=("id_student", "count"),
        avg_score=("score", "mean"),
        pass_rate=("score", lambda x: (x >= 40).sum() / x.dropna().count() * 100 if x.dropna().count() > 0 else 0)
    ).round(1).reset_index().sort_values("avg_score", ascending=False)

    # Submission timeliness (days_delay = date_submitted - assessment_date)
    # Filter where delay is not null
    delays = sa["days_delay"].dropna()
    timeliness = {
        "early": int((delays < 0).sum()),
        "on_time": int((delays == 0).sum()),
        "late_1_7_days": int(((delays > 0) & (delays <= 7)).sum()),
        "late_over_7_days": int((delays > 7).sum()),
        "total_tracked": int(len(delays))
    }

    return {
        "total_submissions": total_submissions,
        "unique_students": unique_students_assessed,
        "avg_score": avg_score,
        "median_score": median_score,
        "min_score": min_score,
        "max_score": max_score,
        "std_score": std_score,
        "missing_scores": missing_scores,
        "banked_submissions": banked_submissions,
        "score_bands": score_bands,
        "type_stats": type_stats,
        "prog_stats": prog_stats,
        "dept_stats": dept_stats,
        "timeliness": timeliness,
        "raw_valid_scores": valid_scores,
    }
