# outputs.py

import plotly.express as px
import plotly.graph_objects as go

MONTHS = [
    'January--Magh','February--Falgun','March--Chaitra','April--Boishakh',
    'May--Jeystho','June--Asharh','July--Srabon','August--Bhadro',
    'September--Ashwin','October--Kartik','November--Aghrahan','December--Poush'
]


def plot_q3_source_bar(df):
    """Q3: Number of rows for each fishing source."""
    fig = px.bar(
        df,
        x='Source Desc',
        y='Count',
        labels={'Source Desc': 'Source of Fishing', 'Count': 'Number of Instances'},
        title='<b>Number of Rows Representing Each Fishing Source (Fishers Dataset)</b>',
        color='Source Desc',
        text='Count'
    )
    fig.update_layout(
        xaxis_title='Name of Fishing Source',
        yaxis_title='Number of Instances (Rows)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20)),
        margin=dict(l=70, r=10, t=100, b=60),
        width=1300,
        height=750,
        legend=dict(x=0.85, y=0.99, traceorder='normal', bgcolor='rgba(255,255,255,1)')
    )
    fig.update_traces(textposition='outside')
    return fig


def plot_q3_source_grouped_bar(df):
    """Q3: Grouped overview after merging small categories into Others."""
    d = df.copy()
    d['Source Desc'] = d['Source Desc'].replace(['Fish Farming in Cages','Mohona'], 'Others')
    d = d.groupby('Source Desc', as_index=False)['Count'].sum()
    d = d.sort_values('Count', ascending=False)
    fig = px.bar(
        d,
        x='Source Desc',
        y='Count',
        labels={'Source Desc': 'Source of Fishing', 'Count': 'Number of Instances'},
        title='<b>Number of Rows Representing Each Fishing Source (Fishers Dataset)</b>',
        color='Source Desc',
        text='Count'
    )
    fig.update_layout(
        xaxis_title='Name of Fishing Source',
        yaxis_title='Number of Instances (Rows)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20)),
        margin=dict(l=70, r=10, t=100, b=60),
        width=1300,
        height=750,
        legend=dict(x=0.85, y=0.99, traceorder='normal', bgcolor='rgba(255,255,255,1)')
    )
    fig.update_traces(textposition='outside')
    return fig


def plot_q4_monthly_catch_bar(df):
    """Q4: Total monthly catch bar chart."""
    d = df.copy()
    d['Total_with_unit'] = d['Total'].astype(str) + ' (mt)'
    fig = px.bar(
        d,
        x='Month',
        y='Total',
        title='<b>Total Monthly Catch for All Fish Species (Metric Tonnes)</b>',
        text='Total_with_unit'
    )
    fig.update_layout(
        xaxis_title='Name of Month',
        yaxis_title='Total Catch Amount (Metric Tonnes)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20), tickformat='.0f'),
        margin=dict(l=70, r=10, t=100, b=60),
        width=1300,
        height=750
    )
    fig.update_traces(textposition='outside')
    return fig


def plot_q4_monthly_catch_line(df):
    """Q4: Total monthly catch line chart."""
    fig = px.line(
        df,
        x='Month',
        y='Total',
        title='<b>Total Monthly Catch for All Fish Species (Metric Tonnes)</b>',
        labels={'Month': 'Name of Month', 'Total': 'Total Catch Amount (Metric Tonnes)'},
        markers=True
    )
    fig.update_layout(
        xaxis_title='Name of Month',
        yaxis_title='Total Catch Amount (Metric Tonnes)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20), tickformat='.0f'),
        margin=dict(l=70, r=20, t=100, b=60),
        width=1300,
        height=750
    )
    return fig


def plot_q4_monthly_catch_area(df):
    """Q4: Total monthly catch area chart."""
    fig = px.area(
        df,
        x='Month',
        y='Total',
        title='<b>Total Monthly Catch for All Fish Species (Metric Tonnes)</b>',
        labels={'Month': 'Name of Month', 'Total': 'Total Catch Amount (Metric Tonnes)'}
    )
    fig.update_layout(
        xaxis_title='Name of Month',
        yaxis_title='Total Catch Amount (Metric Tonnes)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20), tickformat='.0f'),
        margin=dict(l=70, r=20, t=100, b=60),
        width=1300,
        height=750
    )
    return fig


