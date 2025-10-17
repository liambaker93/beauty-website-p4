 document.addEventListener('DOMContentLoaded', function() {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          selectable: true,
          selectHelper: true,
          // events: {
          //   url: events_api_url,
          //   method: 'GET',
          //   failure: function(){
          //     alert('Could not get events from the server!');
          //   }
          // },
          select: function(start, end, allDays) {
            window.location.href = 'calendar_detail';            
          }
        });
        calendar.render();
      });