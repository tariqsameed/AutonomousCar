import altair as alt

source = alt.pd.DataFrame([
      {
        "question": "Post-Crash Features",
        "type": "Very Unlikely",
        "value": 24,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
      },
      {
        "question": "Post-Crash Features",
        "type": "Unlikely",
        "value": 294,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
      },
      {
        "question": "Post-Crash Features",
        "type": "Does Not Matter",
        "value": 594,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
      },
      {
        "question": "Post-Crash Features",
        "type": "Likely",
        "value": 1927,
        "percentage": 14.67,
        "percentage_start": 0,
        "percentage_end": 14.67
      },
      {
        "question": "Post-Crash Features",
        "type": "Very Likely",
        "value": 376,
        "percentage": 85.33,
        "percentage_start": 14.67  ,
        "percentage_end": 100
      },

      {
        "question": "Road Geometry",
        "type": "Very Unlikely",
        "value": 2,
        "percentage": 2.67,
        "percentage_start": -10.665,
        "percentage_end": -7.995
      },
      {
        "question": "Road Geometry",
        "type": "Unlikely",
        "value": 2,
        "percentage": 5.33,
        "percentage_start": -7.995,
        "percentage_end": -2.665
      },
      {
        "question": "Road Geometry",
        "type": "Does Not Matter",
        "value": 0,
        "percentage": 5.33,
        "percentage_start": -2.665,
        "percentage_end": 2.665
      },
      {
        "question": "Road Geometry",
        "type": "Likely",
        "value": 7,
        "percentage": 38.66,
        "percentage_start": 2.665,
        "percentage_end": 41.325
      },
      {
        "question": "Road Geometry",
        "type": "Very Likely",
        "value": 11,
        "percentage": 48,
        "percentage_start": 41.325,
        "percentage_end": 89.325
      },

      {
        "question": "Trajectory",
        "type": "Very Unlikely",
        "value": 2,
        "percentage": 6.67,
        "percentage_start": -27.34,
        "percentage_end": -20.67
      },
      {
        "question": "Trajectory",
        "type": "Unlikely",
        "value": 0,
        "percentage": 14.67,
        "percentage_start": -20.67,
        "percentage_end": -6
      },
      {
        "question": "Trajectory",
        "type": "Does Not Matter",
        "value": 2,
        "percentage": 12,
        "percentage_start": -6,
        "percentage_end": 6
      },
      {
        "question": "Trajectory",
        "type": "Likely",
        "value": 4,
        "percentage": 30.67,
        "percentage_start": 6,
        "percentage_end": 36.67
      },
      {
        "question": "Trajectory",
        "type": "Very Likely",
        "value": 2,
        "percentage": 36,
        "percentage_start": 36.67,
        "percentage_end": 72.67
      },

      {
        "question": "Damaged Area",
        "type": "Very Unlikely",
        "value": 0,
        "percentage": 14.67,
        "percentage_start": -20,
        "percentage_end": -5.33
      },
      {
        "question": "Damaged Area",
        "type": "Unlikely",
        "value": 2,
        "percentage": 5.33,
        "percentage_start": -5.33,
        "percentage_end": 0
      },
      {
        "question": "Damaged Area",
        "type": "Does Not Matter",
        "value": 1,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
      },
      {
        "question": "Damaged Area",
        "type": "Likely",
        "value": 7,
        "percentage": 21.33,
        "percentage_start": 0,
        "percentage_end": 21.33
      },
      {
        "question": "Damaged Area",
        "type": "Very Likely",
        "value": 6,
        "percentage": 58.66,
        "percentage_start": 21.33,
        "percentage_end": 79.99
      },

      {
        "question": "Collision Location",
        "type": "Very Unlikely",
        "value": 0,
        "percentage": 16,
        "percentage_start": -29.995,
        "percentage_end": -13.995
      },
      {
        "question": "Collision Location",
        "type": "Unlikely",
        "value": 1,
        "percentage": 10.66,
        "percentage_start": -13.995,
        "percentage_end": -3.335
      },
      {
        "question": "Collision Location",
        "type": "Does Not Matter",
        "value": 3,
        "percentage": 6.67,
        "percentage_start": -3.335,
        "percentage_end": 3.335
      },
      {
        "question": "Collision Location",
        "type": "Likely",
        "value": 16,
        "percentage": 33.33,
        "percentage_start": 3.335,
        "percentage_end": 36.665
      },
      {
        "question": "Collision Location",
        "type": "Very Likely",
        "value": 4,
        "percentage": 33.33,
        "percentage_start": 36.665,
        "percentage_end": 69.995
      },

    {
        "question": "Car Control",
        "type": "Very Unlikely",
        "value": 0,
        "percentage": 6.67,
        "percentage_start": -23.995,
        "percentage_end": -17.325
    },
    {
        "question": "Car Control",
        "type": "Unlikely",
        "value": 1,
        "percentage": 10.66,
        "percentage_start": -17.325,
        "percentage_end": -6.665
    },
    {
        "question": "Car Control",
        "type": "Does Not Matter",
        "value": 3,
        "percentage": 13.33,
        "percentage_start": -6.665,
        "percentage_end": 6.665
    },
    {
        "question": "Car Control",
        "type": "Likely",
        "value": 16,
        "percentage": 36,
        "percentage_start": 6.665,
        "percentage_end": 42.665
    },
    {
        "question": "Car Control",
        "type": "Very Likely",
        "value": 4,
        "percentage": 33.33,
        "percentage_start": 42.665,
        "percentage_end": 75.995
    },

    {
        "question": "Expected Simulation",
        "type": "Very Unlikely",
        "value": 0,
        "percentage": 8,
        "percentage_start": -20,
        "percentage_end": -12
    },
    {
        "question": "Expected Simulation",
        "type": "Unlikely",
        "value": 1,
        "percentage": 12,
        "percentage_start": -12,
        "percentage_end": 0
    },
    {
        "question": "Expected Simulation",
        "type": "Does Not Matter",
        "value": 3,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
    },
    {
        "question": "Expected Simulation",
        "type": "Likely",
        "value": 16,
        "percentage": 24,
        "percentage_start": 0,
        "percentage_end": 24
    },
    {
        "question": "Expected Simulation",
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
    x=alt.X('percentage_start:Q', title='Percentage'),
    x2='percentage_end:Q',
    y=alt.Y('question:N', axis=y_axis),
    color=alt.Color(
        'type:N',
        legend=alt.Legend( title='Response'),
        scale=color_scale,
    )
).properties(
    width=200,
    height=200
)

chart.save('statement_divergent_chart.html')