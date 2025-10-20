document.addEventListener('DOMContentLoaded', function() {
    if (eventUser) {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'timeGridDay',
            slotMinTime: '08:00:00',
            slotMaxTime: '18:00:00',
            slotLabelInterval: '01:00:00',
            selectable: 'true',
            events: {
                url: events_api_url,
                method: 'GET',
                failure: function(){
                    alert('Could not get events from the server!');
                }
            },
        });
        calendar.render();
    };
});