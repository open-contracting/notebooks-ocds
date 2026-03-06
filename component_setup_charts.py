# ## Charts Setup
#
# *You must run the cells in this section each time you connect to a new runtime. For example, when you return to the notebook after an idle timeout, when the runtime crashes, or when you restart or factory reset the runtime.*

# ! pip install altair pyarrow==14.0.0 >> pip.log

# Import chart packages and define chart functions. The currently available chart functions are:
#
# * Release count
# * Objects per stage
# * Releases by month
# * Objects per year
# * Top buyers
# * Usability indicators

# +
# @title Chart functions { display-mode: "form" }
import altair as alt


class MissingColumnsError(Exception):
    def __init__(self, columns):
        super().__init__(f"The source data is missing one or more of these columns: {columns}")


chart_properties = {
    "width": 600,
    "height": 350,
    "padding": 50,
    "title": alt.TitleParams(text="", subtitle=[""], fontSize=18),
}
chart_axis = {
    "titleFontSize": 14,
    "labelFontSize": 14,
    "labelPadding": 5,
    "ticks": False,
    "domain": False,
}


def check_columns(columns, data):
    # check if input contains the right columns
    if not columns.issubset(data.columns):
        raise MissingColumnsError(columns)


def plot_release_count(release_counts):
    check_columns({"collection_id", "release_type", "release_count", "ocid_count"}, release_counts)
    return (
        alt.Chart(release_counts)
        .mark_bar()
        .encode(
            x=alt.X(
                "release_count",
                type="ordinal",
                axis=alt.Axis(title="release count", labelAngle=0),
            ),
            y=alt.Y(
                "ocid_count",
                type="quantitative",
                axis=alt.Axis(title="ocid count", format="~s", tickCount=5),
            ),
            color=alt.Color(
                "release_type",
                type="nominal",
                title="release type",
                scale=alt.Scale(range=["#D6E100", "#FB6045", "#23B2A7", "#6C75E1"]),
            ),
            tooltip=[
                alt.Tooltip("release_count", title="release count"),
                alt.Tooltip("ocid_count", title="ocid count", format="~s"),
                alt.Tooltip("release_type", title="release type"),
                alt.Tooltip("collection_id", title="collection id"),
            ],
        )
        .properties(**chart_properties)
        .configure_axis(**chart_axis)
        .configure_view(strokeWidth=0)
    )


def plot_objects_per_stage(objects_per_stage):
    check_columns({"stage", "object_count"}, objects_per_stage)
    stages = ["planning", "tender", "awards", "contracts", "implementation"]
    return (
        alt.Chart(objects_per_stage)
        .mark_bar(fill="#d6e100")
        .encode(
            x=alt.X(
                "stage",
                type="ordinal",
                scale=alt.Scale(domain=stages),
                sort=stages,
                axis=alt.Axis(title="stage", labelAngle=0),
            ),
            y=alt.Y(
                "object_count",
                type="quantitative",
                axis=alt.Axis(title="number of objects", format="~s", tickCount=len(stages)),
            ),
            tooltip=[
                alt.Tooltip("stage", title="stage"),
                alt.Tooltip("object_count", title="number of objects"),
            ],
        )
        .properties(**chart_properties)
        .configure_axis(**chart_axis)
        .configure_view(strokeWidth=0)
    )


def plot_releases_by_month(release_dates):
    check_columns({"date", "collection_id", "release_type", "release_count"}, release_dates)
    max_rows = 5000
    # check if number of rows is more than 5000
    if release_dates.shape[0] > max_rows:
        alt.data_transformers.disable_max_rows()

    # draw chart
    return (
        alt.Chart(release_dates)
        .mark_line(strokeWidth=3)
        .encode(
            x=alt.X("date", timeUnit="yearmonth", axis=alt.Axis(title="year and month")),
            y=alt.Y(
                "release_count",
                type="quantitative",
                aggregate="sum",
                axis=alt.Axis(title="number of releases", format="~s", tickCount=5),
                scale=alt.Scale(zero=False),
            ),
            color=alt.Color(
                "release_type",
                type="nominal",
                scale=alt.Scale(range=["#D6E100", "#FB6045", "#23B2A7", "#6C75E1"]),
                legend=alt.Legend(title="release type"),
            ),
            tooltip=[
                alt.Tooltip("date", timeUnit="yearmonth", title="date"),
                alt.Tooltip("release_count", aggregate="sum", title="number of releases"),
                alt.Tooltip("release_type", title="release type"),
            ],
        )
        .properties(**chart_properties)
        .configure_axis(**chart_axis)
        .configure_view(strokeWidth=0)
    )