def plot_q4_top_species_bar(df):
    """Q4: Yearly totals for top 10 species bar chart."""
    d = df.copy()
    d['Total_with_unit'] = d['Year Total'].astype(str) + ' (mt)'
    fig = px.bar(
        d,
        x='Fish Name',
        y='Year Total',
        title='<b>Yearly Catch Totals for The Top 10 Fish Species (Metric Tonnes)</b>',
        text='Total_with_unit',
        color='Fish Name',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig.update_layout(
        xaxis_title='Name of Fish Species',
        yaxis_title='Total Catch Amount (Metric Tonnes)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20), tickformat='.0f'),
        margin=dict(l=70, r=10, t=100, b=60),
        width=1300,
        height=750,
        legend=dict(x=0.89, y=0.99, traceorder='normal', bgcolor='rgba(255,255,255,1)')
    )
    fig.update_traces(textposition='outside')
    return fig


def plot_q4_top_species_box(df):
    """Q4: Box plot of monthly catch for top species."""
    long = df.melt(
        id_vars=["Fish Name", "Year Total"],
        value_vars=MONTHS,
        var_name="Month",
        value_name="Catch"
    )
    fig = px.box(
        long,
        x='Fish Name',
        y='Catch',
        title='<b>Box Plot of Monthly Catch for Top 10 Fish Species (Metric Tonnes)</b>',
        labels={'Catch':'Monthly Catch Totals','Fish Name':'Fish Species'}
    )
    fig.update_layout(
        xaxis_title='Name of Fish Species',
        yaxis_title='Monthly Catch (Metric Tonnes)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20), tickformat='.0f'),
        margin=dict(l=70, r=10, t=100, b=60),
        width=1300,
        height=750
    )
    return fig


def plot_q4_top_species_stacked_bar(df):
    """Q4: Stacked bar chart of monthly catch by species."""
    long = df.melt(
        id_vars=["Fish Name", "Year Total"],
        value_vars=MONTHS,
        var_name="Month",
        value_name="Catch"
    )
    fig = px.bar(
        long,
        x='Month',
        y='Catch',
        color='Fish Name',
        title='<b>Stacked Bar Chart of Top 10 Fish Species (Metric Tonnes)</b>'
    )
    fig.update_layout(
        xaxis_title='Name of Month',
        yaxis_title='Monthly Catch (Metric Tonnes)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20)),
        margin=dict(l=70, r=10, t=100, b=60),
        width=1300,
        height=750,
        legend=dict(x=0.01, y=0.99, traceorder='normal', bgcolor='rgba(255,255,255,1)')
    )
    return fig


def plot_q4_top_species_line(df):
    """Q4: Line chart of monthly catch for each top species."""
    fig = go.Figure()
    for fish in df['Fish Name']:
        vals = df[df['Fish Name'] == fish][MONTHS].values.flatten()
        fig.add_trace(go.Scatter(
            x=MONTHS,
            y=vals,
            mode='lines+markers',
            name=fish
        ))
    fig.update_layout(
        title='<b>Monthly Catch Totals for Each Fish Species (Metric Tonnes)</b>',
        xaxis_title='Name of Month',
        yaxis_title='Monthly Catch (Metric Tonnes)',
        title_font_size=24,
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20), tickformat='.0f'),
        margin=dict(l=70, r=20, t=100, b=60),
        width=1300,
        height=750,
        legend=dict(x=0.01, y=0.99, traceorder='normal', bgcolor='rgba(255,255,255,1)')
    )
    return fig


