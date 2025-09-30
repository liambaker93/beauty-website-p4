 document.addEventListener('DOMContentLoaded', function() {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          selectable: true,
          selectHelper: true,
          select: function(start, end, allDays) {
            window.location.href = 'calendar_detail';            
          }
        });
        calendar.render();
      });