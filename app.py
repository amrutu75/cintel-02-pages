from shiny import App, ui, render
from shinywidgets import render_widget, output_widget
import plotly.express as px
from palmerpenguins import load_penguins
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
penguins_df = load_penguins()

# UI
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.h2("Penguin Sidebar"),
            ui.input_selectize(
                "selected_attribute", "Select attribute",
                ["bill_length_mm", "bill_depth_mm", "body_mass_g"]
            ),
            ui.input_numeric("plotly_bin_count", "Plotly Histogram Bins", value=200),
            ui.input_slider("seaborn_bin_count", "Seaborn Histogram Bins", 0, 200, 50),
            ui.input_checkbox_group(
                "selected_species_list", "Filter Species",
                ["Adelie", "Gentoo", "Chinstrap"],
                selected=["Adelie", "Gentoo", "Chinstrap"],
                inline=True
            )
        ),
        ui.layout_columns(
            ui.output_table("data_table"),
            ui.output_table("data_grid")
        ),
        output_widget("plotly_histogram"),
        ui.output_plot("seaborn_histogram"),
        output_widget("plotly_scatterplot"),  # ✅ Added scatter plot to UI
        ui.hr(),
        ui.a("GitHub", href="https://github.com/amrutu75/cintel-02-pages", target="_blank")
    )
)

# Server
def server(input, output, session):
    @output
    @render.table
    def data_table():
        return penguins_df

    @output
    @render.table
    def data_grid():
        return penguins_df

    @output
    @render_widget
    def plotly_histogram():
        col = input.selected_attribute()
        bins = input.plotly_bin_count()
        filtered_df = penguins_df[penguins_df["species"].isin(input.selected_species_list())]
        fig = px.histogram(
            filtered_df,
            x=col,
            nbins=int(bins),
            color="species",
            title=f"Plotly Histogram of {col}"
        )
        return fig

    @output
    @render.plot
    def seaborn_histogram():
        col = input.selected_attribute()
        bins = input.seaborn_bin_count()
        filtered_df = penguins_df[penguins_df["species"].isin(input.selected_species_list())]

        fig, ax = plt.subplots()
        sns.histplot(
            data=filtered_df,
            x=col,
            bins=int(bins),
            hue="species",
            ax=ax
        )
        ax.set_title(f"Seaborn Histogram of {col}")
        return fig

    @output
    @render_widget
    def plotly_scatterplot():
        filtered_df = penguins_df[penguins_df["species"].isin(input.selected_species_list())]
        fig = px.scatter(
            filtered_df,
            x="bill_depth_mm",
            y="bill_length_mm",
            color="species",
            symbol="species",
            labels={
                "bill_depth_mm": "Bill Depth (mm)",
                "bill_length_mm": "Bill Length (mm)"
            },
            title="Bill Depth vs. Bill Length by Penguin Species"
        )
        return fig

# App
app = App(app_ui, server)