def plot_q5_annual_catch_by_source_bar(df):
    """Q5: Total annual catch by source bar chart."""
    d = df.copy().sort_values('Total', ascending=False)
    d['Total_with_unit'] = d['Total'].astype(str) + ' (mt)'
    fig = px.bar(
        d,
        x='Source',
        y='Total',
        title='<b>Total Annual Catch by Source (Metric Tonnes)</b>',
        labels={'Total':'Total Catch (Metric Tonnes)'},
        text='Total_with_unit',
        color='Source',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig.update_layout(
        xaxis_title='Name of Fishing Source',
        yaxis_title='Total Catch (Metric Tonnes)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20)),
        margin=dict(l=70, r=10, t=100, b=60),
        width=1300,
        height=750,
        legend=dict(x=0.85, y=0.99, traceorder='normal', bgcolor='rgba(255,255,255,1)')
    )
    fig.update_traces(textposition='outside')
    return fig


def plot_q5_monthly_catch_by_source_line(df):
    """Q5: Monthly catch totals by source line chart."""
    fig = go.Figure()
    for src in df['Source']:
        vals = df[df['Source'] == src][MONTHS].values.flatten()
        fig.add_trace(go.Scatter(
            x=MONTHS,
            y=vals,
            mode='lines+markers',
            name=src
        ))
    fig.update_layout(
        title='<b>Monthly Catch Totals by Source (Metric Tonnes)</b>',
        xaxis_title='Name of Month',
        yaxis_title='Monthly Catch (Metric Tonnes)',
        title_font_size=24,
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20), tickformat='.0f'),
        margin=dict(l=70, r=20, t=100, b=60),
        width=1300,
        height=750,
        legend=dict(x=0.01, y=0.99, traceorder='normal', bgcolor='rgba(255,255,255,1)')
    )
    return fig


def plot_q6_monthly_waste_bar(df):
    """Q6: Total monthly wastage bar chart."""
    d = df.copy()
    d['Total_with_unit'] = d['Total'].astype(str) + ' (mt)'
    fig = px.bar(
        d,
        x='Month',
        y='Total',
        title='<b>Total Monthly Wastage for All Fish Species (Metric Tonnes)</b>',
        text='Total_with_unit'
    )
    fig.update_layout(
        xaxis_title='Name of Month',
        yaxis_title='Total Wastage (Metric Tonnes)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20), tickformat='.0f'),
        margin=dict(l=70, r=10, t=100, b=60),
        width=1300,
        height=750
    )
    fig.update_traces(textposition='outside')
    return fig


def plot_q6_monthly_waste_line(df):
    """Q6: Total monthly wastage line chart."""
    fig = px.line(
        df,
        x='Month',
        y='Total',
        title='<b>Total Monthly Wastage for All Fish Species (Metric Tonnes)</b>',
        labels={'Month': 'Name of Month', 'Total': 'Total Wastage (Metric Tonnes)'},
        markers=True
    )
    fig.update_layout(
        xaxis_title='Name of Month',
        yaxis_title='Total Wastage (Metric Tonnes)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20), tickformat='.0f'),
        margin=dict(l=70, r=20, t=100, b=60),
        width=1300,
        height=750
    )
    return fig


def plot_q6_monthly_waste_area(df):
    """Q6: Total monthly wastage area chart."""    
    fig = px.area(
        df,
        x='Month',
        y='Total',
        title='<b>Total Monthly Wastage for All Fish Species (Metric Tonnes)</b>',
        labels={'Month': 'Name of Month', 'Total': 'Total Wastage (Metric Tonnes)'}
    )
    fig.update_layout(
        xaxis_title='Name of Month',
        yaxis_title='Total Wastage (Metric Tonnes)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20), tickformat='.0f'),
        margin=dict(l=70, r=20, t=100, b=60),
        width=1300,
        height=750
    )
    return fig


