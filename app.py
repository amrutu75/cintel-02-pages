from shiny import App, ui, render
from palmerpenguins import load_penguins
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
penguins_df = load_penguins()

# UI
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.h2("Sidebar"),
            ui.input_selectize(
                "selected_attribute", "Select attribute",
                ["bill_length_mm", "bill_depth_mm", "body_mass_g"]
            ),
            ui.input_numeric("plotly_bin_count", "Plotly Histogram Bins", value=20),
            ui.input_slider("seaborn_bin_count", "Seaborn Histogram Bins", 0, 50, 20),
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

# App
app = App(app_ui, server)
        
