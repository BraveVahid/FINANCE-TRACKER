import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def set_dark_theme():
    plt.style.use("dark_background")
    plt.rcParams.update({
        "figure.facecolor": "#333333",  
        "axes.facecolor": "#333333",    
        "text.color": "white",
        "axes.labelcolor": "white",
        "axes.edgecolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "legend.facecolor": "#333333",  
        "legend.edgecolor": "white",
        "figure.dpi": 100,
    })


class ChartGenerator:
    @staticmethod
    def create_pie_chart(data, frame, theme="Light"):
        plt.close("all")
        plt.style.use("default")

        if theme == "Dark":
            set_dark_theme()

        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        categories = list(data.keys())
        values = [data[cat]["percentage"] for cat in categories]

        if not values:
            if theme == "Light":
                text_color = "black"
            else:
                text_color = "white"

            ax.text(
                x=0.5,
                y=0.5,
                s="No expense data available",
                horizontalalignment="center",
                verticalalignment="center",
                color=text_color
            )

        else:
            colors = plt.cm.tab10(np.arange(len(categories)) % 10)
            _, texts, auto_texts = ax.pie(
                values,
                labels=categories,
                autopct="%1.1f%%",
                textprops={"fontsize": 8, "color": "black" if theme == "Light" else "white"},
                colors=colors
            )

            for text in texts:
                text.set_fontsize(7)

            for autotext in auto_texts:
                autotext.set_fontsize(7)

            title_color = "black" if theme == "Light" else "white"
            ax.set_title("Expense Breakdown", fontsize=10, color=title_color)

        fig.tight_layout()
        chart = FigureCanvasTkAgg(fig, frame)
        chart.draw()
        
        frame._chart_reference = chart
        return chart

    @staticmethod
    def create_bar_chart(data, frame, theme="Light"):
        plt.close("all")
        plt.style.use("default")
        
        if theme == "Dark":
            set_dark_theme()

        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        months = [item["month"] for item in data]
        incomes = [item["income"] for item in data]
        expenses = [item["expenses"] for item in data]
        x = np.arange(len(months))
        width = 0.35
        
        income_color = "#4CAF50"
        expense_color = "#F44336"
        
        ax.bar(x - width / 2, incomes, width, label="Income", color=income_color)
        ax.bar(x + width / 2, expenses, width, label="Expenses", color=expense_color)
        
        title_color = "black" if theme == "Light" else "white"
        ax.set_title("Monthly Income vs. Expenses", fontsize=10, color=title_color)
        ax.set_xticks(x)
        ax.set_xticklabels(months, fontsize=8, color=title_color)
        ax.tick_params(axis="y", labelsize=8, colors=title_color)
        legend = ax.legend(fontsize=8)

        if theme == "Dark":
            plt.setp(legend.get_texts(), color="white")

        ax.grid(True, linestyle="--", alpha=0.3)
        fig.tight_layout()
        chart = FigureCanvasTkAgg(fig, frame)
        chart.draw()
        
        frame._chart_reference = chart
        return chart

    @staticmethod
    def create_line_chart(data, frame, theme="Light"):
        plt.close("all")
        plt.style.use("default")
        
        if theme == "Dark":
            set_dark_theme()

        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        months = [item["month"] for item in data]
        balances = [item["balance"] for item in data]
        
        line_color = "#2196F3"
        
        ax.plot(months, balances, marker="o", linestyle="-", linewidth=2, color=line_color)
        ax.axhline(y=0, color="#9E9E9E", linestyle="--", alpha=0.7)
        
        ax.fill_between(months, balances, 0, where=(np.array(balances) > 0), color="#4CAF50", alpha=0.2)
        ax.fill_between(months, balances, 0, where=(np.array(balances) <= 0), color="#F44336", alpha=0.2)

        if theme == "Light":
            title_color = "black"
        else:
            title_color = "white"

        ax.set_title("Monthly Balance Trend", fontsize=10, color=title_color)
        x_positions = np.arange(len(months))
        ax.set_xticks(x_positions)
        ax.set_xticklabels(months, fontsize=8, rotation=45, color=title_color)
        ax.tick_params(axis="y", labelsize=8, colors=title_color)
        ax.grid(True, linestyle="--", alpha=0.3)
        fig.tight_layout()
        chart = FigureCanvasTkAgg(fig, frame)
        chart.draw()
        
        frame._chart_reference = chart
        return chart
