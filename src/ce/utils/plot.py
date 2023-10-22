import matplotlib.pyplot as plt
from typing import List

def quality_plots(data: List, categories: List[str]):
    # Create a scatter plot
    plt.figure(figsize=(10, 6))
    for i, category_data in enumerate(data):
        plt.scatter([i] * len(category_data), category_data, label=categories[i], alpha=0.7)

    # Customize the plot
    plt.xticks(range(len(categories)), categories)
    plt.xlabel('Algorithm')
    plt.ylabel('Performance')
    plt.title('Categorical Scatter Plot')
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.tight_layout()
    plt.show()