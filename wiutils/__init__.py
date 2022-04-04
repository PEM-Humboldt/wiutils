from wiutils.extraction import get_scientific_name
from wiutils.filtering import (
    remove_domestic,
    remove_duplicates,
    remove_inconsistent_dates,
    remove_unidentified,
)
from wiutils.plotting import (
    plot_activity_hours,
    plot_detection_history,
    plot_date_ranges,
)
from wiutils.preprocessing import (
    change_image_timestamp,
    convert_video_to_images,
    reduce_image_size,
)
from wiutils.reading import read_project
from wiutils.transformation import (
    compute_deployment_count_summary,
    compute_detection_by_deployment,
    compute_detection_history,
    compute_general_count,
    compute_hill_numbers,
    create_dwc_events,
    create_dwc_records,
)
from wiutils.verification import compute_date_ranges
