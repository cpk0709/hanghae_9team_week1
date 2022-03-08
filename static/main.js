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
            //Modal 띄워주는 처리
            const dayTag = document.getElementById("selec_day");
            //클릭한 날짜를 모달 날짜태그에 넣어줌
            dayTag.innerText = info.dateStr;

            //클릭한 날짜 td태그
            const td = info.dayEl;
            const modal = document.querySelector(".modal.enter");
            const overlay = modal.querySelector(".modal__overlay");
            const closeBtn = modal.querySelector("#close_btn");
            //modal의 class="hidden"을 삭제
            const openModal = () => {
                modal.classList.remove("hidden");
            }
            //modal의 class="hidden"을 추가가
            const closeModal = () => {
                modal.classList.add("hidden");
            }
            overlay.addEventListener("click", closeModal);
            closeBtn.addEventListener("click", closeModal);
            td.addEventListener("click", openModal());
        },
        //여기서 수정/삭제처리할 예정
        eventClick: function (info) {
            //클릭한 일정의 시작날짜데이터를 dateInfo에 담아주고있음
            const dateInfo = info.el.fcSeg.eventRange.range.start;
            //자바스크립트 Date함수를 통해 date 인스턴스 생성
            const date = new Date(dateInfo);
            //오브젝트탑인인 date를 string으로 바꾼 후 split으로 나누어 배열로 만들고있음.
            const dateArray = String(date).split(" ");
            //dateArray의 year부분
            const year = dateArray[3];
            //dateArray의 month부분. month는 0부터시작이라 +1해줌. 두자리로 만들기위해 '0'붙임
            const month = '0' + (date.getMonth(dateArray[1])+1);
            //dateArray의 day부분
            const day = dateArray[2];

            const editDate = year.concat('-',month,'-',day);
            //스케줄 시작일을 수정/삭제 모달에 넣어주고있다.
            document.getElementById('edit_day').innerText = editDate;
            //스케줄 내용을 수정/삭제 모달에 넣어주고있다.
            document.querySelector("#edit_input").innerText = info.event.title;
            const modal = document.querySelector(".modal.remove");
            const overlay = modal.querySelector(".modal__overlay");
            const closeBtn = modal.querySelector("#close_btn");
            //modal의 class="hidden"을 삭제
            const openModal = () => {
                modal.classList.remove("hidden");
            }
            //modal의 class="hidden"을 추가가
            const closeModal = () => {
                modal.classList.add("hidden");
            }

            overlay.addEventListener("click", closeModal);
            closeBtn.addEventListener("click", closeModal);

            openModal();


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