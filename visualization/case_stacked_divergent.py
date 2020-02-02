import altair as alt

source = alt.pd.DataFrame([
      {
        "question": "Case 1",
        "type": "Very Unlikely",
        "value": 24,
        "percentage": 0,
        "percentage_start": -2.375,
        "percentage_end": -2.375
      },
      {
        "question": "Case 1",
        "type": "Unlikely",
        "value": 294,
        "percentage": 1.9,
        "percentage_start": -2.375,
        "percentage_end": -.475
      },
      {
        "question": "Case 1",
        "type": "Does Not Matter",
        "value": 594,
        "percentage": 0.95,
        "percentage_start": -.475,
        "percentage_end": 0.475
      },
      {
        "question": "Case 1",
        "type": "Likely",
        "value": 1927,
        "percentage": 20.95,
        "percentage_start": 0.475,
        "percentage_end": 21.425
      },
      {
        "question": "Case 1",
        "type": "Very Likely",
        "value": 376,
        "percentage": 76.19,
        "percentage_start": 21.425  ,
        "percentage_end": 97.615
      },

      {
        "question": "Case 2",
        "type": "Very Unlikely",
        "value": 2,
        "percentage": 0.95,
        "percentage_start": -6.185,
        "percentage_end": -5.235
      },
      {
        "question": "Case 2",
        "type": "Unlikely",
        "value": 2,
        "percentage": 1.91,
        "percentage_start": -5.235,
        "percentage_end": -3.335
      },
      {
        "question": "Case 2",
        "type": "Does Not Matter",
        "value": 0,
        "percentage": 6.67,
        "percentage_start": -3.335,
        "percentage_end": 3.335
      },
      {
        "question": "Case 2",
        "type": "Likely",
        "value": 7,
        "percentage": 28.05,
        "percentage_start": 3.335,
        "percentage_end": 31.385
      },
      {
        "question": "Case 2",
        "type": "Very Likely",
        "value": 11,
        "percentage": 61.09,
        "percentage_start": 31.385,
        "percentage_end": 92.475
      },

      {
        "question": "Case 3",
        "type": "Very Unlikely",
        "value": 2,
        "percentage": 0,
        "percentage_start": -3.35,
        "percentage_end": -3.35
      },
      {
        "question": "Case 3",
        "type": "Unlikely",
        "value": 0,
        "percentage": 0,
        "percentage_start": -3.35,
        "percentage_end": -3.35
      },
      {
        "question": "Case 3",
        "type": "Does Not Matter",
        "value": 2,
        "percentage": 6.7,
        "percentage_start": -3.35,
        "percentage_end": 3.35
      },
      {
        "question": "Case 3",
        "type": "Likely",
        "value": 4,
        "percentage": 42.8,
        "percentage_start": 3.35,
        "percentage_end": 46.15
      },
      {
        "question": "Case 3",
        "type": "Very Likely",
        "value": 2,
        "percentage": 50.47,
        "percentage_start": 46.15,
        "percentage_end": 96.62
      },

      {
        "question": "Case 4",
        "type": "Very Unlikely",
        "value": 0,
        "percentage": 5.71,
        "percentage_start": -17.18,
        "percentage_end": -11.47
      },
      {
        "question": "Case 4",
        "type": "Unlikely",
        "value": 2,
        "percentage": 6.71,
        "percentage_start": -11.47,
        "percentage_end": -4.76
      },
      {
        "question": "Case 4",
        "type": "Does Not Matter",
        "value": 1,
        "percentage": 9.52,
        "percentage_start": -4.76,
        "percentage_end": 4.76
      },
      {
        "question": "Case 4",
        "type": "Likely",
        "value": 7,
        "percentage": 33.33,
        "percentage_start": 4.76,
        "percentage_end": 38.09
      },
      {
        "question": "Case 4",
        "type": "Very Likely",
        "value": 6,
        "percentage": 44.73,
        "percentage_start": 38.09,
        "percentage_end": 82.82
      },

      {
        "question": "Case 5",
        "type": "Very Unlikely",
        "value": 0,
        "percentage": 32.38,
        "percentage_start": -65.24,
        "percentage_end": -32.86
      },
      {
        "question": "Case 5",
        "type": "Unlikely",
        "value": 1,
        "percentage": 31.43,
        "percentage_start": -32.86,
        "percentage_end": -1.43
      },
      {
        "question": "Case 5",
        "type": "Does Not Matter",
        "value": 3,
        "percentage": 2.86,
        "percentage_start": -1.43,
        "percentage_end": 1.43
      },
      {
        "question": "Case 5",
        "type": "Likely",
        "value": 16,
        "percentage": 16.19,
        "percentage_start": 1.43,
        "percentage_end": 17.62
      },
      {
        "question": "Case 5",
        "type": "Very Likely",
        "value": 4,
        "percentage": 17.14,
        "percentage_start": 17.62,
        "percentage_end": 34.76
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
    title='Case Study',
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

chart.save('case_divergent_chart.html')