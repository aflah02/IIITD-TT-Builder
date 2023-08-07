import plotly.graph_objects as go
import streamlit as st
import json
# light colors
colors = [
    'red',
    'blue',
    'green',
    'orange',
    'pink',
    'cyan',
    'yellow',
    'lightgreen',
]

mem = {}

def create_gantt_chart(courses):
    # Define the days of the week
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Sort courses based on their start time
    courses.sort(key=lambda course: (days_of_week.index(course["day"]), course["start_time"]))

    # Create the Gantt chart traces
    data = []
    for course in courses:
        start_time = course["start_time"]
        end_time = course["end_time"]
        day_index = days_of_week.index(course["day"])
        y_val = days_of_week[day_index]

        if (course["name"] in mem):
            color = mem[course["name"]]
        else:
            color = colors.pop()
            mem[course["name"]] = color

        data.append(
            go.Scatter(
                x=[start_time, end_time],
                y=[y_val, y_val],
                mode="lines+markers",
                name=course["name"],
                line=dict(width=20, color=color),
                marker=dict(symbol="line-ns-open", size=14, color=color),
            )
        )

        print(data)

        # Add Annotations inside the Gantt chart
        data.append(
            go.Scatter(
                x=[start_time, end_time],
                y=[y_val, y_val],
                mode="text",
                name=course["name"],
                text=[course["name"]+" "+course["room"]],
                textposition="top center",
                textfont=dict(color="black"),
            )
        )

    # Create the Gantt chart layout
    layout = go.Layout(
        title="Course Timetable",
        xaxis=dict(title="Time", type="category", range=["9:30", "18:00"]),
        yaxis=dict(title="Day of the Week", type="category", categoryorder="array", categoryarray=days_of_week, range=[days_of_week[-1], days_of_week[0]]),
        height=400,
        width=800,
    )

    # remove legend
    layout.update(showlegend=False)

    # Create the figure and plot it
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(autorange="reversed")  # Reverse the order of the y-axis (days of the week)
    # sort the x-axis
    x_axis_order = ['09:30', '11:00', '12:30', '13:30', '14:00', '15:00', '16:30', '18:00']
    fig.update_xaxes(categoryorder='array', categoryarray=x_axis_order)
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    return fig

with open('courseDB_Monsoon_2023.json') as f:
    courseData = json.load(f)
with open('slotsMapping_Monsoon_2023.json') as f:
    slotsData = json.load(f)

courseNames = courseData.keys()

# Create streamlit app
st.title("Course Timetable")

st.write(
    "Note: The data may be error prone, please report any errors you find and don't blame me if you miss a class because of this app xD"
)

st.markdown("This is a simple app to visualize your course timetable. To get started, select your courses from the multi-select box below.")

# Create a multi-select box for course selection
selected_courses = st.multiselect("Select your courses", courseNames)

# Add 3 Meeting slots
st.markdown("## Meeting Slots")
st.markdown("Add your meeting slots below. You can add upto 3 meeting slots.")
meeting_slots = []
meeting1 = st.checkbox("Add Meeting Slot 1")
if meeting1:
    meeting_1_name = st.text_input("Meeting Slot 1 Name")
    start_time_1 = st.time_input("Meeting Slot 1 Start Time")
    end_time_1 = st.time_input("Meeting Slot 1 End Time")
    day_1 = st.selectbox("Meeting Slot 1 Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    meeting_slots.append({
        "name": meeting_1_name,
        "start_time": start_time_1,
        "end_time": end_time_1,
        "day": day_1,
    })
meeting2 = st.checkbox("Add Meeting Slot 2")
if meeting2:
    meeting_2_name = st.text_input("Meeting Slot 2 Name")
    start_time_2 = st.time_input("Meeting Slot 2 Start Time")
    end_time_2 = st.time_input("Meeting Slot 2 End Time")
    day_2 = st.selectbox("Meeting Slot 2 Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    meeting_slots.append({
        "name": meeting_2_name,
        "start_time": start_time_2,
        "end_time": end_time_2,
        "day": day_2,
    })
meeting3 = st.checkbox("Add Meeting Slot 3")
if meeting3:
    meeting_3_name = st.text_input("Meeting Slot 3 Name")
    start_time_3 = st.time_input("Meeting Slot 3 Start Time")
    end_time_3 = st.time_input("Meeting Slot 3 End Time")
    day_3 = st.selectbox("Meeting Slot 3 Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    meeting_slots.append({
        "name": meeting_3_name,
        "start_time": start_time_3,
        "end_time": end_time_3,
        "day": day_3,
    })
# Convert times to 24 hour format
for meeting_slot in meeting_slots:
    meeting_slot["start_time"] = meeting_slot["start_time"].strftime("%H:%M")
    meeting_slot["end_time"] = meeting_slot["end_time"].strftime("%H:%M")

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

        # convert to 24 hour format
        for i in range(len(startTimes)):
            if startTimes[i][-2:] == 'AM':
                startTimes[i] = startTimes[i][:-3]
                startTimes[i] = startTimes[i].strip()
            else:
                hr = int(startTimes[i].split(':')[0])
                mins = int(startTimes[i].split(':')[1][:2])
                if mins == 0:
                    mins = '00'
                if hr == 12:
                    startTimes[i] = str(hr) + ':' + str(mins)
                else:
                    startTimes[i] = str(hr + 12) + ':' + str(mins)
            if endTimes[i][-2:] == 'AM':
                endTimes[i] = endTimes[i][:-3]
                endTimes[i] = endTimes[i].strip()
            else:
                hr = int(endTimes[i].split(':')[0])
                mins = int(endTimes[i].split(':')[1][:2])
                if mins == 0:
                    mins = '00'
                if hr == 12:
                    endTimes[i] = str(hr) + ':' + str(mins)
                else:
                    endTimes[i] = str(hr + 12) + ':' + str(mins)

        for i in range(len(days)):
            courses.append({"name": course, "day": days[i], "start_time": startTimes[i], "end_time": endTimes[i], "room": room})

for meeting_slot in meeting_slots:
    courses.append({"name": meeting_slot["name"], "day": meeting_slot["day"], "start_time": meeting_slot["start_time"], "end_time": meeting_slot["end_time"], "room": ""})

# button to show timetable
if st.button("Show Timetable"):
    # Create the Gantt chart
    fig = create_gantt_chart(courses)
    # Plot the Gantt chart
    st.plotly_chart(fig)