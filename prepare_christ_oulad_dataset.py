
import pandas as pd
import numpy as np
from pathlib import Path

# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

INPUT_DIR = Path("Dataset")  # Folder containing original OULAD CSV files
OUTPUT_DIR = Path("christ_dataset")

N_STUDENTS = 40000
RANDOM_STATE = 42
CHUNK_SIZE = 200000

OUTPUT_DIR.mkdir(exist_ok=True)

# Columns used to identify a course presentation
COURSE_KEYS = ["code_module", "code_presentation"]


# --------------------------------------------------
# 2. Read the six smaller CSV files
# --------------------------------------------------

student_info = pd.read_csv(INPUT_DIR / "studentInfo.csv")
student_registration = pd.read_csv(INPUT_DIR / "studentRegistration.csv")
student_assessment = pd.read_csv(INPUT_DIR / "studentAssessment.csv")

assessments = pd.read_csv(INPUT_DIR / "assessments.csv")
vle = pd.read_csv(INPUT_DIR / "vle.csv")
courses = pd.read_csv(INPUT_DIR / "courses.csv")


# --------------------------------------------------
# 3. Select the required number of unique students
# --------------------------------------------------

unique_students = student_info["id_student"].drop_duplicates()

actual_count = min(N_STUDENTS, len(unique_students))

if actual_count < N_STUDENTS:
    print(
        f"Warning: Only {actual_count} unique students are available "
        f"in the dataset. Selecting all available students."
    )

selected_ids = unique_students.sample(
    n=actual_count,
    random_state=RANDOM_STATE
)

# Keep all course records belonging to selected students
student_info = student_info[
    student_info["id_student"].isin(selected_ids)
].copy()

selected_pairs = student_info[COURSE_KEYS].drop_duplicates()

# Use course and presentation combinations to preserve relationships
selected_pair_index = pd.MultiIndex.from_frame(selected_pairs)


# --------------------------------------------------
# 4. Create simulated CHRIST student information
# --------------------------------------------------

rng = np.random.default_rng(RANDOM_STATE)

# Illustrative values: edit these to match your chosen
# CHRIST campus and programme list.
programme_data = {
    "MCA": ("Computer Science", "School of Engineering and Technology"),
    "BCA": ("Computer Science", "School of Engineering and Technology"),
    "BCom": ("Commerce", "School of Commerce, Finance and Accountancy"),
    "MBA": ("Management", "School of Business and Management")
}

campuses = [
    "Bangalore Central",
    "Bangalore Bannerghatta",
    "Bangalore Kengeri"
]

profile = pd.DataFrame({
    "id_student": selected_ids.to_numpy()
})

profile["christ_student_id"] = [
    f"CU2026{i:05d}" for i in range(1, len(profile) + 1)
]

profile["campus"] = rng.choice(campuses, size=len(profile))

programmes = rng.choice(
    list(programme_data.keys()),
    size=len(profile)
)

profile["programme"] = programmes
profile["department"] = [
    programme_data[p][0] for p in programmes
]
profile["school"] = [
    programme_data[p][1] for p in programmes
]

profile["semester"] = rng.integers(1, 7, size=len(profile))
profile["academic_year"] = "2026-2027"

# Add the simulated profile to student information
student_info = student_info.merge(profile, on="id_student", how="left")


# --------------------------------------------------
# 5. Filter student registration and assessment data
# --------------------------------------------------

student_registration = student_registration[
    student_registration["id_student"].isin(selected_ids)
].copy()

student_registration = student_registration.merge(
    profile, on="id_student", how="left"
)

# Keep assessments belonging to the selected course presentations
assessments = assessments.merge(
    selected_pairs, on=COURSE_KEYS, how="inner"
)

selected_assessment_ids = assessments["id_assessment"].unique()

student_assessment = student_assessment[
    (student_assessment["id_student"].isin(selected_ids)) &
    (student_assessment["id_assessment"].isin(selected_assessment_ids))
].copy()

student_assessment = student_assessment.merge(
    profile, on="id_student", how="left"
)


# --------------------------------------------------
# 6. Filter VLE activity data in chunks
# --------------------------------------------------

# studentVle is the largest OULAD file, so process it
# in smaller chunks to reduce memory usage.

student_vle_path = INPUT_DIR / "studentVle.csv"
output_vle_path = OUTPUT_DIR / "studentVle.csv"

if output_vle_path.exists():
    output_vle_path.unlink()

used_site_ids = set()
first_chunk = True
total_activity_rows = 0

for chunk in pd.read_csv(student_vle_path, chunksize=CHUNK_SIZE):

    # Keep activities from selected students and course presentations
    pair_index = pd.MultiIndex.from_frame(chunk[COURSE_KEYS])

    mask = (
        chunk["id_student"].isin(selected_ids) &
        pair_index.isin(selected_pair_index)
    )

    filtered_chunk = chunk.loc[mask].copy()

    if not filtered_chunk.empty:
        used_site_ids.update(filtered_chunk["id_site"].unique())

        filtered_chunk = filtered_chunk.merge(
            profile, on="id_student", how="left"
        )

        filtered_chunk.to_csv(
            output_vle_path,
            index=False,
            mode="w" if first_chunk else "a",
            header=first_chunk
        )

        total_activity_rows += len(filtered_chunk)
        first_chunk = False

# Create an empty CSV with headers if no activity rows were found
if first_chunk:
    empty_vle = pd.read_csv(student_vle_path, nrows=0)
    for column in profile.columns:
        if column != "id_student":
            empty_vle[column] = pd.Series(dtype="object")
    empty_vle.to_csv(output_vle_path, index=False)


# --------------------------------------------------
# 7. Filter remaining reference tables
# --------------------------------------------------

# Keep only resources connected to the selected activity records
vle_pair_index = pd.MultiIndex.from_frame(vle[COURSE_KEYS])

vle = vle[
    vle["id_site"].isin(used_site_ids) &
    vle_pair_index.isin(selected_pair_index)
].copy()

courses = courses.merge(
    selected_pairs, on=COURSE_KEYS, how="inner"
)


# --------------------------------------------------
# 8. Save the filtered dataset
# --------------------------------------------------

student_info.to_csv(OUTPUT_DIR / "studentInfo.csv", index=False)
student_registration.to_csv(
    OUTPUT_DIR / "studentRegistration.csv", index=False
)
student_assessment.to_csv(
    OUTPUT_DIR / "studentAssessment.csv", index=False
)

assessments.to_csv(OUTPUT_DIR / "assessments.csv", index=False)
vle.to_csv(OUTPUT_DIR / "vle.csv", index=False)
courses.to_csv(OUTPUT_DIR / "courses.csv", index=False)

# Save the student-to-CHRIST profile mapping separately
profile.to_csv(
    OUTPUT_DIR / "christ_student_profile.csv", index=False
)


# --------------------------------------------------
# 9. Display dataset summary
# --------------------------------------------------

print("\nDataset preparation completed!")
print("-----------------------------------")
print("Selected unique students:", actual_count)
print("Student information rows:", len(student_info))
print("Registration rows:", len(student_registration))
print("VLE activity rows:", total_activity_rows)
print("Assessment rows:", len(student_assessment))
print("Output folder:", OUTPUT_DIR.resolve())

print("\nNote: CHRIST-specific fields are simulated.")
print("Original OULAD files have not been modified.")
