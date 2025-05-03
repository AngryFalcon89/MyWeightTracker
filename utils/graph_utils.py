import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta  # Added timedelta import
from config import ACCENT_COLOR, GRAPH_BG_COLOR, SKIP_COLOR

def create_weight_graph(dates, pre_weights, post_weights, skipped_dates):
    fig, ax = plt.subplots(figsize=(9, 6))
    fig.patch.set_facecolor(GRAPH_BG_COLOR)
    ax.set_facecolor("#ffffff")
    
    # Convert dates if they're strings
    if dates and isinstance(dates[0], str):
        dates = [datetime.strptime(d, "%d-%m-%Y") for d in dates]
    
    # Plot pre-gym weights
    if pre_weights and dates:
        ax.plot(dates, pre_weights, 'o-', color=ACCENT_COLOR, label='Pre-gym Weight')
    
    # Plot post-gym weights
    if post_weights and dates:
        ax.plot(dates, post_weights, 's--', color='#34c759', label='Post-gym Weight')
    
    # Plot skipped days
    if skipped_dates:
        for sd in skipped_dates:
            if isinstance(sd, str):
                sd = datetime.strptime(sd, "%d-%m-%Y")
            ax.axvline(x=sd, color=SKIP_COLOR, linestyle=':', alpha=0.5)
        ax.plot([], [], ':', color=SKIP_COLOR, label='Skipped Days')
    
    # Add trend line if enough data
    if dates and len(pre_weights) > 2:
        try:
            x = [d.toordinal() for d in dates]
            y = pre_weights
            coeffs = np.polyfit(x, y, 1)
            trend_line = np.poly1d(coeffs)
            
            future_dates = [min(dates), max(dates) + timedelta(weeks=2)]
            future_x = [d.toordinal() for d in future_dates]
            ax.plot(future_dates, trend_line(future_x), ':', color='#ff9500', label='Trend Line')
            
            projection_date = max(dates) + timedelta(weeks=2)
            projection_weight = trend_line(projection_date.toordinal())
            ax.annotate(
                f'Projection: {projection_weight:.1f} kg',
                xy=(projection_date, projection_weight),
                xytext=(10, 10),
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8),
                arrowprops=dict(arrowstyle='->')
            )
        except Exception as e:
            print(f"Couldn't create trend line: {e}")
    
    # Format graph
    ax.set_title('Weight Over Time', pad=20)
    ax.set_xlabel('Date')
    ax.set_ylabel('Weight (kg)')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    fig.autofmt_xdate()
    
    return fig