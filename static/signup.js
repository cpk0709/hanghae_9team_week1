const fillPw = () => {
    const pw = document.getElementById('pw');
    const pwCheck = document.getElementById('pw_check');
    if (pw != '') {
        pwCheck.classList.remove('hidden');
    }
}

const passwordConf = () => {
    const pw = document.getElementById('pw').value;
    const pw_conf = document.getElementById('pw-conf').value;

    const pwCheck = document.getElementById('pw_check');
    const pwConfCheck = document.getElementById('pwConf_check');

    if (pw != '') {
        const notCorect_span = document.querySelector('.pw_notCorect');
        const corect_span = document.querySelector('.pw_corect');

        if (pw !== pw_conf) {
            notCorect_span.classList.remove('hidden');
            document.getElementById('pw').value = '';
            corect_span.classList.add('hidden');
            pwConfCheck.classList.add('hidden');
            pwCheck.classList.add('hidden');
        } else {
            corect_span.classList.remove('hidden');
            notCorect_span.classList.add('hidden');
            pwConfCheck.classList.remove('hidden');
        }
    } else {
        alert('비밀번호를 입력해주세요');
    }
}

const signUp = () => {
    const id = document.getElementById('id');
    if (id.value != '') {
        const pw = document.getElementById('pw');

        //비밀번호 입력했을 때 나타나는 체크아이콘을 가져옴
        const pwCheck = document.getElementById('pw_check');
        //체크아이콘의 class 값들을 가져옴. hidden이 있다면 길이 2인 배열이고, 없으면 길이가 1인 즉, 제대로 입력했다는것
        const pwFlag = pwCheck.getAttribute('class').split(" ").length;

        //위 비밀번호와 같음. 비밀번호 확인쪽에서도 체크아이콘이 있다면 class값에 hidden이 remove되어 길이가 1인 배열일것임.
        const pwConfCheck = document.getElementById('pwConf_check');
        const pwConfFlag = pwConfCheck.getAttribute('class').split(" ").length;

        if(pwFlag === 1 && pwConfFlag === 1){
            alert('비밀번호까지 맞게 썼음');
        //    여기부터 아이디,비밀번호 가져와서 ajax로 넘기는 처리

        }else{
            alert('비밀번호를 확인해 주세요');
        }
    }else{
        alert('아이디를 입력하세요');
    }

}