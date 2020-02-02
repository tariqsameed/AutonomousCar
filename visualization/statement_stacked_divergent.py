import altair as alt

source = alt.pd.DataFrame([
      {
        "question": "Statement 1",
        "type": "Very Unlikely",
        "value": 24,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
      },
      {
        "question": "Statement 1",
        "type": "Unlikely",
        "value": 294,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
      },
      {
        "question": "Statement 1",
        "type": "Does Not Matter",
        "value": 594,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
      },
      {
        "question": "Statement 1",
        "type": "Likely",
        "value": 1927,
        "percentage": 14.67,
        "percentage_start": 0,
        "percentage_end": 14.67
      },
      {
        "question": "Statement 1",
        "type": "Very Likely",
        "value": 376,
        "percentage": 85.33,
        "percentage_start": 14.67  ,
        "percentage_end": 100
      },

      {
        "question": "Statement 2",
        "type": "Very Unlikely",
        "value": 2,
        "percentage": 2.67,
        "percentage_start": -10.665,
        "percentage_end": -7.995
      },
      {
        "question": "Statement 2",
        "type": "Unlikely",
        "value": 2,
        "percentage": 5.33,
        "percentage_start": -7.995,
        "percentage_end": -2.665
      },
      {
        "question": "Statement 2",
        "type": "Does Not Matter",
        "value": 0,
        "percentage": 5.33,
        "percentage_start": -2.665,
        "percentage_end": 2.665
      },
      {
        "question": "Statement 2",
        "type": "Likely",
        "value": 7,
        "percentage": 38.66,
        "percentage_start": 2.665,
        "percentage_end": 41.325
      },
      {
        "question": "Statement 2",
        "type": "Very Likely",
        "value": 11,
        "percentage": 48,
        "percentage_start": 41.325,
        "percentage_end": 89.325
      },

      {
        "question": "Statement 3",
        "type": "Very Unlikely",
        "value": 2,
        "percentage": 6.67,
        "percentage_start": -27.34,
        "percentage_end": -20.67
      },
      {
        "question": "Statement 3",
        "type": "Unlikely",
        "value": 0,
        "percentage": 14.67,
        "percentage_start": -20.67,
        "percentage_end": -6
      },
      {
        "question": "Statement 3",
        "type": "Does Not Matter",
        "value": 2,
        "percentage": 12,
        "percentage_start": -6,
        "percentage_end": 6
      },
      {
        "question": "Statement 3",
        "type": "Likely",
        "value": 4,
        "percentage": 30.67,
        "percentage_start": 6,
        "percentage_end": 36.67
      },
      {
        "question": "Statement 3",
        "type": "Very Likely",
        "value": 2,
        "percentage": 36,
        "percentage_start": 36.67,
        "percentage_end": 72.67
      },

      {
        "question": "Statement 4",
        "type": "Very Unlikely",
        "value": 0,
        "percentage": 14.67,
        "percentage_start": -20,
        "percentage_end": -5.33
      },
      {
        "question": "Statement 4",
        "type": "Unlikely",
        "value": 2,
        "percentage": 5.33,
        "percentage_start": -5.33,
        "percentage_end": 0
      },
      {
        "question": "Statement 4",
        "type": "Does Not Matter",
        "value": 1,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
      },
      {
        "question": "Statement 4",
        "type": "Likely",
        "value": 7,
        "percentage": 21.33,
        "percentage_start": 0,
        "percentage_end": 21.33
      },
      {
        "question": "Statement 4",
        "type": "Very Likely",
        "value": 6,
        "percentage": 58.66,
        "percentage_start": 21.33,
        "percentage_end": 79.99
      },

      {
        "question": "Statement 5",
        "type": "Very Unlikely",
        "value": 0,
        "percentage": 16,
        "percentage_start": -29.995,
        "percentage_end": -13.995
      },
      {
        "question": "Statement 5",
        "type": "Unlikely",
        "value": 1,
        "percentage": 10.66,
        "percentage_start": -13.995,
        "percentage_end": -3.335
      },
      {
        "question": "Statement 5",
        "type": "Does Not Matter",
        "value": 3,
        "percentage": 6.67,
        "percentage_start": -3.335,
        "percentage_end": 3.335
      },
      {
        "question": "Statement 5",
        "type": "Likely",
        "value": 16,
        "percentage": 33.33,
        "percentage_start": 3.335,
        "percentage_end": 36.665
      },
      {
        "question": "Statement 5",
        "type": "Very Likely",
        "value": 4,
        "percentage": 33.33,
        "percentage_start": 36.665,
        "percentage_end": 69.995
      },

    {
        "question": "Statement 6",
        "type": "Very Unlikely",
        "value": 0,
        "percentage": 6.67,
        "percentage_start": -23.995,
        "percentage_end": -17.325
    },
    {
        "question": "Statement 6",
        "type": "Unlikely",
        "value": 1,
        "percentage": 10.66,
        "percentage_start": -17.325,
        "percentage_end": -6.665
    },
    {
        "question": "Statement 6",
        "type": "Does Not Matter",
        "value": 3,
        "percentage": 13.33,
        "percentage_start": -6.665,
        "percentage_end": 6.665
    },
    {
        "question": "Statement 6",
        "type": "Likely",
        "value": 16,
        "percentage": 36,
        "percentage_start": 6.665,
        "percentage_end": 42.665
    },
    {
        "question": "Statement 6",
        "type": "Very Likely",
        "value": 4,
        "percentage": 33.33,
        "percentage_start": 42.665,
        "percentage_end": 75.995
    },

    {
        "question": "Statement 7",
        "type": "Very Unlikely",
        "value": 0,
        "percentage": 8,
        "percentage_start": -20,
        "percentage_end": -12
    },
    {
        "question": "Statement 7",
        "type": "Unlikely",
        "value": 1,
        "percentage": 12,
        "percentage_start": -12,
        "percentage_end": 0
    },
    {
        "question": "Statement 7",
        "type": "Does Not Matter",
        "value": 3,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
    },
    {
        "question": "Statement 7",
        "type": "Likely",
        "value": 16,
        "percentage": 24,
        "percentage_start": 0,
        "percentage_end": 24
    },
    {
        "question": "Statement 7",
        "type": "Very Likely",
        "value": 4,
        "percentage": 56,
        "percentage_start": 24,
        "percentage_end": 80
    },
])

color_scale = alt.Scale(
    domain=[
        "Very Unlikely",
        "Unlikely",
        "Does Not Matter",
        "Likely",
        "Very Likely"
    ],
    range=["#c30d24", "#f3a583", "#cccccc", "#94c6da", "#1770ab"]
)

y_axis = alt.Axis(
    title='Statement Study',
    offset=5,
    ticks=False,
    minExtent=60,
    domain=False
)

chart = alt.Chart(source).mark_bar().encode(
    x='percentage_start:Q',
    x2='percentage_end:Q',
    y=alt.Y('question:N', axis=y_axis),
    color=alt.Color(
        'type:N',
        legend=alt.Legend( title='Response'),
        scale=color_scale,
    )
)

chart.save('statement_divergent_chart.html')