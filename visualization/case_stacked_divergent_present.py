import altair as alt

source = alt.pd.DataFrame([
      {
        "question": "1. Cross Junction",
        "type": "Very Unlikely",
        "value": 24,
        "percentage": 0,
        "percentage_start": -2.375,
        "percentage_end": -2.375
      },
      {
        "question": "1. Cross Junction",
        "type": "Unlikely",
        "value": 294,
        "percentage": 1.9,
        "percentage_start": -2.375,
        "percentage_end": -.475
      },
      {
        "question": "1. Cross Junction",
        "type": "Does Not Matter",
        "value": 594,
        "percentage": 0.95,
        "percentage_start": -.475,
        "percentage_end": 0.475
      },
      {
        "question": "1. Cross Junction",
        "type": "Likely",
        "value": 1927,
        "percentage": 20.95,
        "percentage_start": 0.475,
        "percentage_end": 21.425
      },
      {
        "question": "1. Cross Junction",
        "type": "Very Likely",
        "value": 376,
        "percentage": 76.19,
        "percentage_start": 21.425  ,
        "percentage_end": 97.615
      },

      {
        "question": "2. T Junction",
        "type": "Very Unlikely",
        "value": 2,
        "percentage": 0.95,
        "percentage_start": -6.185,
        "percentage_end": -5.235
      },
      {
        "question": "2. T Junction",
        "type": "Unlikely",
        "value": 2,
        "percentage": 1.91,
        "percentage_start": -5.235,
        "percentage_end": -3.335
      },
      {
        "question": "2. T Junction",
        "type": "Does Not Matter",
        "value": 0,
        "percentage": 6.67,
        "percentage_start": -3.335,
        "percentage_end": 3.335
      },
      {
        "question": "2. T Junction",
        "type": "Likely",
        "value": 7,
        "percentage": 28.05,
        "percentage_start": 3.335,
        "percentage_end": 31.385
      },
      {
        "question": "2. T Junction",
        "type": "Very Likely",
        "value": 11,
        "percentage": 61.09,
        "percentage_start": 31.385,
        "percentage_end": 92.475
      },

      {
        "question": "3. Y Junction",
        "type": "Very Unlikely",
        "value": 2,
        "percentage": 0,
        "percentage_start": -3.35,
        "percentage_end": -3.35
      },
      {
        "question": "3. Y Junction",
        "type": "Unlikely",
        "value": 0,
        "percentage": 0,
        "percentage_start": -3.35,
        "percentage_end": -3.35
      },
      {
        "question": "3. Y Junction",
        "type": "Does Not Matter",
        "value": 2,
        "percentage": 6.7,
        "percentage_start": -3.35,
        "percentage_end": 3.35
      },
      {
        "question": "3. Y Junction",
        "type": "Likely",
        "value": 4,
        "percentage": 42.8,
        "percentage_start": 3.35,
        "percentage_end": 46.15
      },
      {
        "question": "3. Y Junction",
        "type": "Very Likely",
        "value": 2,
        "percentage": 50.47,
        "percentage_start": 46.15,
        "percentage_end": 96.62
      },

      {
        "question": "4. Cross Junction",
        "type": "Very Unlikely",
        "value": 0,
        "percentage": 5.71,
        "percentage_start": -17.18,
        "percentage_end": -11.47
      },
      {
        "question": "4. Cross Junction",
        "type": "Unlikely",
        "value": 2,
        "percentage": 6.71,
        "percentage_start": -11.47,
        "percentage_end": -4.76
      },
      {
        "question": "4. Cross Junction",
        "type": "Does Not Matter",
        "value": 1,
        "percentage": 9.52,
        "percentage_start": -4.76,
        "percentage_end": 4.76
      },
      {
        "question": "4. Cross Junction",
        "type": "Likely",
        "value": 7,
        "percentage": 33.33,
        "percentage_start": 4.76,
        "percentage_end": 38.09
      },
      {
        "question": "4. Cross Junction",
        "type": "Very Likely",
        "value": 6,
        "percentage": 44.73,
        "percentage_start": 38.09,
        "percentage_end": 82.82
      },

      {
        "question": "5. Cross Junction",
        "type": "Very Unlikely",
        "value": 0,
        "percentage": 32.38,
        "percentage_start": -65.24,
        "percentage_end": -32.86
      },
      {
        "question": "5. Cross Junction",
        "type": "Unlikely",
        "value": 1,
        "percentage": 31.43,
        "percentage_start": -32.86,
        "percentage_end": -1.43
      },
      {
        "question": "5. Cross Junction",
        "type": "Does Not Matter",
        "value": 3,
        "percentage": 2.86,
        "percentage_start": -1.43,
        "percentage_end": 1.43
      },
      {
        "question": "5. Cross Junction",
        "type": "Likely",
        "value": 16,
        "percentage": 16.19,
        "percentage_start": 1.43,
        "percentage_end": 17.62
      },
      {
        "question": "5. Cross Junction",
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
    minExtent=30,
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


chart.save('case_divergent_chart.html')