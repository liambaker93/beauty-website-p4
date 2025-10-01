document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridDay',
        slotDuration: '00:45:00',
        slotMinTime: '08:00:00',
        slotMaxTime: '18:00:00',
    });
    calendar.render();
});