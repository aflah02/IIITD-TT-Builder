import plotly.graph_objects as go
import streamlit as st
import json

def create_gantt_chart(courses):
    # Define the days of the week
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Sort courses based on their start time
    courses.sort(key=lambda course: (days_of_week.index(course["day"]), course["start_time"]))

    # Create a color mapping for courses with the same name
    color_mapping = {}
    color_index = 0

    # Create the Gantt chart traces
    data = []
    legend_entries = set()

    for course in courses:
        start_time = course["start_time"]
        end_time = course["end_time"]
        day_index = days_of_week.index(course["day"])
        y_val = days_of_week[day_index]

        # Assign a color to the course based on its name
        if course["name"] not in color_mapping:
            color_mapping[course["name"]] = color_index
            color_index += 1

        color = f"rgb({color_mapping[course['name']] * 50 % 256}, {color_mapping[course['name']] * 30 % 256}, {color_mapping[course['name']] * 80 % 256})"

        legend_entry = course["name"]
        if course["name"] in legend_entries:
            legend_entry = None
        else:
            legend_entries.add(course["name"])

        data.append(
            go.Scatter(
                x=[start_time, end_time],
                y=[y_val, y_val],
                mode="lines+markers",
                name=legend_entry,
                line=dict(width=20, color=color),
                marker=dict(symbol="line-ns-open", size=14, color=color),
            )
        )

    # Create the Gantt chart layout
    layout = go.Layout(
        title="Course Timetable",
        xaxis=dict(title="Time", type="category", range=["9:00", "18:00"], tickvals=[f"{'0' + str(h) if h < 10 else h}:00" for h in range(9, 19)], dtick="M1"),
        yaxis=dict(title="Day of the Week", type="category", categoryorder="array", categoryarray=days_of_week,
                   tickvals=list(range(len(days_of_week))), ticktext=days_of_week[::-1]),
        height=400,
        width=800,
    )

    # Create the figure and plot it
    fig = go.Figure(data=data, layout=layout)

    return fig

# read json courseDB.json
with open('courseDB_Monsoon_2023.json') as f:
    courseData = json.load(f)
with open('slotsMapping_Monsoon_2023.json') as f:
    slotsData = json.load(f)

courseNames = courseData.keys()

# Create streamlit app
st.title("Course Timetable")
st.markdown("This is a simple app to visualize your course timetable. To get started, select your courses from the multi-select box below.")

# Create a multi-select box for course selection
selected_courses = st.multiselect("Select your courses", courseNames)

# Get all course times

courses = []
for course in selected_courses:
    slots = courseData[course]["Slots"]
    room = courseData[course]["Room"]
    for slot in slots:
        if "Lunch" in slot:
            slotName = slot.split('-')[0] + '-' + slot.split('-')[1]
            slotDay = slot.split('-')[2]
            indexToDay = {'1': 'Monday', '2': 'Tuesday', '3': 'Wednesday', '4': 'Thursday', '5': 'Friday'}
            days = [indexToDay[slotDay]]
            slot = slotName
        else:
            days = slotsData[slot]["Days"]
        startTimes = slotsData[slot]["StartTime"]
        endTimes = slotsData[slot]["EndTime"]
        if slot == 'Slot9':
            startTimes = startTimes.split(',')
            endTimes = endTimes.split(',')
        else:
            startTimes = [startTimes]
            endTimes = [endTimes]

        if len(startTimes) == 1:
            startTimes = startTimes * len(days)
            endTimes = endTimes * len(days)
        for i in range(len(days)):
            courses.append({"name": course, "day": days[i], "start_time": startTimes[i], "end_time": endTimes[i], "room": room})

st.write(courses)

# button to show timetable
if st.button("Show Timetable"):
    # Create the Gantt chart
    fig = create_gantt_chart(courses)
    # Plot the Gantt chart
    st.plotly_chart(fig)