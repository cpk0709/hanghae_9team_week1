document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'ko',
        selectable: true,
        aspectRatio: 1.35,
        //navLinks => day 클릭했을때 상세보기
        // navLinks: true,
        editable: true,
        // droppable:true,
        //기본 스케줄 입력 메서드
        // select: function (arg) {
        //     var title = prompt('Event Title:');
        //     if (title) {
        //         calendar.addEvent({
        //             title: title,
        //             start: arg.start,
        //             end: arg.end,
        //             allDay: arg.allDay
        //                        })
        //     }
        //     calendar.unselect()
        // },
        events: [
            {
                title: 'event1',
                start: '2022-03-01'
            },
            // {
            //     title: 'event1-1',
            //     start: '2022-03-01'
            // },
            // {
            //     title: 'event1-2',
            //     start: '2022-03-01'
            // },
            // {
            //     title: 'event1-3',
            //     start: '2022-03-01'
            // },
            // {
            //     title: 'event1-4',
            //     start: '2022-03-01'
            // },
            {
                title: 'event2',
                start: '2022-03-03',
                end: '2022-03-05'
            },
            {
                title: 'event3',
                start: '2022-03-09T12:30:00',
                allDay: false // will make the time show
            }
        ],
        dateClick: function (info) {

            const dayTag = document.getElementById("selec_day");
            //클릭한 날짜를 모달 날짜태그에 넣어줌
            dayTag.innerText = info.dateStr;

            //클릭한 날짜 td태그
            const td = info.dayEl;
            const modal = document.querySelector(".modal.enter");
            const overlay = modal.querySelector(".modal__overlay");
            const closeBtn = modal.querySelector("#close_btn");
            const openModal = () => {
                modal.classList.remove("hidden");
            }
            const closeModal = () => {
                modal.classList.add("hidden");
            }
            overlay.addEventListener("click", closeModal);
            closeBtn.addEventListener("click", closeModal);
            td.addEventListener("click", openModal());
        },
        //여기서 수정/삭제처리할 예정
        eventClick: function (info) {
            alert('Event: ' + info.event.title);


            const modal = document.querySelector(".modal.enter");
            const overlay = modal.querySelector(".modal__overlay");
            const closeBtn = modal.querySelector("#close_btn");
            // alert('Coordinates: ' + info.jsEvent.pageX + ',' + info.jsEvent.pageY);

            // change the border color just for fun
            // info.el.style.borderColor = 'red';
        }
    });

    calendar.render();
});

//새로운 스케줄 입력하는 메서드
function enter_sche() {
    const date = $('#selec_day').text();
    const sche = $('#sche_input').val();
    console.log(date);
    console.log(sche);
    $.ajax({
        type: 'POST',
        url: '/test',
        data: {date_giv: date, sche_give: sche},
        success: function (response) {
            alert(response);
        }
    });
}