document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    //쿠키에서 캘린더아이디값 가져오기
    let calendarId = getCookieValue('calendarId');
    // console.log(calendarId);

    let postIdArray = [];

    var calendar = new FullCalendar.Calendar(calendarEl, {
        // plugins:['dayGridMonth','dayGridPlugin'],
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
            // {
            //     title: 'event1',
            //     start: '2022-03-01'
            // },
            // {
            //     title: 'event2',
            //     start: '2022-03-03',
            //     end: '2022-03-05'
            // },
            // {
            //     title: '대통령선거',
            //     start: '2022-03-09T12:30:00',
            //     allDay: false // will make the time show
            // }

            $.ajax({
                type: "GET",
                url: "/api/calendar/get",
                data: {calendarId: calendarId},
                success: function (response) {
                    // console.log(response.schedule);
                    const postArray = response.schedule;
                    for (let i = 0; i < postArray.length; i++) {
                        calendar.addEvent({
                            title: postArray[i]['content'],
                            start: postArray[i]['datatime'],
                            postId : postArray[i]['_id'],
                            nickname : postArray[i]['nickname']
                        })
                        postIdArray.push(postArray[i]['_id']);
                    }

                }
            })

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
            const closeBtn = modal.querySelector("#enter_close_btn");
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
            const month = '0' + (date.getMonth(dateArray[1]) + 1);
            //dateArray의 day부분
            const day = dateArray[2];

            const editDate = year.concat('-', month, '-', day);
            //스케줄 시작일을 수정/삭제 모달에 넣어주고있다.
            document.getElementById('edit_day').innerText = editDate;
            //스케줄 내용을 수정/삭제 모달에 넣어주고있다.
            document.querySelector("#edit_input").innerText = info.event.title;
            const modal = document.querySelector(".modal.remove");
            const overlay = modal.querySelector(".modal__overlay");
            const closeBtn = modal.querySelector("#edit_close_btn");
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

        }
    });

    // const postDomArray = document.getElementsByClassName('fc-daygrid-event-harness');
    // console.log(postDomArray);
    // Array.from(postDomArray).map((el) => console.log(el));
    // console.log(postIdArray);

    //완성된 캘린더 랜더
    calendar.render();
});

//새로운 포스트 생성
function enter_sche() {
    let calendarId = getCookieValue('calendarId');
    const nickName = 'nickname';
    const calendarid = calendarId;
    const date = $('#selec_day').text();
    const sche = $('#sche_input').val();
    $.ajax({
        type: 'POST',
        url: '/api/calendar/post/new',
        data: {calendarId: calendarid, nickname: nickName, dateTime: date, content: sche},
        success: function (response) {
            alert('등록완료!');
            window.location.reload();
        }
    });
}

//포스트 수정
function edit_sche() {
    const calendarid = '62283409f8c7b626d7a4f691';
    const postid = 'postId';
    const date = $('#edit_day').text();
    const sche = $('#edit_input').val();
    $.ajax({
        type: 'POST',
        url: '/api/calendar/post/edit',
        data: {calendarId: calendarid, postId: postid, dateTime: date, content: sche},
        success: function (response) {
            console.log(response);
        }
    });
}

function delete_sche() {
    const postId = 'postId';
    $.ajax({
        type: 'POST',
        url: '/api/calendar/post/delete',
        data: {postId: postId},
        success: function (response) {
            console.log(response);
        }
    });
}


// 네비게이션바 캘린더 리스트 받아온 후 보여주기
$(document).ready(function () {
    getCalendarList()
})
function getCalendarList(){
    let userId = getCookieValue('id');
    $.ajax({
        type: 'GET',
        url: '/api/calendar/list',
        data: {'id':userId},
        success: function (response) {
            //personal calendar append
            let temp_html = `
                <li class="personal-sche">
                    <a href="#" id="${response['personal']['_id']}">${response['personal']['name']}</a>
                </li>
            `
            $('#calendar-nav').append(temp_html)

            //team calendar append
            for (const calendar of response['team']['list']) {
                let temp_html = `
                    <li class="personal-sche">
                        <a href="#" id="${calendar['_id']}">${calendar['name']}</a>
                    </li>
                `
                $('#calendar-nav').append(temp_html)
            }
        }
    });
}
//get cookie function
const getCookieValue = (key) => {
  let cookieKey = key + "=";
  let result = "";
  const cookieArr = document.cookie.split(";");

  for(let i = 0; i < cookieArr.length; i++) {
    if(cookieArr[i][0] === " ") {
      cookieArr[i] = cookieArr[i].substring(1);
    }

    if(cookieArr[i].indexOf(cookieKey) === 0) {
      result = cookieArr[i].slice(cookieKey.length, cookieArr[i].length);
      return result;
    }
  }
  return result;
}

