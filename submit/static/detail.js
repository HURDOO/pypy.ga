function init_view_code() {
    document.getElementById('view_code').onclick = () => {
        result = confirm('이 문제를 풀지 않고 다른 코드를 보면, 30%의 포인트만 얻을 수 있습니다. 코드를 보시겠습니까?')
        if (result) {
            window.location.href = location.protocol + '//' + location.host + location.pathname + '?view_code=true#code';
        }
        return false;
    }
}