def plot_q6_top_waste_species_bar(df):
    """Q6: Yearly wastage totals for top species bar chart."""
    d = df.copy()
    d['Total_with_unit'] = d['Year Total'].astype(str) + ' (mt)'
    fig = px.bar(
        d,
        x='Fish Name',
        y='Year Total',
        title='<b>Yearly Wastage Totals for The Top 10 Fish Species (Metric Tonnes)</b>',
        text='Total_with_unit',
        color='Fish Name',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig.update_layout(
        xaxis_title='Name of Fish Species',
        yaxis_title='Total Wastage (Metric Tonnes)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20), tickformat='.0f'),
        margin=dict(l=70, r=10, t=100, b=60),
        width=1300,
        height=750,
        legend=dict(x=0.85, y=0.99, traceorder='normal', bgcolor='rgba(255,255,255,1)')
    )
    fig.update_traces(textposition='outside')
    return fig


def plot_q6_top_waste_species_box(df):
    """Q6: Box plot of monthly wastage for top species."""
    long = df.melt(
        id_vars=["Fish Name", "Year Total"],
        value_vars=MONTHS,
        var_name="Month",
        value_name="Waste"
    )
    fig = px.box(
        long,
        x='Fish Name',
        y='Waste',
        title='<b>Box Plot of Monthly Wastage for Top 10 Fish Species (Metric Tonnes)</b>'
    )
    fig.update_layout(
        xaxis_title='Name of Fish Species',
        yaxis_title='Monthly Wastage (Metric Tonnes)',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20), tickformat='.0f'),
        margin=dict(l=70, r=10, t=100, b=60),
        width=1300,
        height=750,
        legend=dict(x=0.85, y=0.99, traceorder='normal', bgcolor='rgba(255,255,255,1)')
    )
    return fig


def plot_q7_loss_by_reason_bar(df):
    """Q7: Total fish wastage by reason horizontal bar chart."""
    d = df.copy()
    d['Total_with_unit'] = d['total_quantity_lost_mt'].round(2).astype(str) + ' (mt)'
    fig = px.bar(
        d,
        x='total_quantity_lost_mt',
        y='Reason',
        orientation='h',
        title='<b>Total Fish Wastage by Reason (Metric Tonnes)</b>',
        text='Total_with_unit',
        color='Reason',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig.update_layout(
        xaxis_title='Total Quantity Lost (Metric Tonnes)',
        yaxis_title='Reason for Waste',
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(tickmode='linear', title_font=dict(size=20)),
        margin=dict(l=50, r=10, t=100, b=60),
        width=1500,
        height=750,
        legend=dict(x=0.75, y=0.01, traceorder='normal', bgcolor='rgba(255,255,255,1)')
    )
    fig.update_traces(textposition='outside')
    return fig


def plot_q12_distribution_sankey(df):
    """Q12: Sankey diagram of fish distribution channels."""
    sources, targets, values = [], [], []
    fish_types = df['q12_b1_nam'].tolist()
    dests = df.columns[1:-1].tolist()
    nodes = fish_types + dests
    mapping = {n: i for i, n in enumerate(nodes)}
    for _, row in df.iterrows():
        for dest in dests:
            v = row[dest]
            if v > 0:
                sources.append(mapping[row['q12_b1_nam']])
                targets.append(mapping[dest])
                values.append(v)
    colors = ['#636EFA','#EF553B','#00CC96','#AB63FA','#FFA15A',
              '#19D3F3','#FF6692','#B6E880','#FF97FF','#FECB52']
    fish_colors = colors * ((len(fish_types)//len(colors))+1)
    node_colors = fish_colors[:len(fish_types)] + ['#A9A9A9']*len(dests)
    fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=25,
                  line=dict(color="black", width=0.8),
                  label=nodes, color=node_colors),
        link=dict(source=sources, target=targets, value=values,
                  hovertemplate='From %{source.label} to %{target.label}: %{value} MT<extra></extra>')
    )])
    fig.update_layout(
        title_text="<b>Flow of Fish Species to Different Destinations (Metric Tonnes)</b>",
        title={'x':0.5,'xanchor':'center','font':{'size':24}},
        font_size=12, autosize=True, height=900,
        margin=dict(l=20, r=20, t=80, b=20), paper_bgcolor='white'
    )
    return fig