def plot_objects_per_year(objects_per_year):
    check_columns({"year", "tenders", "awards"}, objects_per_year)
    stages = ["tenders", "awards"]
    return (
        alt.Chart(objects_per_year)
        .transform_fold(stages)
        .mark_line(strokeWidth=3)
        .encode(
            x=alt.X(
                "year",
                type="quantitative",
                axis=alt.Axis(title="year", format=".0f", tickCount=objects_per_year.shape[0]),
            ),
            y=alt.Y(
                "value",
                type="quantitative",
                axis=alt.Axis(title="number of objects", format="~s", tickCount=5),
                scale=alt.Scale(zero=False),
            ),
            color=alt.Color(
                "key",
                type="nominal",
                title="object type",
                scale=alt.Scale(domain=stages, range=["#D6E100", "#FB6045"]),
            ),
            tooltip=[
                alt.Tooltip("year", title="year", type="quantitative"),
                alt.Tooltip("value", title="number of objects", type="quantitative"),
                alt.Tooltip("key", title="object type", type="nominal"),
            ],
        )
        .properties(**chart_properties)
        .configure_axis(**chart_axis)
        .configure_view(strokeWidth=0)
    )


def plot_top_buyers(buyers):
    check_columns({"name", "total_tenders"}, buyers)
    return (
        alt.Chart(buyers)
        .mark_bar(fill="#d6e100")
        .encode(
            x=alt.X(
                "total_tenders",
                type="quantitative",
                axis=alt.Axis(title="number of tenders", format="~s", tickCount=5),
            ),
            y=alt.Y(
                "name",
                type="ordinal",
                axis=alt.Axis(title="buyer", labelAngle=0),
                sort=alt.SortField("total_tenders", order="descending"),
            ),
            tooltip=[
                alt.Tooltip("name", title="buyer", type="nominal"),
                alt.Tooltip("total_tenders", title="number of tenders", type="quantitative"),
            ],
        )
        .properties(**chart_properties)
        .configure_axis(**chart_axis)
        .configure_view(strokeWidth=0)
    )


def plot_usability_indicators(data, lang="English"):
    labels = {
        "English": {
            "nrow": "row_number(indicator)",
            "sort": "calculation",
            "y_sort": "indicator",
            "groupby": "Use case",
            "title": "number of indicators",
            "tooltip_missing": "Missing Fields",
        },
        "Spanish": {
            "nrow": "row_number(Indicador)",
            "sort": "¿Se puede calcular?",
            "y_sort": "Indicador",
            "groupby": "Caso de Uso",
            "title": "Número de indicadores",
            "tooltip_missing": "Campos faltantes",
        },
    }
    return (
        alt.Chart(data)
        .transform_window(
            nrow=labels[lang]["nrow"],
            frame=[None, None],
            sort=[{"field": labels[lang]["sort"]}],
            groupby=[labels[lang]["groupby"]],
        )
        .mark_circle(size=250, opacity=1)
        .encode(
            x=alt.X(
                "nrow",
                type="quantitative",
                axis=alt.Axis(title=[labels[lang]["title"], ""], orient="top", tickCount=5),
            ),
            y=alt.Y(
                labels[lang]["groupby"],
                type="nominal",
                sort=alt.Sort(field=labels[lang]["y_sort"], op="count", order="descending"),
            ),
            color=alt.Color(
                labels[lang]["sort"],
                type="nominal",
                scale=alt.Scale(range=["#fb6045", "#d6e100"]),
                legend=alt.Legend(title=[labels[lang]["sort"]]),
            ),
            tooltip=[
                alt.Tooltip(labels[lang]["y_sort"], type="nominal"),
                alt.Tooltip(labels[lang]["groupby"], type="nominal"),
                alt.Tooltip(labels[lang]["sort"], type="nominal"),
                alt.Tooltip(labels[lang]["tooltip_missing"], type="nominal"),
            ],
        )
        .properties(**chart_properties)
        .configure_axis(**chart_axis)
        .configure_view(strokeWidth=0)
    )
